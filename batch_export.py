# batch_export.py
from registry import build_step_context
from docs_export import export_html
from prompts import USER_DOC_PROMPT, DEV_DOC_PROMPT

def export_all_steps(registry, llm):
    for step_name, step in registry.items():
        context = build_step_context(step)

        user_doc = llm.invoke(USER_DOC_PROMPT.format(context=context))
        dev_doc = llm.invoke(DEV_DOC_PROMPT.format(context=context))

        export_html(step_name, user_doc, "User")
        export_html(step_name, dev_doc, "Developer")