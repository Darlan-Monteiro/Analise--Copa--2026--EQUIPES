from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup


def extrair_nome_limpo(tag_nome):
    """
    Extrai apenas o nome do jogador/equipe
    """
    if tag_nome is None:
        return None

    texto_direto = tag_nome.find(text=True, recursive=False)
    if texto_direto and texto_direto.strip():
        return texto_direto.strip()

    texto_completo = tag_nome.get_text(separator="|", strip=True)
    if texto_completo:
        return texto_completo.split("|")[0].strip()

    return None


def contar_linhas_tabela_visivel(pagina):
    
    return pagina.evaluate("""() => {
        let tables = document.querySelectorAll('table');
        let visiveis = Array.from(tables).filter(t => t.offsetParent !== null);
        if (visiveis.length === 0) return 0;
        let tbody = visiveis[0].querySelector('tbody');
        if (!tbody) return 0;
        return tbody.querySelectorAll('tr').length;
    }""")


def clicar_load_more_ate_fim(pagina, cat, max_cliques=200):
    cliques = 0

    while cliques < max_cliques:
        
        botao = pagina.get_by_role("button", name="Load more")
        if botao.count() == 0:
            botao = pagina.get_by_role("button", name="Carregar mais")
        if botao.count() == 0:
            botao = pagina.get_by_text("Load more", exact=False).filter(visible=True)
        if botao.count() == 0:
            botao = pagina.get_by_text("Carregar mais", exact=False).filter(visible=True)

        if botao.count() == 0:
            break  

        try:
            if not botao.first.is_visible():
                break
        except Exception:
            break

        linhas_antes = contar_linhas_tabela_visivel(pagina)

        try:
            botao.first.scroll_into_view_if_needed(timeout=5000)
            botao.first.click(timeout=5000)
        except Exception:
            try:
                botao.first.evaluate("node => node.click()")
            except Exception as e:
                print(f"Erro ao clicar em 'Load more' ({e})")
                break

        tentativas = 0
        carregou = False
        while tentativas < 20:
            pagina.wait_for_timeout(500)
            linhas_depois = contar_linhas_tabela_visivel(pagina)
            if linhas_depois > linhas_antes:
                carregou = True
                break
            tentativas += 1

        cliques += 1

        if not carregou:
            break

    return cliques


def extrair_dados_tabela_atual(pagina):
    html_atual = pagina.evaluate("""() => {
        let tables = document.querySelectorAll('table');
        let visiveis = Array.from(tables).filter(t => t.offsetParent !== null);
        return visiveis.length > 0 ? visiveis[0].outerHTML : '';
    }""")

    if not html_atual:
        return None

    df_temp = pd.read_html(StringIO(html_atual))[0]

    sopa = BeautifulSoup(html_atual, 'html.parser')
    corpo_tabela = sopa.find('tbody')
    linhas = corpo_tabela.find_all('tr') if corpo_tabela else [
        tr for tr in sopa.find_all('tr') if not tr.find('th')
    ]

    links_imagens = []
    nomes_limpos = []

    for tr in linhas:
        imagem = tr.find('img')
        if imagem and imagem.has_attr('src'):
            links_imagens.append(imagem['src'])
        else:
            links_imagens.append("Sem Imagem")

        celulas = tr.find_all('td')
        tag_nome = celulas[1] if len(celulas) > 1 else None
        nomes_limpos.append(extrair_nome_limpo(tag_nome))

    if len(links_imagens) == len(df_temp):
        df_temp['URL_Imagem'] = links_imagens

    if len(nomes_limpos) == len(df_temp) and any(nomes_limpos):
        col_nome = df_temp.columns[1] if len(df_temp.columns) > 1 else None
        if col_nome is not None:
            df_temp[col_nome] = nomes_limpos

    return df_temp


