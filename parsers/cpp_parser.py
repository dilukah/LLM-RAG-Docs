import os
import re
from langchain_core.documents import Document

CLASS_BLOCK_REGEX = re.compile(
    r"(class\s+(\w+Step)\b[\s\S]*?^\};)",
    re.MULTILINE
)

def extract_step_class_blocks(text: str):
    results = []
    for match in CLASS_BLOCK_REGEX.finditer(text):
        results.append((match.group(2), match.group(1)))
    return results

def load_cpp_documents(folder):
    docs = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith((".h", ".hpp", ".cpp")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for step, block in extract_step_class_blocks(f.read()):
                        docs.append(
                            Document(
                                page_content=block,
                                metadata={
                                    "step": step,
                                    "type": "cpp",
                                    "source": file,
                                    "path": path,
                                },
                            )
                        )
    return docs