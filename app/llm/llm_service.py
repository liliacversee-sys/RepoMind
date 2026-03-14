import ollama

def ask_llm(question, context):

    prompt = f"""
You are a senior software engineer analyzing a code repository.

Answer the question using the provided code context.

Context:
{context}

Question:
{question}

Explain clearly and reference files/functions if possible.
"""

    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error calling Ollama API: {str(e)}"