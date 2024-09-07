from docx import Document

class WordFileReader:
    """
    A class to read content from Word (.docx) files.

    Methods:
        read_file(file_path: str) -> str: Reads the content of the specified Word file and returns it as a string.
    """
    def read_file(self, file_path: str) -> str:
        """
        Reads the content of a Word document and returns the text.
        
        Args:
            file_path (str): The path to the Word file to be read.

        Returns:
            str: The extracted text from the Word document, with paragraphs joined by newline characters.
        """
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text])
