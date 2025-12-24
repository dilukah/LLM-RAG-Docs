from langchain_ollama import OllamaLLM

def get_llm():
    return OllamaLLM(model="mistral")

def answer_question(llm, docs, query):
    context = "\n\n".join(d.page_content for d in docs)
    prompt = f"""
Answer strictly using the context below.
If not found, say "Not found in the provided context."

Context:
{context}

Question:
{query}
"""
    return llm.invoke(prompt)