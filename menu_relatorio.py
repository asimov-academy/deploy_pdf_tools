import tempfile
from pathlib import Path

import streamlit as st

from projeto_pdf_excel.gerar_relatorio import main as gerar_relatorio_pdf, CONFIG


def exibir_menu_relatorio(coluna):
    """Exibe o menu para gerar um relatório PDF a partir de um arquivo Excel."""
    with coluna:
        st.markdown(
            """
        # Gerar relatório PDF

        Selecione um arquivo Excel para gerar um relatório:
        """
        )
        arquivo_excel = st.file_uploader(
            label="Selecione o arquivo Excel...",
            type='xlsx',
            accept_multiple_files=False,
        )
        if arquivo_excel:
            botoes_desativados = False
        else:
            botoes_desativados = True
        col1, col2 = st.columns(2)
        with col1:
            seletor_ano = st.selectbox('Ano', range(2020, 2024), disabled=botoes_desativados)
        with col2:
            seletor_mes = st.selectbox('Mês', range(1, 13), disabled=botoes_desativados)

        clicou_processar = st.button(
            'Clique para processar o arquivo Excel...',
            disabled=botoes_desativados,
            use_container_width=True,
        )
        if clicou_processar:
            dados_pdf = pegar_dados_do_relatorio_pdf(arquivo_excel, seletor_ano, seletor_mes)
            if dados_pdf is None:
                return
            nome_arquivo = f'relatório.pdf'
            st.download_button(
                'Clique para baixar o arquivo PDF resultante...',
                type='primary',
                data=dados_pdf,
                file_name=nome_arquivo,
                mime='application/pdf',
                use_container_width=True,
            )


def pegar_dados_do_relatorio_pdf(arquivo_excel, seletor_ano, seletor_mes):
    # Configurar mês referência para o relatório
    mes_referencia = f'{seletor_ano}-{seletor_mes:02d}'
    CONFIG['mes_referencia'] = mes_referencia
    # Configurar caminho temporário para os dados Excel
    with tempfile.TemporaryDirectory() as pasta_temp:
        caminho_temp = Path(pasta_temp)
        CONFIG['pasta_dados'] = caminho_temp
        CONFIG['pasta_output'] = caminho_temp
        # Inserir dados Excel na pasta temporária
        with open(caminho_temp / 'dados.xlsx', 'wb') as arq_excel_temp:
            dados_excel = arquivo_excel.getvalue()
            arq_excel_temp.write(dados_excel)
        # Rodar função de relatório
        try:
            gerar_relatorio_pdf(**CONFIG)
        except ValueError:  # Erro gerado quando a data não existe nos dados
            st.warning(f'Sem dados para o mês {mes_referencia}!')
            return
        # st.write(list(caminho_temp.iterdir()))  # Mostrar nome do relatório gerado!
        nome_output = caminho_temp / f'Relatório Mensal - {mes_referencia}.pdf'
        with open(nome_output, 'rb') as relatorio_pdf:
            dados_pdf = relatorio_pdf.read()
    return dados_pdf
