# -*- coding: utf-8 -*-

from pyPdf import PdfFileWriter, PdfFileReader

def concatPDFs(output_file, input_files):
    print "concat all files:"

    output = PdfFileWriter()
    total_pages = 0
    for f in input_files:
        # expect filename as "*.pdf"
        if f[-4:] != ".pdf":
            print "skipped file: ", f
            continue
        else:
            inputPDF = PdfFileReader(file(f, 'rb'))
            num_pages = inputPDF.getNumPages()
            total_pages += num_pages
            print f, "->", str(num_pages) + "pages"
            for i in xrange(0, num_pages):
                output.addPage(inputPDF.getPage(i))
       
    outputStream = file(output_file, 'wb')
    output.write(outputStream)
    print total_pages, "pages written"
    outputStream.close()

def gen4in1Book(output_file, input_files):
    print "generate 4in1 book:"
    output = PdfFileWriter()
    inputPDF = PdfFileReader(file(input_files, 'rb'))
    n_page_src = inputPDF.getNumPages()
    
    # 1. Align pages w/ blank pages
    n_paper_dst = n_page_src / 8
    if ((n_page_src % 8)!=0):
        n_paper_dst += 1
    
    n_page_dst = n_paper_dst * 8
    n_page_blank = n_page_dst - n_page_src
    
    # 2. Create FourPlane
    four_plane = []
    four_plane.append([])
    four_plane.append([])
    four_plane.append([])
    four_plane.append([])
    n_four_plane = n_paper_dst*2
    for j in xrange(0,4):
        for i in xrange(1+j*n_four_plane, (j+1)*n_four_plane+1):
            four_plane[j].append(i)
    
    # 3. Create Ordered 4 Plane
    four_plane[1].reverse()
    four_plane[3].reverse()
    
    # 4.1 Create Output Pages
    output_pages = []
    for i in range(0,len(four_plane[0])):
        created_page = []
        for plane in range(0,4):
            created_page.append(four_plane[plane][i])
        
        output_pages.append(created_page)
    
    # 4.2 Order in 4132(odd) or 1423(even)
    for i in xrange(0,len(output_pages)):
        if i%2: # odd -> 1423 order
            output_pages[i].insert(1, output_pages[i].pop(3))
        else: # even -> 4132 order
            output_pages[i].insert(0, output_pages[i].pop(3))
            output_pages[i].insert(3, output_pages[i].pop(2))
    
    # 5. Compose actual PDF pages
    for i in xrange(0,len(output_pages)):
        for j in xrange(0,4):
            pdf_page = inputPDF.getPage(output_pages[i][j]-1)
            if (j >= 2):
                pdf_page.rotateClockwise(180)
            output.addPage(pdf_page)
    
    #print "end"    
    outputStream = file(output_file, 'wb')
    output.write(outputStream)
    outputStream.close()


if __name__ == '__main__':
    import argparse
    description = "This program orders input PDF files in 4in1-2sided-book order."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-o", "--output", default="output.pdf")
    parser.add_argument("-i", "--input", nargs='*', required=True)
    parser.add_argument("-v", "--version", action='version',
                        version="%(prog)s 1.0")
    args = vars(parser.parse_args())
    
    print "****** start concatination ******"
    #concatPDFs(args['output'], args['input'])
    gen4in1Book(args['output'], args['input'])
    