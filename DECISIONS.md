## Estratégias de Design e Justificativas

### Abordagem para Análise de Sentimento

A análise de sentimento foi implementada usando uma **abordagem baseada em regras**, em vez de um modelo de machine learning (ML). Esta escolha estratégica foi motivada por:

-   **Simplicidade e Transparência:** Um sistema baseado em regras é intrinsecamente mais fácil de entender e depurar. As palavras-chave positivas e negativas são explicitamente definidas e documentadas, permitindo que qualquer pessoa compreenda a lógica por trás da pontuação de sentimento.
-   **Agilidade no Desenvolvimento:** A implementação de regras é mais rápida e não exige um grande volume de dados rotulados, nem o tempo e os recursos computacionais necessários para treinar, validar e manter um modelo de ML.
-   **Controle e Manutenção:** A lista de palavras pode ser facilmente ajustada e expandida conforme novas tendências linguísticas ou termos específicos do contexto (como nomes de projetos ou iniciativas) surgem.

Embora um modelo de ML possa oferecer maior precisão em cenários complexos (ex: sarcasmo), a abordagem de regras é ideal para este protótipo, pois atende aos requisitos de forma eficaz e eficiente.

### Resiliência da Pipeline e Tratamento de Erros

A pipeline foi projetada para ser robusta e minimizar falhas, garantindo que a aplicação final continue a funcionar mesmo com problemas na coleta de dados.

-   **Tratamento de Falhas na Requisição (HTTP):** O script `fetch_rss.py` inclui um mecanismo de *retry* simples. Em caso de erro HTTP (como timeout ou status de erro), ele tenta a requisição novamente. Se a falha persistir, a aplicação registra o erro e continua o fluxo sem interromper.
-   **Garantia de Conteúdo para a Análise:** Uma das principais decisões foi aprimorar o script `process_text.py` com uma lógica de *fallback*. Se a tentativa de extrair o texto completo do artigo (web scraping) falhar, o script utiliza a descrição da notícia (coletada do RSS) para gerar a nuvem de palavras e analisar o sentimento. Isso evita que o dashboard `streamlit_app.py` receba dados vazios e, consequentemente, quebre.
-   **Aviso de Dados Insuficientes:** Para garantir a confiabilidade da análise, o script `fetch_rss.py` inclui um aviso (`warning`) no arquivo de saída caso menos de 5 notícias sejam coletadas no total. Essa é uma indicação clara de que a amostra de dados é pequena e que a análise pode não ser representativa.