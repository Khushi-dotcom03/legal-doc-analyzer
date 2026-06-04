from agent import legal_doc_graph
from utils import extract_text_from_pdf

# --- Test 1: Full analysis, no question ---
print("=" * 50)
print("TEST 1: Analysis only (no follow-up question)")
print("=" * 50)

text = extract_text_from_pdf("assets/sample.pdf")

result = legal_doc_graph.invoke({
    "raw_text": text,
    "chunks": [],
    "summary": "",
    "risky_clauses": [],
    "question": "",   # empty = skip QA node
    "answer": "",
    "error": ""
})

print("\n📝 SUMMARY:")
print(result["summary"])
print(f"\n🚩 RISKY CLAUSES ({len(result['risky_clauses'])} found):")
for clause in result["risky_clauses"]:
    print(f"  ⚠️  {clause}")

# --- Test 2: With a follow-up question ---
print("\n" + "=" * 50)
print("TEST 2: Analysis + follow-up question")
print("=" * 50)

result2 = legal_doc_graph.invoke({
    "raw_text": text,
    "chunks": [],
    "summary": "",
    "risky_clauses": [],
    "question": "Can I terminate this agreement early and what are the penalties?",
    "answer": "",
    "error": ""
})

print("\n💬 QUESTION ANSWERED:")
print(result2["answer"])