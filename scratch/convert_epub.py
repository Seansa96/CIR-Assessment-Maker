import sys
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from fpdf import FPDF

def epub_to_pdf(epub_path, pdf_path):
    book = epub.read_epub(epub_path)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Try to add Arial or fallback to standard fonts that support unicode if possible.
    # standard FPDF fonts don't support full utf8 out of the box, but we'll try to replace unencodable chars
    pdf.set_font("Helvetica", size=11)
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text = soup.get_text()
            
            # encode to latin-1 and ignore bad chars to avoid FPDF errors with standard fonts
            safe_text = text.encode('latin-1', 'replace').decode('latin-1')
            
            for line in safe_text.split('\n'):
                line = line.strip()
                if line:
                    pdf.multi_cell(0, 5, txt=line)
                    pdf.ln(1)
            pdf.ln(5)
            
    pdf.output(pdf_path)
    print("PDF successfully generated.")

if __name__ == "__main__":
    epub_file = sys.argv[1]
    pdf_file = sys.argv[2]
    epub_to_pdf(epub_file, pdf_file)
