from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

fp = open(r'C:\Users\Kenny\Downloads\AI_Football_Prediction_Blueprint_compressed - Muh ihram Syahputra (2).pdf', 'rb')
parser = PDFParser(fp)
doc = PDFDocument(parser)
pages = list(PDFPage.create_pages(doc))
print("Total pages in Muh ihram Blueprint:", len(pages))
fp.close()
