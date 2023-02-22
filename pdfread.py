import PyPDF2
import os
import pdfplumber
import json
import fitz

def size_check(file):
    size=os.path.getsize(file)
    if(size>5000000):
        print('file size is more than 5Mb')
        exit(0)
    else:
        print('size ok')
        return

def error_check(file):
    try:
        PyPDF2.PdfReader(file)
    except PyPDF2.errors.PdfReadError:
        print('invalid PDF file')
        exit(0)
    else:
        print('no error')
        pass

def empty_check(file):
    reader=PyPDF2.PdfReader(file)
    totalpages = len(reader.pages)
    for i in range(0, totalpages):
        page=reader.pages[i]
        if(page.get_contents()==None):
            print('empty')
            flag=0
        else:
            flag=1
            pass
    if(flag==1):
        print('not empty')
def extract_text(file):
    
    table=[]
    with pdfplumber.open(file) as pdf:
        totalpages = len(pdf.pages)
        for i in range(0, totalpages):
            page = pdf.pages[i]    
            table.append(page.extract_tables(table_settings={"vertical_strategy": "lines", 
                                                    "horizontal_strategy": "lines", 
                                                    "snap_tolerance": 4,}))
        for i in table:
            for j in i:
                for k in j:
                    if k==['', None]:
                        del j[j.index(k)]

        dic={}

        for i in table:
            for j in i:
                for k in j:
                    for l in k:
                        r=k.index(l)
                
                        if l =='':
                            o=k.index(l)
                            dic.update({head:dic[head]+', '+k[0+1]})
                            break
                        else:
                            dic.update({k[r]: k[r+1]})
                            head=k[r]
                            break
        
        with open("text.json", "w") as outfile:
            json.dump(dic, outfile)
    
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
    
file='Delhi_A_2022_10.pdf'
size_check(file)
error_check(file)
empty_check(file)
extract_text(file)
extract_images(file)
