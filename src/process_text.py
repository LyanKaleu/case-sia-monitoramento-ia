'''
- Funções: 
    clean_html(text): remover tags HTML (BeatifulSoup .get_text())
    normalize(text): strip, lower(), remover caracteres especiais (regex), remover múltiplos espaços
    tokenize_and_filter(text): split, remover stopwords (lista simples em portuguese), remover palavras <= 2 chars
- Gerar campo text_clean e tokens
- Salvar DataFrame final com colunas: id, title, link, published, source, description, text_clean, tokens

CHECK:
- Funções testáveis (test/test_processing.py com 2 asserts)
- Handle missing fields (ex.: published nulo -> usar None) 
'''

import re
from bs4 import BeautifulSoup
import json
import os
import pandas as pd


PORTUGUESE_STOPWORDS = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", "há", "nos", "já", "está", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "depois", "sem", "mesmo", "aos", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia", "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas", "este", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram", "estava", "estávamos", "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", "estivesse", "estivéssemos", "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve", "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse", "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos", "houverão", "houveria", "houveríamos", "houveriam", "sou", "somos", "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos", "fossem", "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria", "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", "tínhamos", "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "terá", "teremos", "terão", "teria", "teríamos", "teriam"
}


def clean_html(text):
    """
    Remove tags HTML do texto usando BeautifulSoup.
    """
    if not text:
        return ""
    return BeautifulSoup(text, "html.parser").get_text()


def normalize(text):
    """
    Remove espaços extras, coloca em minúsculo e remove caracteres especiais.
    """
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize_and_filter(text):
    """
    Tokeniza, remove stopwords e palavras com <= 2 caracteres.
    """
    if not text:
        return []
    tokens = text.split()
    filtered = [t for t in tokens if t not in PORTUGUESE_STOPWORDS and len(t) > 2]
    return filtered


def main():
    raw_path = os.path.join("data", "news_raw.json")
    processed_path = os.path.join("data", "news_processed.json")

    if not os.path.exists(raw_path):
        print(f"Arquivo {raw_path} não encontrado.")
        return
    
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        news = data.get("news", [])
    
    if not news:
        print("Nenhuma notícia para processar.")
        with open(processed_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return
    
    df = pd.DataFrame(news)
    df["text_clean"] = df["description"].apply(clean_html).apply(normalize)
    df["tokens"] = df["text_clean"].apply(tokenize_and_filter)

    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump({"news": df.to_dict("records")}, f, ensure_ascii=False, indent=2)

    print(f"Notícias processadas e salvas em {processed_path}")


if __name__ == "__main__":
    main()
