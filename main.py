import PyPDF2 as pdf


def read_pdf(filename='10_detection_tracking.pdf'):
    with open(filename, 'rb') as f:
        reader = pdf.PdfFileReader(f)
        paths = []
        for i in range(reader.getNumPages()):
            path = read_page(i, reader)
            if path:
                paths.extend(path)
        return paths


def read_page(n, reader):
    pageObj = reader.getPage(n)
    if not '/Annots' in pageObj.keys(): return
    paths = []
    for obj in pageObj['/Annots']:
        path = obj.getObject()['/A'].get('/F')
        if path:
            paths.append(path)
    return paths


if __name__ == '__main__':
    for video_path in read_pdf():
        print(video_path)
