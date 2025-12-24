import os
from langchain_core.documents import Document

def infer_step_from_qml(filename: str) -> str:
    base = filename.replace(".qml", "")
    return base[:-4] if base.endswith("View") else base

def load_qml_documents(folder):
    docs = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".qml"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    docs.append(
                        Document(
                            page_content=f.read(),
                            metadata={
                                "step": infer_step_from_qml(file),
                                "type": "qml",
                                "source": file,
                                "path": path,
                            },
                        )
                    )
    return docs