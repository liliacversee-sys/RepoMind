import os
from app.llm.llm_service import ask_llm


class CodeSearch:

    def search(self, repo_path, query):

        results = []
        keywords = query.lower().split()

        for root, _, files in os.walk(repo_path):

            for file in files:

                if file.endswith(".py"):

                    path = os.path.join(root, file)

                    try:
                        with open(path, "r", errors="ignore") as f:

                            content = f.read()

                            if any(word in content.lower() for word in keywords):

                                results.append({
                                    "file": path,
                                    "snippet": content[:500],
                                    "full_code": content[:2000]
                                })

                    except:
                        pass

        results = results[:5]

        context = ""

        for r in results:
            context += f"""
File: {r['file']}

Code:
{r['full_code']}
"""

        answer = ask_llm(query, context)

        return {
            "results": results,
            "answer": answer
        }