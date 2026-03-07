from Bio import Entrez
from pathlib import Path
import json
import time


Entrez.email = "aswinkumarak2005@gmail.com"


def fetch_pubmed(query: str, max_results: int = 1000, batch_size: int = 200):
    print("Searching PubMed...")
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        retmax=max_results,
    )
    record = Entrez.read(handle)
    id_list = record["IdList"]

    print(f"Found {len(id_list)} articles")

    abstracts = []

    for start in range(0, len(id_list), batch_size):
        end = min(start + batch_size, len(id_list))
        batch_ids = id_list[start:end]

        print(f"Fetching records {start} to {end}")

        fetch_handle = Entrez.efetch(
            db="pubmed",
            id=",".join(batch_ids),
            rettype="abstract",
            retmode="xml",
        )

        records = Entrez.read(fetch_handle)

        for i, article in enumerate(records["PubmedArticle"]):
            try:
                article_data = article["MedlineCitation"]["Article"]
                title = article_data["ArticleTitle"]
                abstract_list = article_data.get("Abstract", {}).get("AbstractText", [])
                abstract = " ".join(abstract_list)

                if not abstract.strip():
                    continue

                abstracts.append(
                    {
                        "id": f"doc_{start+i}",
                        "title": str(title),
                        "abstract": str(abstract),
                    }
                )
            except Exception:
                continue

        time.sleep(0.34)  # stay under 3 requests/sec

    return abstracts


def main():
    query = '("CRISPR" OR "genome editing") AND immune'
    results = fetch_pubmed(query, max_results=1000)

    output_path = Path("data/raw/corpus.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved {len(results)} abstracts to {output_path}")


if __name__ == "__main__":
    main()