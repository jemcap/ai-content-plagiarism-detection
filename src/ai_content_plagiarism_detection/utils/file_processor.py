import PyPDF2

def extract_text_from_file(file_path: str) -> str:
    """Simple text extraction from a file."""
    try:
        if(file_path.endswith('.pdf')):
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        elif(file_path.endswith('.txt')):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return f"Unsupported file type: {file_path.split('.')[-1]}"
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"