# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, Katsuya Iwata <iwata.katsuya@gmail.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__author__ = "Katsuya Iwata"
__author_email__ = "iwata.katsuya@gmail.com"

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
    print "****** Completed (^-^)b - 4in1 book generation ******"
