import os
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter as filereader, filewriter
import produce_stamps

def get_num_pgs(file_name):
    try:
        with open(file_name, 'rb') as pdf_file:
            reader = filereader(pdf_file)
            return reader.numPages
    except FileNotFoundError:
        print('File not found')
    except Exception as e:
        print('Error getting number of pgs:', e)

def get_exhibit_number(file_name):
    try:
        index = file_name.index('Ex') # Finds the index of the "Ex." part of the file name
        # Finds the exhibit number #
        exhibit = file_name[index:]
        i = 0
        while exhibit[i] != ' ' and not exhibit[i].isnumeric(): # For support of "Ex. 1" and "Ex 1" and "Exhibit 1" and "Exhibit1"
            i += 1
        if exhibit[i].isnumeric(): # Meaning we jumped the gun and found the first digit of the exhibit number
            i -= 1
        ex_num_index = i + 1 # The starting index of the exhibit number in Ex. ### or Ex###
        ex_num = ''
        while ex_num_index < len(exhibit) and exhibit[ex_num_index].isnumeric():
            ex_num += exhibit[ex_num_index]
            ex_num_index += 1
        return ex_num
    except ValueError:
        print('\"Ex\" not found in file name')
    except Exception as e:
        print('Error getting exhibit number:', e)
    
def apply_stamp(file_name):
    try:
        ex_num = get_exhibit_number(file_name)
        num_pgs = get_num_pgs(file_name)
        produce_stamps(ex_num, num_pgs) # TODO: Will create PDF of every stamp with the desired uniform size and orientation
        orig_doc = filereader(open(file_name, 'rb'))
        stamp_doc = filereader(open(f'{ex_num} stamps', 'rb'))
        writer = filewriter()
        # Applies the stamps #
        for i in range(1, num_pgs + 1): # The pg. number part of the Bates stamp
            pg = orig_doc.getPage(i - 1) # Since PyPDF2 starts the pg count at 0
            stamp = stamp_doc.getPage(i - 1)
            pg.mergePage(stamp)
            writer.addPage(pg)
        # Creates and writes to the revised file #
        with open(file_name + ' stamped', 'wb') as modified_ex_file:
            writer.write(modified_ex_file)
        if os.path.isfile(file_name + ' stamped'): # Checks if the new exhibit doc exists
            return True # Successfully stamped the exhibit
        else:
            return False
    except FileNotFoundError:
        print(f'File for {"orig_doc" if orig_doc == None else "stamp_doc"} could not be found')
    except Exception as e:
        print('Error applying stamp:', e)
        
        
        
def main():
    file_name = sys.argv[1]
    stamp_text = apply_stamp(file_name)

main()