def extrair_tabelas(pagina, categorias, nome_etapa):
    tabelas = {}

    for idx, cat in enumerate(categorias):
        html_anterior = ""
        if idx > 0:
            html_anterior = pagina.evaluate("""() => {
                let tables = document.querySelectorAll('table');
                let visiveis = Array.from(tables).filter(t => t.offsetParent !== null);
                return visiveis.length > 0 ? visiveis[0].outerHTML : '';
            }""")

        # Localiza o botão da categoria
        botoes = pagina.get_by_role("button", name=cat, exact=True)
        if botoes.count() == 0:
            botoes = pagina.get_by_text(cat, exact=True).filter(visible=True)

        if botoes.count() == 0:
            continue

        try:
            botoes.first.click(timeout=5000)
        except Exception as e:
            try:
                botoes.first.evaluate("node => node.click()")
            except Exception as e2:
                continue

        try:
            pagina.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass

        tentativas = 0
        sucesso = False

        while tentativas < 30:
            pagina.wait_for_timeout(500)

            html_atual = pagina.evaluate("""() => {
                let tables = document.querySelectorAll('table');
                let visiveis = Array.from(tables).filter(t => t.offsetParent !== null);
                return visiveis.length > 0 ? visiveis[0].outerHTML : '';
            }""")

            if html_atual:
                try:
                    df_check = pd.read_html(StringIO(html_atual))[0]
                    if idx == 0:
                        if len(df_check) > 0:
                            sucesso = True
                            break
                    else:
                        if html_atual != html_anterior and len(df_check) > 0:
                            sucesso = True
                            break
                except Exception:
                    pass

            tentativas += 1

        if not sucesso:
            
            try:
                caminho_print = f"debug_falha_{nome_etapa}_{cat}.png".replace(" ", "_")
                pagina.screenshot(path=caminho_print)
            
            except Exception:
                pass
            continue

     
        cliques = clicar_load_more_ate_fim(pagina, cat)
     
        try:
            df_atual = extrair_dados_tabela_atual(pagina)
        except Exception as e:
            df_atual = None
            continue

        if df_atual is not None and len(df_atual) > 0:
            tabelas[cat] = df_atual
         
        else:
            print(f"Falha ao extrair dados da aba '{cat}'.")
    return tabelas


def iniciar_automacao():
    categorias_equipes = ["Ataque", "Distribuição", "Defesa", "Disciplina", "Goleiro", "Movimentação", "Físico"]
    categorias_jogadores = ["O Artilheiro", "Ataque", "Distribuição", "Defesa", "Disciplina", "Goleiro", "Movimentação", "Físico"]

    with sync_playwright() as p:
    
        navegador = p.chromium.launch(headless=False)
        pagina = navegador.new_page()

        pagina.goto("https://www.fifa.com/pt/tournaments/mens/worldcup/canadamexicousa2026/statistics/team-statistics", wait_until="domcontentloaded")
        pagina.wait_for_timeout(3000)
        tabelas_equipes = extrair_tabelas(pagina, categorias_equipes, "Equipes")

        pagina.goto("https://www.fifa.com/pt/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics", wait_until="domcontentloaded")
        pagina.wait_for_timeout(3000)
        tabelas_jogadores = extrair_tabelas(pagina, categorias_jogadores, "Jogadores")

        navegador.close()

    # pra salvar o xlsx das equipes
    if tabelas_equipes:
        mapa_ids = {}
        cont_id = 1
        with pd.ExcelWriter("Estatisticas_Equipes_Copa_2026.xlsx", engine='openpyxl') as writer:
            for nome_aba, df in tabelas_equipes.items():
                col_time = df.columns[0]
                ids = []
                for time_nome in df[col_time]:
                    nome_limpo = str(time_nome).strip()
                    if nome_limpo not in mapa_ids:
                        mapa_ids[nome_limpo] = cont_id
                        cont_id += 1
                    ids.append(mapa_ids[nome_limpo])
                df.insert(0, 'ID_Equipe', ids)
                df.to_excel(writer, sheet_name=nome_aba, index=False)

    # pra salvar o xlsx dos jogadores
    if tabelas_jogadores:
        mapa_ids = {}
        cont_id = 1
        with pd.ExcelWriter("Estatisticas_Jogadores_Copa_2026.xlsx", engine='openpyxl') as writer:
            for nome_aba, df in tabelas_jogadores.items():
                col_jogador = next((col for col in df.columns if "Jogador" in str(col)), df.columns[1] if len(df.columns) > 1 else None)
                ids = []
                if col_jogador:
                    for jogador_nome in df[col_jogador]:
                        nome_limpo = str(jogador_nome).strip()
                        if nome_limpo not in mapa_ids:
                            mapa_ids[nome_limpo] = cont_id
                            cont_id += 1
                        ids.append(mapa_ids[nome_limpo])
                    df.insert(0, 'ID_Jogador', ids)
                df.to_excel(writer, sheet_name=nome_aba, index=False)

    print("\n Automação finalizada")

if __name__ == "__main__":
    iniciar_automacao()