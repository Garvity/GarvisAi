from langgraph.graph import END, START, StateGraph

from agents.chat_agent import chat_agent
from agents.coding_agent import coding_agent
from agents.image_analyzer_agent import image_analyzer_agent
from agents.image_gen_agent import image_gen_agent
from agents.pdf_agent import pdf_agent
from agents.pdf_rag_agent import pdf_rag_agent
from agents.ppt_agent import ppt_agent
from agents.search_agent import search_agent
from graph.router import router
from graph.state import AgentState

workflow = StateGraph(AgentState)

workflow.add_node("router", router)
workflow.add_node("chat", chat_agent)
workflow.add_node("search", search_agent)
workflow.add_node("coding", coding_agent)
workflow.add_node("pdf", pdf_agent)
workflow.add_node("ppt", ppt_agent)
workflow.add_node("image", image_gen_agent)
workflow.add_node("pdfRag", pdf_rag_agent)
workflow.add_node("imageAnalyzer", image_analyzer_agent)

workflow.add_edge(START, "router")


def _route(state):
    agent = state.get("agent")
    match agent:
        case "chat":
            return "chat"
        case "search":
            return "search"
        case "coding":
            return "coding"
        case "pdf":
            return "pdf"
        case "ppt":
            return "ppt"
        case "image":
            return "image"
        case "pdfRag":
            return "pdfRag"
        case "imageAnalyzer":
            return "imageAnalyzer"
        case _:
            return "chat"


workflow.add_conditional_edges(
    "router",
    _route,
    {
        "chat": "chat",
        "search": "search",
        "coding": "coding",
        "pdf": "pdf",
        "ppt": "ppt",
        "image": "image",
        "pdfRag": "pdfRag",
        "imageAnalyzer": "imageAnalyzer",
    },
)

workflow.add_edge("search", "chat")
workflow.add_edge("chat", END)
workflow.add_edge("coding", END)
workflow.add_edge("pdf", END)
workflow.add_edge("ppt", END)
workflow.add_edge("image", END)
workflow.add_edge("pdfRag", END)
workflow.add_edge("imageAnalyzer", END)

graph = workflow.compile()
