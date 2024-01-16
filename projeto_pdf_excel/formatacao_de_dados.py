import locale
from datetime import datetime

from jinja2 import FileSystemLoader, Environment

from projeto_pdf_excel.processamento_de_dados import carregar_tabelas


def pegar_template_renderizado(
        mes_referencia,
        pasta_dados,
        arquivo_excel,
        pasta_assets,
        arquivo_template,
        arquivo_css,
):
    dict_tabelas = carregar_tabelas(
        mes_referencia=mes_referencia,
        pasta_dados=pasta_dados,
        arquivo_excel=arquivo_excel,
    )
    for nome_tabela, tabela in dict_tabelas.items():
        dict_tabelas[nome_tabela] = tabela.to_html(classes='dataframe', float_format=formatar)

    template = carregar_template(pasta_assets=pasta_assets, arquivo_template=arquivo_template)

    caminho_css = pasta_assets / arquivo_css
    css = carregar_css(caminho_css=caminho_css)

    return renderizar_template_como_html(
        template=template,
        css=css,
        mes_referencia=mes_referencia,
        dict_tabelas=dict_tabelas,
    )


def formatar(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')  # Em windows: 'portuguese-brazilian'
    return locale.currency(valor, grouping=True, symbol=True)


def carregar_template(pasta_assets, arquivo_template):
    loader = FileSystemLoader(pasta_assets)
    environment = Environment(loader=loader)
    template = environment.get_template(arquivo_template)
    return template


def carregar_css(caminho_css):
    with open(caminho_css) as arquivo:
        css = arquivo.read()
    return css


def renderizar_template_como_html(
        template,
        css,
        mes_referencia,
        dict_tabelas,
):
    agora = datetime.now()
    dia = agora.strftime('%d/%m/%Y')
    hora = agora.strftime('%H:%M')
    template_vars = {
        'stylesheet': css,
        'mes_referencia': mes_referencia,
        'dia': dia,
        'hora': hora,
    }
    string_html = template.render(**template_vars, **dict_tabelas)
    return string_html


if __name__ == '__main__':  # Testando o código
    from caminhos import PASTA_DADOS, PASTA_ASSETS
    html = pegar_template_renderizado(
        mes_referencia='2023-01',
        pasta_dados=PASTA_DADOS,
        arquivo_excel='dados.xlsx',
        pasta_assets=PASTA_ASSETS,
        arquivo_template='template.jinja',
        arquivo_css='style.css',
    )
    print(html)
    # Conferir o resultado das linhas abaixo abrindo o arquivo em um navegador
    with open('relatorio.html', 'w') as html_file:
        html_file.write(html)
