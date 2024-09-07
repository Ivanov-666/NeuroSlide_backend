from docx import Document

class WordFileReader:
    def read_file(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text])
