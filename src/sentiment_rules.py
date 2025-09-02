'''
- Lista de palavras positivas e negativas. Seja explícito e documente por que (em DECISIONS.md)
- Exemplo de implementação:
    pos_words = {"bom", "positivo", "aprovado", "inovador", "avançado", "promissor"}
    neg_words = {"ruim", "crítico", "problema", "preocupação", "risco", "polêmica"}
    Pontuação = sum(token in pos) - sum(token in neg)
    Rotular:
        - score > 0 -> positivo
        - score == 0 -> neutro
        - score < 0 -> negativo
- Gere coluna sentiment_label e sentiment_score

CHECK:
- Documente limtações (sarcasmo, contexto) no rodapé do dashboard e no DECISIONS.md
- Não usar modelos de ML - explique por que
'''

POSITIVE_WORDS = {"bom", "positivo", "aprovado", "inovador", "avançado", "promissor"}
NEGATIVE_WORDS = {"ruim", "crítico", "problema", "preocupação", "risco", "polêmica"}

def sentiment_score(text):
    """
    Calcula o score de sentimento baseado em palavras positivas e negativas.
    Retorna um inteiro: positivo (>0), neutro (0), negativo (<0).
    """
    tokens = text.lower().split()
    score = sum(token in POSITIVE_WORDS for token in tokens) - sum(token in NEGATIVE_WORDS for token in tokens)
    return score


def sentiment_label(score):
    """
    Rotula o sentimento com base no score.
    """
    if score > 0:
        return "positivo"
    elif score < 0:
        return "negativo"
    return "neutro"


def analyze_sentiment(text):
    """
    Retorna um dicionário com score e label do sentimento.
    """
    score = sentiment_score(text)
    label = sentiment_label(score)
    return {"sentiment_score": score, "sentiment_label": label}
