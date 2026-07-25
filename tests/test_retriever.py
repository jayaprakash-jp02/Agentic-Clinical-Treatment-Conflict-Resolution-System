from knowledge.retriever import GuidelineRetriever


retriever = GuidelineRetriever()


results = retriever.retrieve(
    query="""
Patient has Type 2 Diabetes,
CKD Stage 3b,
eGFR 28,
currently taking Metformin.
""",
    guideline_directory="processed/ADA_2025",
    top_k=3,
)


print()

print("=" * 80)

print("Retrieved Chunks")

print("=" * 80)

for i, result in enumerate(results, start=1):

    print()

    print(f"Rank {i}")

    print("-" * 60)

    print("Distance :", result["score"])

    print()

    print(result["chunk"]["text"][:700])

    print()