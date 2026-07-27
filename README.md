# 🏆 Dossiê Tático: Copa do Mundo FIFA 2026™ - Dashboard(Power BI): Relatório Analítico de Desempenho Coletivo

Bem-vindo ao repositório do **Dossiê Tático da Copa do Mundo 2026**. Este projeto é um dashboard analítico completo focado em inteligência esportiva e análise de desempenho coletivo das 48 seleções participantes do torneio. 

O objetivo principal desta ferramenta é transformar dados brutos de *scouting* oficiais em *insights* visuais acionáveis, permitindo comparações táticas profundas sobre eficiência ofensiva, solidez defensiva, controle de jogo e intensidade física.

---

## 🔗 Acessos Rápidos

*   **📊 [Acessar o Dashboard Interativo Online](https://app.powerbi.com/view?r=eyJrIjoiYTZiYmJiZDEtMGVkMy00MzU1LWE4YjItODhkYjIxMWNhNTdjIiwidCI6IjY1OWNlMmI4LTA3MTQtNDE5OC04YzM4LWRjOWI2MGFhYmI1NyJ9)**
*   **📄 [Ler a Documentação Técnica Detalhada (PDF)](Documentacao_Tecnica_Copa_2026)**

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

Este projeto engloba ponta a ponta o ciclo de vida de uma análise de dados, utilizando as seguintes ferramentas:

*   **Python (Pandas):** Análise exploratória inicial e validação da estrutura dos dados.
*   **Microsoft Power BI:** Ferramenta principal de Data Visualization e BI.
*   **Power Query (Linguagem M):** Processo de ETL (Extração, Transformação e Carga), limpeza de dados e padronização de nomenclaturas.
*   **DAX (Data Analysis Expressions):** Criação de medidas, inteligência de tempo e regras de negócio complexas.
*   **Figma:** Design de UI/UX, criação do background (plano de fundo), tipografia e iconografia padronizada no estilo corporativo da FIFA.

  <img width="1610" height="937" alt="image" src="https://github.com/user-attachments/assets/3c9347be-4a45-42f8-a4a0-fda1922c87a1" />
  <img width="1277" height="785" alt="image" src="https://github.com/user-attachments/assets/8852a193-6b39-446f-aab7-422b4ae82468" />
  <img width="1919" height="1028" alt="image" src="https://github.com/user-attachments/assets/80fed926-9fdb-4139-bff3-c3a5b115aee9" />


---

## 📂 Estrutura do Repositório

*   `Dashboard_Copa2026.pbix`: Arquivo executável do Power BI.
*   `Estatisticas_Equipes_Copa_2026.xlsx`: Banco de dados original contendo as estatísticas extraídas.
*   `etl_exploracao.py`: Script Python utilizado para leitura e validação prévia dos dados brutos.
*   `Documentacao_Tecnica_Copa_2026.pdf`: Relatório detalhando as regras de negócio, modelagem de dados e KPIs.
*   `assets/`: Pasta contendo os backgrounds e ícones desenvolvidos no Figma.

---

## 🧠 Arquitetura e Modelagem de Dados

O modelo de dados foi construído com base nas melhores práticas de BI, utilizando um **Star Schema (Esquema Estrela)** para garantir alta performance nos filtros cruzados.

*   **Tabela Dimensão:** `dEquipes` (ID, Nome do País, Continente, Quantidade de Jogos, URL da Bandeira).
*   **Tabelas Fato:** Dados segmentados por categorias táticas (`fAtaque`, `fDefesa`, `fDistribuicao`, `fDisciplina`, `fFisico`).
*   **Ajustes de ETL:** Tratamento de valores nulos, padronização de nomenclatura de países (ex: *EUA*, *RI do Irã*, *Tchéquia*) e conversão de tipagem de dados (ex: transformação de distâncias de metros para quilômetros).

---

## 🎯 Principais Análises e Páginas (Dashboard)

O relatório foi dividido em 5 verticais táticas:

1.  **Ataque & Letalidade:** Análise de Gols Esperados (xG), volume de finalizações, taxa de conversão e gráfico de dispersão cruzando Gols vs. Chutes (Eficiência Ofensiva).
   <img width="1274" height="765" alt="image" src="https://github.com/user-attachments/assets/5d9fcd6a-0cd8-4b82-9c94-2c7acc3dfcd2" />

2.  **Solidez Defensiva:** Métricas de *Clean Sheets* (Jogos sem sofrer gols), defesas do goleiro, volume de desarmes e avaliação do tempo médio de recuperação de posse de bola (*Gegenpressing*).
    <img width="1271" height="764" alt="image" src="https://github.com/user-attachments/assets/ed6da839-47c3-4d75-8fff-7f183868aedf" />

3.  **Distribuição & Controle:** Análise do estilo de jogo cruzando a Precisão dos Passes (%) com as Tentativas de Ruptura de Linha (Verticalidade).
     <img width="1272" height="764" alt="image" src="https://github.com/user-attachments/assets/23d9c7af-8cfb-46c4-8280-cdc607aa221c" />

4.  **Fair Play & Disciplina:** Avaliação de agressividade por meio da comparação entre faltas cometidas vs. sofridas e incidência de cartões.
    <img width="1268" height="760" alt="image" src="https://github.com/user-attachments/assets/e6617747-519d-44a0-b636-1833953f3fee" />

5.  **Intensidade Física:** Consolidação do esforço atlético, apresentando a distância total percorrida (km) e a velocidade média de corrida das equipes durante o torneio.
    <img width="1271" height="764" alt="image" src="https://github.com/user-attachments/assets/6cac1584-d8f8-408f-9e2a-cd01ab271d0b" />

---

## 💡 Destaques Técnicos

*   **Data Translation:** Adequação de nomenclaturas técnicas ("Perdas de bola forçadas" para "Desarmes e Interceptações") para facilitar a leitura por profissionais do esporte.
*   **UX/UI Design:** Uso de *Tooltips* (dicas de ferramenta) personalizadas nas tabelas para exibir métricas secundárias sem poluir a interface visual, além de navegação fluida entre abas estilo "aplicativo web".
*   **Agregações Inteligentes:** Correção lógica de médias de velocidade e tempo, evitando somas matemáticas incorretas que distorcem análises de longo prazo.

---

**Desenvolvido por:** Darlan Monteiro
