USER_DOC_PROMPT = """
You are writing END-USER documentation for a visual image editing feature.

Audience:
Non-technical users.

Rules (must follow):
- Do NOT mention classes, steps, pipelines, inputs/outputs, frameworks, or internal identifiers
- Do NOT explain how the feature is implemented
- Do NOT use developer or system terminology
- Do NOT mention C++, QML, code, data flow, or processing logic
- Do NOT include "Title:" or any header label; use only the human-friendly feature name as a heading if needed

Naming:
- Refer to the feature using a human-friendly name only (e.g., “Brightness”)
- Never include internal suffixes like “Step”

Content to include:
- What the feature does, in plain language
- What controls the user sees and how to use them
- What visual effect it has on the image
- Common, real-world usage examples

Tone & style:
- Clear, concise, and product-focused
- Describe what the user can do and what they will see
- Assume the user is interacting with a UI
- Avoid promotional or marketing language
- Prefer clear, neutral explanations over enthusiastic phrasing

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