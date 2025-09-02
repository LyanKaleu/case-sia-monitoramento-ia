import streamlit as st
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt


'''
- Layout mínimo exigido:
    - Sidebar: filtros (data range, sentimento: positivo|negativo|neutro, busca por termo)
    - Main:
        - Título e resumo (número total de notícias, porcentagens)
        - Gráfico de pizza -> distribuição por sentimento
        - Nuvem de palavras -> termos mais frequentes (use wordcloud)
        - Tabela interativa (st.dataframe ou st.table) com colunas principais e possibilidade de download do CSV
    - Rodapé: aviso de limitação da análise e indicação clara das etapas feitas por IA (se usou)
- Extras que valem os 5% de criatividade: filtro por data e botão "Atualizar" que reexecuta fetch (ou signala que precisa rodar scripts)

CHECK:
- Rodar streamlit run streamlit_app.py deve abrir sem exceções e exibir os widgets
'''

def load_data():
    path = os.path.join("data", "news_export.json")
    if not os.path.exists(path):
        st.warning("Arquivo de dados não encontrado. Execute o pipeline antes.")
        return pd.DataFrame()
    return pd.read_json(path)


def sidebar_filters(df):
    st.sidebar.header("Filtros")
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
        df = df[(df["published"] >= str(date_range[0])) & (df["published"] <= str(date_range[1]))]
    if sentiment:
        df = df[df["sentiment_label"].isin(sentiment)]
    if termo:
        df = df[df["text_clean"].str.contains(termo, case=False, na=False)]
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
        st.pyplot(plt.figure(figsize=(4,4)))
        plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.close()

        st.subheader("Nuvem de Palavras")
        wc = WordCloud(width=800, height=300, background_color="white").generate(" ".join(df_filtered["text_clean"].dropna()))
        fig, ax = plt.subplots(figsize=(8,3))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

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
