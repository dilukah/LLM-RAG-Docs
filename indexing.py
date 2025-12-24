from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

def build_vectorstore(documents, persist_dir, collection):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=[
            "\nclass ",
            "\nQ_PROPERTY",
            "\nsignals:",
            "\npublic:",
            "\nprivate:",
            "\nItem {",
            "\nRowLayout {",
        ],
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=persist_dir,
        collection_name=collection,
    )