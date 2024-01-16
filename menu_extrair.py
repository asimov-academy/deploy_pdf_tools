from pathlib import Path

import pypdf
import streamlit as st

from utilidades import pegar_dados_pdf


def exibir_menu_extrair(coluna):
    """Exibe o menu para extrair uma página de um arquivo PDF."""
    with coluna:
        st.markdown(
            """
        # Extrair página de PDF

        Escolha um arquivo PDF para extrair uma página:
        """
        )

        arquivo_pdf = st.file_uploader(
            label="Selecione o arquivo PDF...",
            type='pdf',
            accept_multiple_files=False,
        )
        if arquivo_pdf:
            botoes_desativados = False
        else:
            botoes_desativados = True

        numero_pagina = st.number_input('Página para extrair', disabled=botoes_desativados, min_value=1)
        clicou_processar = st.button(
            'Clique para processar o arquivo PDF...',
            disabled=botoes_desativados,
            use_container_width=True,
        )
        if clicou_processar:
            dados_pdf = extrair_pagina_pdf(arquivo_pdf=arquivo_pdf, numero_pagina=numero_pagina)
            if dados_pdf is None:  # Problema no processamento, emitir aviso
                st.warning(f'PDF não possui página de número {numero_pagina}!')
            else:  # Processamento correu OK, exibir botão de download
                nome_arquivo = f'{Path(arquivo_pdf.name).stem}_pg{numero_pagina:03d}.pdf'
                st.download_button(
                    'Clique para baixar o arquivo PDF...',
                    type='primary',
                    data=dados_pdf,
                    file_name=nome_arquivo,
                    mime='application/pdf',
                    use_container_width=True,
                )


def extrair_pagina_pdf(arquivo_pdf, numero_pagina):
    # Pegar página
    leitor = pypdf.PdfReader(arquivo_pdf)
    try:
        pagina = leitor.pages[numero_pagina - 1]
    except IndexError:  # O valor de numero_pagina está além do limite de páginas do PDF
        return None
    # Escrever página para PDF temporário e ler os seus dados
    escritor = pypdf.PdfWriter()
    escritor.add_page(pagina)
    dados_pdf = pegar_dados_pdf(escritor=escritor)
    return dados_pdf
