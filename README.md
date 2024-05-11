# pdfops
```
usage: main.py [--help] --operation operation [--conv_c conv_c] [--in_direc in_direc] [--out_direc out_direc]
[--in_file in_file] [--out_file out_file] [--str_num str_num] [--split_pg split_pg] [--toc_csv toc_csv]

PDF Editor, Maker and Converter

options:
  -h, --help            show this help message and exit
  -p {convert,merge,split,add_TOC}, --operation {convert,merge,split,add_TOC}
                        Operation to perform using the application
  -c {jpg2pdf,pdf2jpg,png2pdf}, --conv_c {jpg2pdf,pdf2jpg,png2pdf}
                        Conversion choice for the 'convert' operation
  -id IN_DIREC, --in_direc IN_DIREC
                        Input directory containing the files to process
  -od OUT_DIREC, --out_direc OUT_DIREC
                        Output directory to save the processed files
  -if IN_FILE, --in_file IN_FILE
                        Input file to process
  -of OUT_FILE, --out_file OUT_FILE
                        Output file to save the processed file
  -sn STR_NUM, --str_num STR_NUM
                        Starting number for the output images if converting PDF to JPG
  -sp SPLIT_PG, --split_pg SPLIT_PG
                        Number of pages to split the PDF file
  -toc TOC_CSV, --toc_csv TOC_CSV
                        CSV file containing the Table of Contents

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

During Usage we first provide the operation to perform using the '-p' or '--operation' argument. The operation
can be any of the 4 categories mentioned above. 

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
        and will save the images starting from the provided number. If not provided, the images will be saved starting
        from 0. The converted images will be saved in the output directory. If the output directory does not exist,
        it will be created.

        The names of the saved/created images will be in the format 001.jpg, 002.jpg, 003.jpg, etc, in the output
        directory.
    
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
    split PDF files using the '-od' or '--out_direc' argument, and the number of pages to split the PDF file
    using the '-sp' or '--split_pg' argument, the application splits the PDF file into multiple PDF files.

    The split PDF files will be saved in the output directory with names like split_001-010.pdf,
    split_011-020.pdf, etc., if the given split number is 10.

ADD_TOC OPERATION:
    Usage: 
pdfops -p add_TOC -if </path/to/input/file.pdf> -toc </path/to/TOC.csv> -of </path/to/output/file.pdf>

    Provided the input file to add Table of Contents using the '-if' or '--in_file' argument, the CSV file
    containing the Table of Contents using the '-toc' or '--toc_csv' argument, and the output file name to
    save the PDF with Table of Contents using the '-of' or '--out_file' argument, the application adds the
    Table of Contents to the PDF file through its metadata.

    The CSV file should contain the following columns:
        -- Title :  The title of the section
        -- Level :  The level of the section in the Table of Contents: a number from 1 to 9, 1 meaning the
                    Section, 2 meaning subsection, and so on.
        -- Page  :  The page number where the section starts

    The Table of Contents is added to the PDF file and saved with the provided output file name.

The application can be used to perform the above operations on the PDF files and images.
```
Add the line `alias pdfops='py /path/to/main.py/on/your/pc>'` and do not forget to edit the `BUFFER_DIR`
variable in the file to the current buffer directory.

The application works flawlessly on Linux.

