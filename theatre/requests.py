import requests


def get_wikipedia_article(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": title
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        page = next(iter(data["query"]["pages"].values()))
        if "extract" in page:
            return page["extract"]
        else:
            return "Article not found."
    else:
        return f"Error: {response.status_code}"
