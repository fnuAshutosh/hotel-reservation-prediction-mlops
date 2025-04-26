# Script to convert requirements.txt from UTF-16 to UTF-8 encoding

def convert_file_encoding(input_file, output_file):
    with open(input_file, 'rb') as f:
        content = f.read()
    # Decode as UTF-16 (common for BOM 0xff 0xfe)
    text = content.decode('utf-16')
    # Write back as UTF-8 without BOM
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    convert_file_encoding('requirements.txt', 'requirements.txt')
