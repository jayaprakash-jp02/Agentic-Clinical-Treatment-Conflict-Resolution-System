print("Program Started")

from knowledge.pdf_loader import load_pdf

print("Import Successful")

text = load_pdf("data/ADA_Guideline.pdf")

print("PDF Loaded Successfully")
print(type(text))
print(text[:500])

print("Program Finished")