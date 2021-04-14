from PIL import Image
import pytesseract

def process_image(iamge_name, lang_code):
	return pytesseract.image_to_string(Image.open(iamge_name), lang=lang_code)

def print_data(data):
	print(data)

def output_file(filename, data):
	file = open(filename, "w+")
	file.write(data)
	file.close()

def main():
	data_spa = process_image("test_spa.png", "spa")
	print_data(data_spa)
	output_file("spa.txt", data_spa)

if  __name__ == '__main__':
	main()