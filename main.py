import argparse
import os
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
import PyPDF2
import pandas as pd

BUFFER_DIR = "/home/jhari/scripts/pdofile/buffer/" # Change this to your desired buffer directory
EPILOG ="""
pdfops is a command line application that can be used to perform operations on PDF files and images.
The application can perform the following operations:
    -- Convert images to PDF and vice versa
    -- Merge multiple PDF files into a single PDF file
    -- Split a PDF file into multiple PDF files
    -- Add Table of Contents to a PDF file
    
Hence the operations are are divided into 4 categories:
    -- convert      : Convert images to PDF and vice versa
    -- merge        : Merge multiple PDF files into a single PDF file
    -- split        : Split a PDF file into multiple PDF files
    -- add_TOC      : Add Table of Contents to a PDF file

During Usage we first provide the operation to perform using the '-p' or '--operation' argument. The operation can be any of the 
4 categories mentioned above. 

CONVERT OPERATION:
    We have 3 conversion choices for the 'convert' operation:
        -- jpg2pdf : Convert jpg image files to a pdf file
        -- png2pdf : Convert png image files to a pdf file
        -- pdf2jpg : Convert a pdf file to jpg image files
    
    IMAGE TO PDF CONVERSION:
        Usage: 
pdfops -p convert -c jpg2pdf <or> png2pdf -id </path/to/input/directory> -of </path/to/output/file.pdf>
        
        We provide the input directory containing the image files using the '-id' or '--in_direc' argument.
        After which we also input the output file name to save the PDF using the '-of' or '--out_file' argument.
        
        The converted PDF file will be saved under the name of the output file.

    PDF TO IMAGE CONVERSION:
        Usage: 
pdfops -p convert -c pdf2jpg -if </path/to/input/file.pdf> -od </path/to/output/directory> [-sn <starting_number>]

        We provide the input file to convert using the '-if' or '--in_file' argument.
        After which we provide the output directory name to save the images using the '-od' or '--out_direc' argument.

        We also have a starting number for the output images using the '-sn' or '--str_num' argument. This is optional
        and will save the images starting from the provided number. If not provided, the images will be saved starting from 0.
        The converted images will be saved in the output directory. If the output directory does not exist, it will be created.

        The names of the saved/created images will be in the format 001.jpg, 002.jpg, 003.jpg, etc, in the output directory.
    
MERGE OPERATION:
    Usage: 
pdfops -p merge -id </path/to/input/directory> -of </path/to/output/file.pdf>

    Provided the input directory containing the PDF files to merge using the '-id' or '--in_direc' argument,
    and the output file name to save the merged PDF using the '-of' or '--out_file' argument, the application
    outputs the merged PDF file.     

SPLIT OPERATION:
    Usage: 
pdfops -p split -if </path/to/input/file.pdf> -od </path/to/output/directory> -sp <split_number>    

    Provided the input file to split using the '-if' or '--in_file' argument, the output directory to save the
    split PDF files using the '-od' or '--out_direc' argument, and the number of pages to split the PDF file using
    the '-sp' or '--split_pg' argument, the application splits the PDF file into multiple PDF files.

    The split PDF files will be saved in the output directory with names like split_001-010.pdf, split_011-020.pdf, etc.
    if the given split number is 10.

ADD_TOC OPERATION:
    Usage: 
pdfops -p add_TOC -if </path/to/input/file.pdf> -toc </path/to/TOC.csv> -of </path/to/output/file.pdf>

    Provided the input file to add Table of Contents using the '-if' or '--in_file' argument, the CSV file containing the
    Table of Contents using the '-toc' or '--toc_csv' argument, and the output file name to save the PDF with Table of Contents
    using the '-of' or '--out_file' argument, the application adds the Table of Contents to the PDF file through its metadata.

    The CSV file should contain the following columns:
        -- Title :  The title of the section
        -- Level :  The level of the section in the Table of Contents: a number from 1 to 9, 1 meaning the Section, 
                    2 meaning subsection, and so on.
        -- Page  :  The page number where the section starts

    The Table of Contents is added to the PDF file and saved with the provided output file name.

The application can be used to perform the above operations on the PDF files and images.
"""
def convert_jpg_to_pdf(folder_path, out_file):

    files = [f for f in sorted(os.listdir(folder_path)) if f.endswith(".jpg")]
    images = []
    max_width = 2667
    pdf_files = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        image = Image.open(file_path)
        images.append(image)
        if len(images) == 60:

            for i in range(len(images)):
                width, height = images[i].size
                aspect_ratio = height / width
                new_height = int(aspect_ratio * max_width)
                images[i] = images[i].resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            output_pdf = os.path.join(BUFFER_DIR, "combined" + str(len(pdf_files)) + ".pdf")
            images[0].save(output_pdf, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
            pdf_files.append(output_pdf)
            images = []
    
    if len(images) > 0:
        for i in range(len(images)):
            width, height = images[i].size
            aspect_ratio = height / width
            new_height = int(aspect_ratio * max_width)
            images[i] = images[i].resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        output_pdf = os.path.join(BUFFER_DIR, "combined" + str(len(pdf_files)) + ".pdf")
        images[0].save(output_pdf, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
        pdf_files.append(output_pdf)

    pdf_merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        pdf_merger.append(pdf_file)
    pdf_merger.write(out_file)
    pdf_merger.close()
    os.system(f"rm {BUFFER_DIR}combined*.pdf")

    print(f"JPG files converted and saved as PDF in '{out_file}' file.")


def convert_png_to_pdf(folder_path, out_file):
    files = [f for f in sorted(os.listdir(folder_path)) if f.endswith(".png")]
    images = []
    max_width = 2667
    pdf_files = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        image = Image.open(file_path)
        images.append(image)
        if len(images) == 60:
            for i in range(len(images)):
                width, height = images[i].size
                aspect_ratio = height / width
                new_height = int(aspect_ratio * max_width)
                images[i] = images[i].resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            output_pdf = os.path.join(BUFFER_DIR, "combined" + str(len(pdf_files)) + ".pdf")
            images[0].save(output_pdf, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
            pdf_files.append(output_pdf)
            images = []
    if len(images) > 0:
        for i in range(len(images)):
            width, height = images[i].size
            aspect_ratio = height / width
            new_height = int(aspect_ratio * max_width)
            images[i] = images[i].resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        output_pdf = os.path.join(BUFFER_DIR, "combined" + str(len(pdf_files)) + ".pdf")
        images[0].save(output_pdf, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
        pdf_files.append(output_pdf)
    
    pdf_merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        pdf_merger.append(pdf_file)
    pdf_merger.write(out_file)
    pdf_merger.close()
    os.system(f"rm {BUFFER_DIR}combined*.pdf")

    print(f"PNG files converted and saved as PDF in '{out_file}' file.")

def convert_pdf_to_jpg(pdf_path, output_dir, j):

    os.makedirs(output_dir, exist_ok=True)

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for i in range(num_pages):
            images = convert_from_path(pdf_path, first_page=i+1, last_page=i+1)
            for image in images:
                image_path = os.path.join(output_dir, f"{str(i+j).zfill(3)}.jpg")
                image.save(image_path, 'JPEG')

def merge_pdf_files(folder_path, out_file):

    files = [f for f in sorted(os.listdir(folder_path)) if f.endswith(".pdf")]
    merger = PdfMerger()
    for file in files:
        file_path = os.path.join(folder_path, file)
        merger.append(file_path)

    with open(out_file, "wb") as f:
        merger.write(f)
    
    print(f"PDF files merged and saved as '{out_file}' file.")

def split_pdf(pdf_path, output_dir, split_pg):

    os.makedirs(output_dir, exist_ok=True)
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        if split_pg < 1 or split_pg > total_pages:
            print("Invalid page number to split the PDF.")
            return
        
        pdf_writer1 = PyPDF2.PdfWriter()
        pdf_writer2 = PyPDF2.PdfWriter()
        
        for i in range(split_pg):
            pdf_writer1.add_page(pdf_reader.pages[i])
        
        for i in range(split_pg, total_pages):
            pdf_writer2.add_page(pdf_reader.pages[i])
        
        output_pdf1 = os.path.join(output_dir, f"part1_000-{str(split_pg).zfill(3)}.pdf")
        output_pdf2 = os.path.join(output_dir, f"part2_{str(split_pg+1).zfill(3)}-{str(total_pages).zfill(3)}.pdf")
        
        with open(output_pdf1, 'wb') as output_file1:
            pdf_writer1.write(output_file1)
        
        with open(output_pdf2, 'wb') as output_file2:
            pdf_writer2.write(output_file2)
    
    print(f"PDF file split into two parts at page {split_pg} and saved in '{output_dir}' directory.")
    return

def add_toc(pdf_path, toc, out_file):
    os.system(f"pdftk {pdf_path} dump_data output {BUFFER_DIR}metadata.txt")

    with open(f"{BUFFER_DIR}metadata.txt", "r") as file:
        metadata = file.read()

    for line_num, line in enumerate(metadata.split("\n")):
        if "NumberOfPages" in line:
            start = line_num
            break

    with open(f"{BUFFER_DIR}metadata_new.txt", "w") as file:

        for i in range(len(toc)):
            file.write(f"BookmarkBegin\n")
            file.write(f"BookmarkTitle: {toc['Title'][i]}\n")
            file.write(f"BookmarkLevel: {toc['Level'][i]}\n")
            file.write(f"BookmarkPageNumber: {toc['Page'][i]}\n")

    with open(f"{BUFFER_DIR}metadata.txt", "r") as file:
        metadata = file.readlines()
    with open(f"{BUFFER_DIR}metadata_new.txt", "r") as file:
        metadata_new = file.readlines()
    metadata[start+1:start+1] = metadata_new
    with open(f"{BUFFER_DIR}metadata_newer.txt", "w") as file:
        file.writelines(metadata)

    os.system(f"pdftk {pdf_path} update_info {BUFFER_DIR}metadata_newer.txt output {out_file} 2> /dev/null")

    os.remove(f"{BUFFER_DIR}metadata.txt")
    os.remove(f"{BUFFER_DIR}metadata_new.txt")
    os.remove(f"{BUFFER_DIR}metadata_newer.txt")
    
    print(f"Table of Contents added to the PDF file and saved as '{out_file}' file.")

def main():

    parser = argparse.ArgumentParser(usage="main.py [--help] --operation operation [--conv_c conv_c] [--in_direc in_direc] [--out_direc out_direc] [--in_file in_file] [--out_file out_file] [--str_num str_num] [--split_pg split_pg] [--toc_csv toc_csv]",
                                      description="PDF Editor, Maker and Converter",
                                      formatter_class=argparse.RawTextHelpFormatter,
                                      epilog=EPILOG)

    parser.add_argument("-p",
                        "--operation",
                        type=str,
                        required=True,
                        choices=["convert", "merge", "split", "add_TOC"],
                        help="Operation to perform using the application")
    
    parser.add_argument("-c",
                        "--conv_c",
                        type=str,
                        choices=["jpg2pdf", "pdf2jpg", "png2pdf"],
                        help="Conversion choice for the 'convert' operation")

    parser.add_argument("-id",
                        "--in_direc",
                        type=str,
                        help="Input directory containing the files to process")

    parser.add_argument("-od",
                        "--out_direc",
                        type=str,
                        help="Output directory to save the processed files")

    parser.add_argument("-if",
                        "--in_file",
                        type=str,
                        help="Input file to process")
    
    parser.add_argument("-of",
                        "--out_file",
                        type=str,
                        help="Output file to save the processed file")
    
    parser.add_argument("-sn",
                        "--str_num",
                        type=int,
                        default=0,
                        help="Starting number for the output images if converting PDF to JPG")

    parser.add_argument("-sp",
                        "--split_pg",
                        type=int,
                        help="Number of pages to split the PDF file")

    parser.add_argument("-toc",
                        "--toc_csv",
                        type=str,
                        help="CSV file containing the Table of Contents")

    args = parser.parse_args()

    if args.operation == "convert":
        if not args.conv_c:
            print("Please provide the conversion choice.\n\nPlease choose 'jpg2pdf', 'png2pdf', or 'pdf2jpg'.")
            return
        if args.conv_c == "jpg2pdf":
            if not args.in_direc:
                print("Please provide the input directory containing the JPG files.")
                return
            if not args.out_file:
                print("Please provide the output file to save the PDF.")
                return
            convert_jpg_to_pdf(args.in_direc, args.out_file)

        elif args.conv_c == "png2pdf":
            if not args.in_direc:
                print("Please provide the input directory containing the JPG files.")
                return
            if not args.out_file:
                print("Please provide the output file to save the PDF.")
                return
            convert_png_to_pdf(args.in_direc, args.out_file)

        elif args.conv_c == "pdf2jpg":
            if not args.in_file:
                print("Please provide the input file to convert.")
                return
            if not args.out_direc:
                print("Please provide the output directory to save the JPEG images.")
                return
            if not args.str_num:
                args.str_num = 0
            convert_pdf_to_jpg(args.in_file, args.out_direc, args.str_num)

        else:
            print("Invalid conversion choice.\n\nPlease choose 'jpg2pdf', 'png2pdf', or 'pdf2jpg'.")
            return
    
    elif args.operation == "merge":
        if not args.in_direc:
            print("Please provide the input directory containing the PDF files to merge.")
            return
        if not args.out_file:
            print("Please provide the output file to save the merged PDF.")
            return
        merge_pdf_files(args.in_direc, args.out_file)

    elif args.operation == "split":
        if not args.in_file:
            print("Please provide the input file to split.")
            return
        if not args.out_direc:
            print("Please provide the output directory to save the split PDF files.")
            return
        if not args.split_pg:
            print("Please provide the number of pages to split the PDF file.")
            return 
        split_pdf(args.in_file, args.out_direc, args.split_pg)

    elif args.operation == "add_TOC":
        if not args.in_file:
            print("Please provide the input file to add Table of Contents.")
            return
        if not args.toc_csv:
            print("Please provide the CSV file containing the Table of Contents.")
            return
        if not args.out_file:
            print("Please provide the output file to save the PDF with Table of Contents.")
            return

        toc = pd.read_csv(args.toc_csv, header=0)
        add_toc(args.in_file, toc, args.out_file)

    else:
        print("Invalid operation choice.\n\nPlease choose 'convert', 'merge', 'split', or 'add_TOC'.")
        return

if __name__ == "__main__":
    main()