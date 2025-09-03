# Monitoramento de Percepção Pública sobre IA no Piauí

## Visão Geral

Este projeto é um protótipo de pipeline para monitorar e analisar notícias sobre Inteligência Artificial (IA) no estado do Piauí. A solução coleta dados de feeds RSS do Google News, processa o texto, realiza uma análise de sentimento baseada em regras e visualiza os resultados em um painel interativo usando Streamlit.

A pipeline é composta por uma sequência de scripts Python que, quando executados na ordem correta, coletam, transformam e preparam os dados para visualização.

## Começando

### Pré-requisitos

Certifique-se de que você tem o **Python 3.8** ou superior instalado em sua máquina. O gerenciador de pacotes `pip` também é necessário.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/LyanKaleu/case-sia-monitoramento-ia
    cd seu-repositorio
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Uso

Para rodar a pipeline completa, execute os scripts na ordem abaixo a partir do diretório raiz do projeto.

1.  **Coletar notícias do RSS:**
    ```bash
    python src/fetch_rss.py
    ```
    Este script busca as notícias e salva os dados brutos e limitados na pasta `data/`.

2.  **Processar texto e extrair conteúdo:**
    ```bash
    python src/process_text.py
    ```
    Este script lê o arquivo de notícias limitadas, visita cada link para extrair o texto completo do artigo e limpa o conteúdo, salvando em um arquivo processado.

3.  **Analisar sentimento:**
    ```bash
    python src/sentiment_rules.py
    ```
    Este script aplica a análise de sentimento baseada em regras sobre o texto processado, gerando um score e um rótulo de sentimento para cada notícia.

4.  **Exportar dados para o dashboard:**
    ```bash
    python src/exporter.py
    ```
    Este script consolida os dados de sentimento e os salva no formato final (`news_export.json`) que será usado pelo painel do Streamlit.

5.  **Executar o painel do Streamlit:**
    ```bash
    streamlit run src/streamlit_app.py
    ```
    O painel será aberto em seu navegador, mostrando a análise de sentimento e a nuvem de palavras.