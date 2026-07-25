from pathlib import Path

from knowledge.guideline_pipeline import GuidelinePipeline


pipeline = GuidelinePipeline()

guideline_folder = Path("data/guidelines")

for pdf in sorted(guideline_folder.glob("*.pdf")):

    result = pipeline.process_guideline(
        pdf_path=str(pdf),
        output_directory="processed",
    )

    print()

    print(result)

    print("-" * 80)