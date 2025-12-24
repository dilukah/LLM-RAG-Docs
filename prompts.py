USER_DOC_PROMPT = """
You are generating END-USER documentation.

Explain:
- What this step does
- UI controls
- Effect on the image
- Typical usage

Avoid mentioning C++, QML, or internal implementation.

Context:
{context}
"""

DEV_DOC_PROMPT = """
You are generating DEVELOPER documentation.

Explain:
- Class responsibilities
- Properties and signals
- Processing logic
- QML ↔ C++ bindings
- Extension points

Use precise technical language.

Context:
{context}
"""

RAG_QA_PROMPT = """
Answer strictly using the context below.
If the answer is not present, reply:
"Not found in the provided context."

Context:
{context}

Question:
{question}
"""