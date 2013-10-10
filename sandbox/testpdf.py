from io import BytesIO
from pdfdocument.document import PDFDocument

def say_hello():
    f = BytesIO()
    pdf = PDFDocument(f)
    pdf.init_report()
    pdf.h1('Hello World')
    pdf.p('Creating PDFs made easy.')
    pdf.generate()
    return f.getvalue()

if __name__ == "__main__":
    say_hello()
