from pypdf import PdfReader


reader = PdfReader("rag_paper.pdf")
print(f"Number of pages: {len(reader.pages)}")

for i range(len(reader.pages)):

   text = reader.pages[1].extract_text()
print(text)