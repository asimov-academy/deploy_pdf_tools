import tempfile
from pathlib import Path

import pypdf
import streamlit as st
from PIL import Image

from utilidades import pegar_dados_pdf


def exibir_menu_imagens(coluna):
    """Exibe o menu para gerar um arquivo PDF contendo múltiplas imagens, uma por página."""
    with coluna:
        st.markdown(
            """
        # Imagens para PDF

        Selecione as imagens para gerar um arquivo PDF com elas:
        """
        )

        imagens = st.file_uploader(
            label="Selecione as imagens que irão para o arquivo PDF...",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,  # Cuidado com ordem de upload!
        )
        if imagens:
            botoes_desativados = False
        else:
            botoes_desativados = True
        clicou_processar = st.button(
            'Clique para processar o arquivo PDF...',
            disabled=botoes_desativados,
            use_container_width=True,
        )
        if clicou_processar:
            dados_pdf = gerar_arquivo_pdf_com_imagens(imagens=imagens)
            nome_arquivo = 'imagens.pdf'
            st.download_button(
                'Clique para baixar o arquivo PDF resultante...',
                type='primary',
                data=dados_pdf,
                file_name=nome_arquivo,
                mime='application/pdf',
                use_container_width=True,
            )


def gerar_arquivo_pdf_com_imagens(imagens):
    # Gerar PDF temporário com imagens
    imagens_pillow = []
    for imagem in imagens:
        dados_imagem = Image.open(imagem)
        if dados_imagem.mode == 'RGBA':  # Remover canal de transparência do PNG, se houver
            dados_imagem = remover_canal_transparencia(imagem=imagem)
        imagens_pillow.append(dados_imagem)
    primeira_imagem = imagens_pillow[0]
    demais_imagens = imagens_pillow[1:]

    with tempfile.TemporaryDirectory() as tempdir:
        nome_arquivo = Path(tempdir) / 'temp.pdf'
        primeira_imagem.save(nome_arquivo, save_all=True, append_images=demais_imagens)
        pdf_imagens = pypdf.PdfReader(nome_arquivo)

    # Passar imagens para um novo PDF em branco, ajustando a dimensão e posicionamento
    escritor = pypdf.PdfWriter()
    for pagina in pdf_imagens.pages:
        pagina_em_branco = escritor.add_blank_page(
            width=pypdf.PaperSize.A4.width,
            height=pypdf.PaperSize.A4.height,
        )
        # Ajuste dimensões
        if pagina.mediabox.top > pagina.mediabox.right:  # Imagem está na vertical
            scale = pagina_em_branco.mediabox.top / pagina.mediabox.top * 0.9
        else:  # Imagem está na horizontal (ou é quadrada)
            scale = pagina_em_branco.mediabox.right / pagina.mediabox.right * 0.9
        # Ajuste posicionamento
        tx = (pagina_em_branco.mediabox.right - pagina.mediabox.right * scale) / 2
        ty = (pagina_em_branco.mediabox.top - pagina.mediabox.top * scale) / 2
        transformation = pypdf.Transformation().scale(scale).translate(tx=tx, ty=ty)
        pagina_em_branco.merge_transformed_page(pagina, transformation, over=True)
    dados_pdf = pegar_dados_pdf(escritor=escritor)
    return dados_pdf


def remover_canal_transparencia(imagem):
    imagem_rgba = Image.open(imagem)
    imagem_rgb = Image.new('RGB', imagem_rgba.size, (255, 255, 255))
    imagem_rgb.paste(imagem_rgba, mask=imagem_rgba.split()[3])
    return imagem_rgb
