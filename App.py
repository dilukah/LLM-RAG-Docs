import streamlit as st
from config import CPP_DIR, QML_DIR, PERSIST_DIR, COLLECTION_NAME
from parsers.cpp_parser import load_cpp_documents
from parsers.qml_parser import load_qml_documents
from registry import build_step_registry, build_step_context
from indexing import build_vectorstore
from docs_export import export_html
from rag import get_llm
from prompts import USER_DOC_PROMPT, DEV_DOC_PROMPT, RAG_QA_PROMPT
from batch_export import export_all_steps
import re

st.set_page_config(layout="wide")
st.title("📘 AI Documentation Generator")

if "registry" not in st.session_state:
    cpp_docs = load_cpp_documents(CPP_DIR)
    qml_docs = load_qml_documents(QML_DIR)

    registry = build_step_registry(cpp_docs, qml_docs)
    db = build_vectorstore(cpp_docs + qml_docs, PERSIST_DIR, COLLECTION_NAME)

    st.session_state.registry = registry
    st.session_state.retriever = db.as_retriever(search_kwargs={"k": 5})
    st.session_state.llm = get_llm()

step_names = sorted(st.session_state.registry.keys())
#selected = st.sidebar.selectbox("Select Module", step_names)
#step = st.session_state.registry[selected]

def display_name(name: str) -> str:
    # Remove trailing 'Step' only
    name = re.sub(r'Step$', '', name)

    # Split CamelCase / PascalCase into words
    name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)

    return name.strip()


display_to_key = {display_name(k): k for k in step_names}
selected = st.sidebar.selectbox(
    "Select Module",
    step_names,
    format_func=display_name
)
step = st.session_state.registry[selected]
#step = st.session_state.registry[display_to_key[selected_display]]

with st.expander("Show Source Files"):
    st.subheader("C++ Files")
    for doc in step.cpp_docs:
        st.markdown(f"- `{doc.metadata['path']}`")

    st.subheader("QML Files")
    for doc in step.qml_docs:
        st.markdown(f"- `{doc.metadata['path']}`")

def generate_editable_doc(step_name: str, prompt_template: str, doc_type: str):
    """
    Generates or regenerates the doc and shows an editable text area.
    Stores content in st.session_state[<step>_<doc_type>_doc].
    """
    key = f"{step_name}_{doc_type}_doc"

    # Regenerate button
    if st.button(f"🔄 Generate {doc_type} Documentation", key=f"regen_{key}"):
        context = build_step_context(step)
        st.session_state[key] = st.session_state.llm.invoke(prompt_template.format(context=context))

    # If not yet generated, generate initially
    if key not in st.session_state:
        context = build_step_context(step)
        st.session_state[key] = st.session_state.llm.invoke(prompt_template.format(context=context))

    # Editable area
    st.session_state[key] = st.text_area(
        f"Edit {doc_type} Documentation before export:",
        value=st.session_state[key],
        height=400,
        key=f"textarea_{key}"
    )

    # Optional preview
    with st.expander("Preview", expanded=False):
        st.markdown(st.session_state[key])

col1, col2 = st.columns([1, 1])


with col1:
    generate_editable_doc(selected, USER_DOC_PROMPT, "User")
    if st.button("💾 Save & Export User Doc"):
        path = export_html(selected, st.session_state[f"{selected}_User_doc"], "User")
        st.success(f"User doc exported → {path}")

with col2:
    generate_editable_doc(selected, DEV_DOC_PROMPT, "Developer")
    if st.button("💾 Save & Export Developer Doc"):
        path = export_html(selected, st.session_state[f"{selected}_Developer_doc"], "Developer")
        st.success(f"Developer doc exported → {path}")


    st.divider()
st.subheader("💬 Ask a Question")

query = st.text_input("Ask about any step, property, or behavior")

if st.button("Get Answer") and query:
    docs = st.session_state.retriever.get_relevant_documents(query)
    context = "\n\n".join(d.page_content for d in docs)

    answer = st.session_state.llm.invoke(
        RAG_QA_PROMPT.format(context=context, question=query)
    )

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Retrieved Context"):
        for d in docs:
            st.markdown(f"**{d.metadata['step']}** — {d.metadata['source']}")
            st.code(d.page_content[:600])

if st.sidebar.button("📦 Export ALL Docs"):
    export_all_steps(st.session_state.registry, st.session_state.llm)
    st.sidebar.success("All documentation exported")