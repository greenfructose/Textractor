import sys, getopt, csv

from PIL import Image
import pytesseract

IMAGE_TEXT = ''
ROW_DATA = []
IMAGE_PATH = ''
OUTPUT_FILE = 'output.csv'

def set_image_text():
    global IMAGE_TEXT
    global IMAGE_PATH
    if IMAGE_PATH:
        IMAGE_TEXT = pytesseract.image_to_string(Image.open(IMAGE_PATH), lang='eng', config='--psm 6')
    else:
        IMAGE_TEXT = 'No image path provided. Please provide an image path.'

def get_image_text() -> str:
    return IMAGE_TEXT

def parse_image_text():
    for line in get_image_text().split('\n'):
        line = str(line.strip())
        line = line.replace(')', '')
        if line:
            data = line.split(' ')
            add_row_data(data)

def set_image_path(path: str):
    global IMAGE_PATH
    if path:
        IMAGE_PATH = path

def get_image_path() -> str:
    return IMAGE_PATH

def set_output_file(path: str):
    global OUTPUT_FILE
    if path:
        OUTPUT_FILE = path

def get_output_file() -> str:
    return OUTPUT_FILE

def add_row_data(row: list):
    global ROW_DATA
    ROW_DATA.append(row)

def get_row_data() -> list:
    return ROW_DATA

def write_to_csv():
    global ROW_DATA
    with open(get_output_file(), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(get_row_data())

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["image=", "output="])
    except getopt.GetoptError:
        print('table_from_image.py -i <image_path> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('table_from_image.py -i <image_path> -o <output_file>')
            sys.exit()
        elif opt in ("-i", "--image"):
            set_image_path(arg)
        elif opt in ("-o", "--output"):
            set_output_file(arg)
    set_image_text()
    parse_image_text()
    write_to_csv()

if __name__ == '__main__':
    main(sys.argv[1:])