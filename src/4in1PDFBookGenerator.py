# -*- coding: utf-8 -*-

from pyPdf import PdfFileWriter, PdfFileReader

def gen4in1Book(output_file, input_file, layout):
    if input_file[-4:] != ".pdf":
        print "Designated input file is not in PDF. This input file must be in PDF."
        exit()
    
    inputPDF = PdfFileReader(file(input_file, 'rb'))
    blankPagePDF = PdfFileReader(file("./SmileBlankPage.pdf", 'rb'))
    output = PdfFileWriter()
    
    n_page_src = inputPDF.getNumPages()
    
    # 1. Align pages w/ blank pages
    n_paper_dst = n_page_src / 8
    if ((n_page_src % 8)!=0):
        n_paper_dst += 1
    
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
    
    # 4.2 Order in 4132(odd) or 1423(even) for Z, 4312(odd) or 1243(even) for N
    for i in xrange(0,len(output_pages)):
        if i%2: # odd -> 1423 order
            if layout=="Z":
                output_pages[i].insert(1, output_pages[i].pop(3))
            else:
                output_pages[i].insert(2, output_pages[i].pop(3))
        else: # even -> 4132 order
            if layout=="Z":
                output_pages[i].insert(0, output_pages[i].pop(3))
                output_pages[i].insert(3, output_pages[i].pop(2))
            else:
                output_pages[i].insert(0, output_pages[i].pop(2))
                output_pages[i].insert(0, output_pages[i].pop(3))
    
    # 5. Compose actual PDF pages
    for i in xrange(0,len(output_pages)):
        for j in xrange(0,4):
            p = output_pages[i][j]-1
            if (p > n_page_src - 1):
                output.addPage(blankPagePDF.getPage(0))
            else:
                pdf_page = inputPDF.getPage(p)
                if (layout=="Z"):
                    if (j >= 2):
                        pdf_page.rotateClockwise(180)
                else:
                    if (j%2):
                        pdf_page.rotateClockwise(180)
                
                output.addPage(pdf_page)
    
    outputStream = file(output_file, 'wb')
    output.write(outputStream)
    outputStream.close()
    print "****** Completed (^-^)b ******"

if __name__ == '__main__':
    import argparse
    description = "This program orders PDF pages in 4in1-2sided-book order."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-o", "--output", default="./Output4in1Book.pdf", help="(default=./Output4in1Book.pdf) set an output file. Example: -o ./output.pdf")
    parser.add_argument("-i", "--input", required=True, help="(Required) set an input file. Example: -i ./input.pdf")
    parser.add_argument("-l", "--layout", default="Z", help="(default=Z) Value must be Z or u. Set print order in one 4 in 1 page. Example: -l Z")
    parser.add_argument("-v", "--version", action='version', version="%(prog)s 1.0")
    args = vars(parser.parse_args())
    
    print "****** Start - 4in1 book generation ******"
    gen4in1Book(args['output'], args['input'], args['layout'])
    print "****** End - 4in1 book generation ******"
    