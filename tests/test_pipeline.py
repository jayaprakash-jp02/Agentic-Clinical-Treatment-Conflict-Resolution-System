from knowledge.guideline_pipeline import GuidelineRetriever

pipeline = GuidelineRetriever(
    "data/ADA_Guideline.pdf"
)

results = pipeline.retrieve(
    "medical AI framework"
)

print("\nRetrieved Chunks\n")

for i, chunk in enumerate(results, start=1):
    print("=" * 80)
    print(f"Result {i}\n")
    print(chunk)