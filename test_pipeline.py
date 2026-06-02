from utils import extract_text_from_pdf, chunk_text, summarize_document, flag_risky_clauses

# --- Config ---
PDF_PATH = "assets/sample.pdf"

# --- Run pipeline ---
print("📄 Extracting text...")
text = extract_text_from_pdf(PDF_PATH)
print(f"✅ Extracted {len(text)} characters\n")

print("✂️ Chunking text...")
chunks = chunk_text(text)
print(f"✅ Created {len(chunks)} chunks\n")

print("🤖 Summarizing document...")
summary = summarize_document(chunks)
print("📝 SUMMARY:")
print(summary)
print()

print("🚩 Flagging risky clauses...")
flags = flag_risky_clauses(chunks)
print(f"⚠️ Found {len(flags)} risky clause(s):")
for flag in flags:
    print(f"  • {flag}")