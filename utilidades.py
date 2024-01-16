import tempfile
from pathlib import Path


def pegar_dados_pdf(escritor):
    """Recebe um PDFWriter, escreve seu conteúdo para um arquivo temporário,
    e retorna o conteúdo do PDF como bytes.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_pdf_file = Path(temp_dir) / 'temp.pdf'
        escritor.write(temp_pdf_file)
        with open(temp_pdf_file, 'rb') as output_pdf:
            pdf_data = output_pdf.read()
    return pdf_data
