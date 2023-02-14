import PyPDF2
import os
import json
import fitz

def size_check(file):
    size=os.path.getsize(file)
    if(size>5000000):
        print('file size is more than 5Mb')
        exit(0)
    else:
        return

def error_check(file):
    try:
        PyPDF2.PdfReader(file)
    except PyPDF2.errors.PdfReadError:
        print('invalid PDF file')
        exit(0)
    else:
        pass

def empty_check(file):
    reader=PyPDF2.PdfReader(file)
    totalpages = len(reader.pages)
    for i in range(0, totalpages):
        page=reader.pages[i]
        if(page.get_contents()==None):
            print('empty')
        else:
            pass
def extract_text(file):
    reader=PyPDF2.PdfReader(file)
    dictionary={}
    totalpages = len(reader.pages)
    for i in range(0, totalpages):
        page=reader.pages[i]
        pdfData=page.extract_text()
        dictionary={**dictionary,**{'page '+str(i+1):pdfData}}
    with open("text.json", "w") as outfile:
        json.dump(dictionary, outfile)
    
def extract_images(file):
    doc=fitz.open(file)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.save("p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.save("p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None
    
file='sample5.pdf'
size_check(file)
error_check(file)
empty_check(file)
extract_text(file)
extract_images(file)
