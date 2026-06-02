import fitz 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from dotenv import load_dotenv



def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file."""
    doc = fitz.open(file_path)
    all_text = []
    
    for page_num, page in enumerate(doc):
        text = page.get_text("text")  # "text" mode = clean plain text
        if text.strip():              # skip blank pages
            all_text.append(f"--- Page {page_num + 1} ---\n{text}")
    
    doc.close()
    return "\n\n".join(all_text)



def chunk_text(text: str, chunk_size: int = 3000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks for LLM processing."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)

load_dotenv()  

def get_llm():
    """Returns a configured Groq LLM instance."""
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,     
        max_tokens=2048
    )

def summarize_document(chunks: list[str]) -> str:
    """Summarize a legal document from its chunks."""
    llm = get_llm()
    
    # If short enough, summarize in one shot
    if len(chunks) == 1:
        prompt = f"""You are a legal document assistant. 
Summarize the following legal document in plain English.
Be clear, concise, and avoid legal jargon.
Organize your summary with these sections:
- What this document is
- Key parties involved
- Main obligations and rights
- Important dates or deadlines
- Any notable conditions

Document:
{chunks[0]}"""
        return llm.invoke(prompt).content
    
    # For longer docs — summarize each chunk, then combine
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        prompt = f"""Summarize this section ({i+1} of {len(chunks)}) 
of a legal document in 3-5 plain English sentences:

{chunk}"""
        summary = llm.invoke(prompt).content
        chunk_summaries.append(summary)
    
    # Final pass — combine chunk summaries into one clean summary
    combined = "\n\n".join(chunk_summaries)
    final_prompt = f"""You are a legal document assistant.
Below are section-by-section summaries of a legal document.
Combine them into one clear, organized summary in plain English.
Use these sections:
- What this document is
- Key parties involved  
- Main obligations and rights
- Important dates or deadlines
- Any notable conditions

Section summaries:
{combined}"""
    
    return llm.invoke(final_prompt).content

def flag_risky_clauses(chunks: list[str]) -> list[str]:
    """Identify potentially risky or unfair clauses."""
    llm = get_llm()
    all_flags = []
    
    for chunk in chunks:
        prompt = f"""You are a legal document reviewer protecting the reader's interests.
Analyze the following section and identify any clauses that are:
- Unusual, one-sided, or potentially unfair
- Related to termination, penalties, or liability
- Auto-renewal or lock-in terms
- Data sharing or privacy concerns
- Non-compete or exclusivity restrictions
- Hidden fees or payment obligations

For each risky clause found, respond in this format:
⚠️ [Clause Type]: [Plain English explanation of the risk]

If no risky clauses are found, respond with: NONE

Document section:
{chunk}"""
        
        response = llm.invoke(prompt).content
        if response.strip() != "NONE":
            # Split by ⚠️ to get individual flags
            flags = [f.strip() for f in response.split("⚠️") if f.strip()]
            all_flags.extend(flags)
    
    return all_flags