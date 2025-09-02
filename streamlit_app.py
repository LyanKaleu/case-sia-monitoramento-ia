import streamlit as st
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def load_data():
    path = os.path.join("data", "news_export.json")
    if not os.path.exists(path):
        st.warning("Arquivo de dados não encontrado. Execute o pipeline antes.")
        return pd.DataFrame()
    return pd.read_json(path)


def sidebar_filters(df):
    st.sidebar.header("Filtros")
    df['published'] = pd.to_datetime(df['published'], errors='coerce')
    min_date = df["published"].min() if not df.empty else None
    max_date = df["published"].max() if not df.empty else None

    date_range = st.sidebar.date_input("Período", value=(min_date, max_date)) if min_date and max_date else None
    sentiment = st.sidebar.multiselect("Sentimento", ["positivo", "negativo", "neutro"], default=["positivo", "negativo", "neutro"])
    termo = st.sidebar.text_input("Buscar termo")
    return date_range, sentiment, termo


def filter_data(df, date_range, sentiment, termo):
    if df.empty:
        return df
    if date_range:
        df = df[(df["published"].dt.date >= date_range[0]) & (df["published"].dt.date <= date_range[1])]
    if sentiment:
        df = df[df["sentiment_label"].isin(sentiment)]
    if termo:
        search_column = "text_clean" if "text_clean" in df.columns else "description"
        df = df[df[search_column].str.contains(termo, case=False, na=False)]
    return df


def main():
    st.set_page_config(page_title="Monitoramento de Notícias SIA", layout="wide")
    st.title("Monitoramento de Percepção Pública sobre IA no Piauí")
    df = load_data()
    date_range, sentiment, termo = sidebar_filters(df)
    df_filtered = filter_data(df, date_range, sentiment, termo)

    st.subheader("Resumo")
    total = len(df_filtered)
    st.write(f"Total de notícias: {total}")
    if total > 0:
        pct_pos = (df_filtered["sentiment_label"] == "positivo").mean() * 100
        pct_neg = (df_filtered["sentiment_label"] == "negativo").mean() * 100
        pct_neu = (df_filtered["sentiment_label"] == "neutro").mean() * 100
        st.write(f"Positivas: {pct_pos:.1f}% | Negativas: {pct_neg:.1f}% | Neutras: {pct_neu:.1f}%")

        st.subheader("Distribuição por Sentimento")
        pie_data = df_filtered["sentiment_label"].value_counts()
        fig, ax = plt.subplots(figsize=(4,4))
        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Nuvem de Palavras")
        text_for_wordcloud = " ".join(df_filtered["text_clean"].dropna()) if "text_clean" in df_filtered.columns else " ".join(df_filtered["description"].dropna())
        wc = WordCloud(width=800, height=300, background_color="white").generate(text_for_wordcloud)
        fig, ax = plt.subplots(figsize=(8,3))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Tabela de Notícias")
        st.dataframe(df_filtered[["id", "title", "published", "source", "sentiment_label", "description"]])
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar CSV", data=csv, file_name="noticias_filtradas.csv", mime="text/csv")
    else:
        st.info("Nenhuma notícia encontrada para os filtros selecionados.")

    st.markdown("---")
    st.caption("Limitações: análise de sentimento baseada em regras, não detecta sarcasmo/contexto. Etapas de IA: apenas regras, sem modelos de ML.")
    st.caption("Para atualizar os dados, execute os scripts de coleta e processamento.")


if __name__ == "__main__":
    main()
