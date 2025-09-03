import requests
import hashlib
import json
import os
from xml.etree import ElementTree
from bs4 import BeautifulSoup


'''
- Entrada: lista de queries (ex: "Inteligência Artificial Piauí", "SIA Piauí")
- Fonte: Google News RSS - montar URL
- Buscar 10-15 notícias por execução
- Extrair ao menos: id (hash), title, link, published, source, description
- Salvar raw em data/news_raw.json
- Tratar erros HTTP (timeout, status != 200) e fazer retry simples (1 retry)
- Ferramentas: requests, xml.etree.ElementTree ou BeatifulSoup (parser XML)

CHECK:
- Se a requisição falhar com código HTTP -> o script deve retornar um JSON vazio com campo error (não crashar)
- Se retornar < 5 notícias, gravar warning no arquivo e anotar em DECISIONS.md
'''

GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
RAW_PATH = os.path.join("data", "news_raw.json")
LIMITED_PATH = os.path.join("data", "_intermediate", "news_limited.json")


def build_rss_url(query):
	return GOOGLE_NEWS_RSS_URL.format(query=query.replace(' ', '+'))


def fetch_rss(query, retry=1):
	url = build_rss_url(query)
	try:
		response = requests.get(url, timeout=10)
		if response.status_code != 200:
			if retry > 0:
				return fetch_rss(query, retry=retry-1)
			return {"error": f"HTTP {response.status_code}"}
		return response.content
	except Exception as e:
		if retry > 0:
			return fetch_rss(query, retry=retry-1)
		return {"error": str(e)}


def parse_rss(xml_content, limit=None):
	news_list = []
	try:
		tree = ElementTree.fromstring(xml_content)
		items = tree.findall('.//item')
		if limit is not None:
			items = items[:limit]

		for item in items:
			title = item.findtext('title') or ""
			link = item.findtext('link') or ""
			pub_date = item.findtext('pubDate')
			source = item.find('source').text if item.find('source') is not None else None
			description = item.findtext('description') or ""
			description = BeautifulSoup(description, "html.parser").get_text()
			id_hash = hashlib.md5((title+link).encode()).hexdigest()
			news_list.append({
				"id": id_hash,
				"title": title,
				"link": link,
				"published": pub_date,
				"source": source,
				"description": description
			})
	except Exception as e:
		return [], str(e)
	return news_list, None


def save_data(data, path, warning=None):
	save_data = {"news": data}
	if warning:
		save_data["warning"] = warning
	
	with open(path, "w", encoding="utf-8") as f:
		json.dump(save_data, f, ensure_ascii=False, indent=2)


def get_article_text(url):
    """Tenta extrair o texto principal de uma notícia a partir do link."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return ""
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text.strip()
    except Exception as e:
        return ""


def main(queries, limit_total=15):
	all_news_raw = []  
	all_news_limited = [] 

	for query in queries:
		xml_content = fetch_rss(query)
		if isinstance(xml_content, dict) and "error" in xml_content:
			save_data([], RAW_PATH, warning=xml_content["error"])
			save_data([], LIMITED_PATH, warning=xml_content["error"])
			return
		
		raw_news, parse_error = parse_rss(xml_content)
		if parse_error:
			save_data([], RAW_PATH, warning=parse_error)
			save_data([], LIMITED_PATH, warning=parse_error)
			return
		
		for news in raw_news:
			if len(all_news_limited) < limit_total:
				all_news_limited.append(news)
		all_news_raw.extend(raw_news)

		if len(all_news_limited) >= limit_total:
			break
	
	warning = None
	if len(all_news_limited) < 5:
		warning = "Menos de 5 notícias coletadas."

	save_data(all_news_raw, RAW_PATH, warning)
	save_data(all_news_limited, LIMITED_PATH, warning)


if __name__ == "__main__":
	# Exemplo de uso
	queries = ["Inteligência Artificial Piauí", "SIA Piauí"]
	main(queries)
