import streamlit as st
from agent import legal_doc_graph, answer_followup
from utils import extract_text_from_pdf
import tempfile
import os

# --- Page config (must be first Streamlit call) ---
st.set_page_config(
    page_title="AI Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# --- Initialize session state ---
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# --- Header ---
st.title("⚖️ AI Legal Document Analyzer")
st.markdown(
    "Upload any legal document — **offer letter, rent agreement, T&C** — "
    "and get a plain English summary, flagged risky clauses, "
    "and answers to your questions."
)
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Supported: offer letters, rent agreements, T&C, contracts"
    )

    if uploaded_file is not None:

        # Show file info
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        st.caption(f"Size: {uploaded_file.size / 1024:.1f} KB")

        # Analyze button
        analyze_btn = st.button(
            "🔍 Analyze Document",
            type="primary",
            use_container_width=True
        )

        if analyze_btn:
            # Save uploaded file to a temp location
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".pdf"
            ) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Run the pipeline
            with st.spinner(" Analyzing your document... this may take 30–60 seconds"):
                try:
                    raw_text = extract_text_from_pdf(tmp_path)

                    result = legal_doc_graph.invoke({
                        "raw_text": raw_text,
                        "chunks": [],
                        "summary": "",
                        "risky_clauses": [],
                        "question": "",
                        "answer": "",
                        "error": ""
                    })

                    # Store in session state
                    st.session_state.analysis_result = result
                    st.session_state.file_processed = True
                    st.session_state.chat_history = []  # reset chat for new doc

                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")

                finally:
                    # Always clean up the temp file
                    os.unlink(tmp_path)

            st.rerun()  # rerun to show results immediately

with col2:
    if st.session_state.file_processed and st.session_state.analysis_result:
        result = st.session_state.analysis_result

        # Check for errors from the graph
        if result.get("error"):
            st.error(f"⚠️ {result['error']}")

        else:
            # --- Tabs for organized display ---
            tab1, tab2, tab3 = st.tabs([
                "📝 Summary",
                "🚩 Risky Clauses",
                "💬 Ask Questions"
            ])

            with tab1:
                st.subheader("Document Summary")
                st.markdown(result["summary"])

                # Download summary button
                st.download_button(
                    label="⬇️ Download Summary",
                    data=result["summary"],
                    file_name="summary.txt",
                    mime="text/plain"
                )

            with tab2:
                st.subheader("Flagged Clauses")

                clauses = result["risky_clauses"]

                if not clauses:
                    st.success("✅ No major risky clauses detected!")
                else:
                    st.warning(
                        f"Found **{len(clauses)}** clause(s) that need attention:"
                    )
                    for i, clause in enumerate(clauses, 1):
                        with st.expander(f"⚠️ Clause {i}", expanded=True):
                            st.markdown(clause)

            with tab3:
                st.subheader("Ask a Question")
                st.caption(
                    "Ask anything about this document — "
                    "clauses, obligations, deadlines, rights..."
                )

                # Display chat history
                for chat in st.session_state.chat_history:
                    with st.chat_message("user"):
                        st.write(chat["question"])
                    with st.chat_message("assistant"):
                        st.write(chat["answer"])

                # Question input
                question = st.chat_input(
                    "E.g. Can I terminate early? What are my obligations?"
                )

                if question:
                    with st.chat_message("user"):
                        st.write(question)

                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            answer = answer_followup(
                                st.session_state.analysis_result,
                                question
                            )
                        st.write(answer)

                    # Save to history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer
                    })

    else:
        # Nothing uploaded yet — show placeholder
        st.info(" Upload a document on the left to get started.")

with st.sidebar:
    st.header("ℹ About")
    st.markdown("""
    This tool uses AI to help you understand legal documents.
    
    **What it does:**
    - Summarizes documents in plain English
    - Flags potentially risky clauses
    - Answers your specific questions
    
    **Supported documents:**
    - Offer letters
    - Rent agreements
    - Terms & Conditions
    - Service contracts
    - NDAs
    """)

    st.divider()
    st.caption(" This tool is for informational purposes only and is not a substitute for legal advice.")

    # Show stats if document is processed
    if st.session_state.file_processed and st.session_state.analysis_result:
        st.divider()
        st.subheader(" Document Stats")
        result = st.session_state.analysis_result
        st.metric("Chunks analyzed", len(result.get("chunks", [])))
        st.metric("Risky clauses found", len(result.get("risky_clauses", [])))
        st.metric("Questions asked", len(st.session_state.chat_history))