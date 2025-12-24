from models import StepArtifact

def build_step_registry(cpp_docs, qml_docs):
    registry = {}

    for doc in cpp_docs + qml_docs:
        step = doc.metadata["step"]
        registry.setdefault(step, StepArtifact(step))

        if doc.metadata["type"] == "cpp":
            registry[step].cpp_docs.append(doc)
        else:
            registry[step].qml_docs.append(doc)

    return registry

def build_step_context(step):
    return "\n\n".join(d.page_content for d in step.cpp_docs + step.qml_docs)