from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from app.search.vector_search import VectorSearch
from app.search.code_search import CodeSearch

from app.repo.cloner import clone_repository
from app.repo.scanner import scan_repository
from app.parser.treesitter_parser import TreeSitterParser

from app.graph.dependency_graph import build_dependency_graph

from app.llm.llm_service import ask_llm

load_dotenv()

app = FastAPI(title="RepoMind AI")

vector_search = VectorSearch()
code_search = CodeSearch()

dependency_graph = None
current_repo_path = None


# Request model for /ask
class AskRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RepoMind AI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            input, button { padding: 10px; margin: 10px 0; }
            #result { margin-top: 20px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>RepoMind AI</h1>
        <p>Analyze a repository and ask questions about the code.</p>
        
        <h2>Step 1: Analyze Repository</h2>
        <input type="text" id="repoUrl" placeholder="Enter GitHub repo URL" size="50">
        <button onclick="analyzeRepo()">Analyze</button>
        <div id="analyzeResult"></div>
        
        <h2>Step 2: Ask a Question</h2>
        <input type="text" id="question" placeholder="Ask a question about the code" size="50">
        <button onclick="askQuestion()">Ask</button>
        <div id="result"></div>
        
        <script>
            async function analyzeRepo() {
                const url = document.getElementById('repoUrl').value;
                const result = document.getElementById('analyzeResult');
                result.textContent = 'Analyzing...';
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(url)
                    });
                    const data = await response.json();
                    result.textContent = JSON.stringify(data, null, 2);
                } catch (e) {
                    result.textContent = 'Error: ' + e.message;
                }
            }
            
            async function askQuestion() {
                const question = document.getElementById('question').value;
                const result = document.getElementById('result');
                result.textContent = 'Thinking...';
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({question})
                    });
                    const data = await response.json();
                    result.textContent = JSON.stringify(data, null, 2);
                } catch (e) {
                    result.textContent = 'Error: ' + e.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content


@app.post("/analyze")
def analyze_repo(repo_url: str):

    global dependency_graph
    global current_repo_path

    print("Cloning repository...")
    repo_path = clone_repository(repo_url)

    current_repo_path = repo_path

    print("Scanning repository...")
    files = scan_repository(repo_path)

    print("Total files found:", len(files))

    parser = TreeSitterParser("python")

    parsed_data = []

    print("Parsing files...")

    for file in files:
        try:
            result = parser.analyze_file(file)

            parsed_data.append({
                "file": file,
                "data": result
            })

        except Exception as e:
            print("Error parsing:", file, e)

    print("Building dependency graph...")

    dependency_graph = build_dependency_graph(parsed_data)

    print("Building vector index...")
    vector_search.build_index(repo_path)

    print("Analysis complete")

    return {
        "total_files": len(files),
        "parsed_files": len(parsed_data),
        "graph_nodes": len(dependency_graph.nodes),
        "graph_edges": list(dependency_graph.edges)[:20]
    }


@app.post("/ask")
def ask_repo(data: AskRequest):

    if not current_repo_path:
        return {"error": "Analyze a repository first using /analyze"}

    search_results = code_search.search(current_repo_path, data.question)

    context = ""
    if "results" in search_results:
        for result in search_results["results"][:5]:
            context += f"File: {result.get('file', '')}\nCode: {result.get('full_code', '')}\n\n"

    answer = search_results.get("answer") or ask_llm(data.question, context)

    return {"question": data.question, "answer": answer, "context": context}