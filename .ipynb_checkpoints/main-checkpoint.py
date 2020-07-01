import os
import argparse
from PyPDF2 import PdfFileReader


def read_pdf(filename):
    """
    Reads all video links from a PDF. Only tested for slidedeck PDFs created with PDFLatex.
    :param filename:
    :return:
    """
    with open(filename, 'rb') as f:
        reader = PdfFileReader(f)
        paths = []
        for i in range(reader.getNumPages()):
            path = read_page(i, reader)
            if path:
                paths.extend(path)
        return paths


def read_page(n, reader):
    """
    Given a reader object, reads the video paths from the n'th page
    :param n:
    :param reader:
    :return:
    """
    pageObj = reader.getPage(n)
    if not '/Annots' in pageObj.keys(): return
    paths = []
    for obj in pageObj['/Annots']:
        path = obj.getObject()['/A'].get('/F')
        if path:
            paths.append(path)
    return paths


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Filename', action='store', nargs='*')
    return parser.parse_args()


if __name__ == '__main__':
    """
    User can specify either a pdf, 
    or a path to be read from, 
    or nothing in which case I will process the pdfs in the script's directory. 
    
    All videos in the pdf(s) are printed.
    (verified results on lecture 9 and 10)
    """
    if not parse_args().path:
        path = "."
    else:
        path = parse_args().path[0]

    if path.endswith('.pdf'):
        for video_path in read_pdf(path):
            print(video_path)
    else:
        files = os.listdir(path)
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(path, file)
                for video_path in read_pdf(pdf_path):
                    print(video_path)