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

st.set_page_config(layout="wide")
st.title("📘 Documentation Generator")

if "registry" not in st.session_state:
    cpp_docs = load_cpp_documents(CPP_DIR)
    qml_docs = load_qml_documents(QML_DIR)

    registry = build_step_registry(cpp_docs, qml_docs)
    db = build_vectorstore(cpp_docs + qml_docs, PERSIST_DIR, COLLECTION_NAME)

    st.session_state.registry = registry
    st.session_state.retriever = db.as_retriever(search_kwargs={"k": 5})
    st.session_state.llm = get_llm()

step_names = sorted(st.session_state.registry.keys())
selected = st.sidebar.selectbox("Select Step", step_names)
step = st.session_state.registry[selected]

if st.button("📄 Generate User Documentation"):
    context = build_step_context(step)
    user_doc = st.session_state.llm.invoke(
        USER_DOC_PROMPT.format(context=context)
    )
    st.markdown(user_doc)
    export_html(selected, user_doc, "User")

if st.button("🛠 Generate Developer Documentation"):
    context = build_step_context(step)
    dev_doc = st.session_state.llm.invoke(
        DEV_DOC_PROMPT.format(context=context)
    )
    st.markdown(dev_doc)
    export_html(selected, dev_doc, "Developer")


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