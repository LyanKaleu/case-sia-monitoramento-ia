import requests
import hashlib
import json
import os
from xml.etree import ElementTree


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


def parse_rss(xml_content):
	news_list = []
	try:
		tree = ElementTree.fromstring(xml_content)
		for item in tree.findall('.//item'):
			title = item.findtext('title')
			link = item.findtext('link')
			pub_date = item.findtext('pubDate')
			source = item.find('source').text if item.find('source') is not None else None
			description = item.findtext('description')
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


def save_raw_news(news, warning=None):
	data = {"news": news}
	if warning:
		data["warning"] = warning
	with open(RAW_PATH, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)


def main(queries):
	all_news = []
	for query in queries:
		xml_content = fetch_rss(query)
		if isinstance(xml_content, dict) and "error" in xml_content:
			save_raw_news([], warning=xml_content["error"])
			return
		news, parse_error = parse_rss(xml_content)
		if parse_error:
			save_raw_news([], warning=parse_error)
			return
		all_news.extend(news)
	warning = None
	if len(all_news) < 5:
		warning = "Menos de 5 notícias encontradas. Verificar DECISIONS.md."
	save_raw_news(all_news, warning=warning)


if __name__ == "__main__":
	# Exemplo de uso
	queries = ["Inteligência Artificial Piauí", "SIA Piauí"]
	main(queries)
