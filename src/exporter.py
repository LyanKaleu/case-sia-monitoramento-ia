import os
import json
import pandas as pd
import argparse


'''
- Salvar CSV ou JSON completo (em data/)
- Incluir opção de sobrescrever com --force e opção --top N

CHECK:
- Incluir no README os comandos exatos para gerar os arquivos (ex.: python src/fetch_rss.py && python src/process_text.py && python src/exporter.py)
'''

def load_data(json_path):
    """
    Carrega dados do arquivo JSON.
    """
    if not os.path.exists(json_path):
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("news", [])


def export_data(data, out_path, top_n=None, as_csv=False, force=False):
    """
    Exporta dados para CSV ou JSON, com opções de sobrescrever e limitar N linhas.
    """
    if top_n:
        data = data[:top_n]
    if os.path.exists(out_path) and not force:
        print(f"Arquivo {out_path} já existe. Use --force para sobrescrever.")
        return
    df = pd.DataFrame(data)
    if as_csv:
        df.to_csv(out_path, index=False, encoding="utf-8")
    else:
        df.to_json(out_path, orient="records", force_ascii=False, indent=2)
    print(f"Arquivo exportado: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Exporta dados para CSV ou JSON.")
    parser.add_argument("--csv", action="store_true", help="Exporta para CSV (padrão é JSON)")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivo existente")
    parser.add_argument("--top", type=int, default=None, help="Exporta apenas os top N registros")
    args = parser.parse_args()

    json_path = os.path.join("data", "news_raw.json")
    out_path = os.path.join("data", f"news_export.{'csv' if args.csv else 'json'}")
    data = load_data(json_path)
    export_data(data, out_path, top_n=args.top, as_csv=args.csv, force=args.force)


if __name__ == "__main__":
    main()
    