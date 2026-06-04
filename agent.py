from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from utils import chunk_text, summarize_document, flag_risky_clauses
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# --- State definition ---
class DocAnalysisState(TypedDict):
    raw_text: str           # full extracted PDF text
    chunks: list[str]       # chunked version
    summary: str            # plain English summary
    risky_clauses: list[str]  # flagged clauses
    question: str           # user's follow-up question (empty string if none)
    answer: str             # QA node's response
    error: str              # any error message (empty string if none)

    # --- Node 1: Chunk the raw text ---
def chunk_node(state: DocAnalysisState) -> dict:
    """Split raw text into processable chunks."""
    try:
        chunks = chunk_text(state["raw_text"])
        return {"chunks": chunks, "error": ""}
    except Exception as e:
        return {"chunks": [], "error": f"Chunking failed: {str(e)}"}


# --- Node 2: Summarize ---
def summarize_node(state: DocAnalysisState) -> dict:
    """Summarize the document from chunks."""
    if state.get("error"):
        return {"summary": ""}  # skip if previous node errored
    try:
        summary = summarize_document(state["chunks"])
        return {"summary": summary}
    except Exception as e:
        return {"summary": "", "error": f"Summarization failed: {str(e)}"}


# --- Node 3: Flag risky clauses ---
def flag_node(state: DocAnalysisState) -> dict:
    """Identify risky or unfair clauses."""
    if state.get("error"):
        return {"risky_clauses": []}
    try:
        flags = flag_risky_clauses(state["chunks"])
        return {"risky_clauses": flags}
    except Exception as e:
        return {"risky_clauses": [], "error": f"Flagging failed: {str(e)}"}


# --- Node 4: Answer follow-up questions ---
def qa_node(state: DocAnalysisState) -> dict:
    """Answer a follow-up question using the document summary as context."""
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
    
    prompt = f"""You are a legal document assistant.
A user has uploaded a legal document and asked a follow-up question.
Use the document summary and flagged clauses below as context.

Document Summary:
{state["summary"]}

Flagged Risky Clauses:
{chr(10).join(state["risky_clauses"]) if state["risky_clauses"] else "None identified"}

User Question:
{state["question"]}

Answer clearly and in plain English. If the answer isn't in the document, say so honestly."""
    
    try:
        answer = llm.invoke(prompt).content
        return {"answer": answer}
    except Exception as e:
        return {"answer": "", "error": f"QA failed: {str(e)}"}
    


def should_run_qa(state: DocAnalysisState) -> str:
    """Decide whether to run the QA node."""
    if state.get("error"):
        return "end"
    if state.get("question", "").strip():
        return "qa"
    return "end"

def build_graph():
    """Build the LangGraph document analysis graph."""
    
    graph = StateGraph(DocAnalysisState)
    
    # --- Add nodes ---
    graph.add_node("chunk", chunk_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("flag", flag_node)
    graph.add_node("qa", qa_node)
    
    # --- Set entry point ---
    graph.set_entry_point("chunk")
    
    # --- Add edges (straight connections) ---
    graph.add_edge("chunk", "summarize")
    graph.add_edge("summarize", "flag")
    
    # --- Add conditional edge after flag ---
    graph.add_conditional_edges(
        "flag",                    # from this node
        should_run_qa,             # run this function to decide
        {
            "qa": "qa",            # if returns "qa" → go to qa node
            "end": END             # if returns "end" → terminate
        }
    )
    
    # --- QA always ends after answering ---
    graph.add_edge("qa", END)
    
    return graph.compile()


# Compile once at module level — import this in app.py
legal_doc_graph = build_graph()

def answer_followup(existing_result: dict, new_question: str) -> str:
    from agent import qa_node, DocAnalysisState
    state = {**existing_result, "question": new_question, "answer": ""}
    return qa_node(state)["answer"]