import requests
from bs4 import BeautifulSoup


def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    post_links = soup.find_all("a")
    return [link["href"] for link in post_links]


urls = ["https://fitgirl-repacks.site/all-my-repacks-a-z/"]
urls.extend(
    [
        f"https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={x}#lcp_instance_0"
        for x in range(71)
        if x >= 2
    ]
)
sites_to_remove = set(open("sites-to-remove.txt", "r").readlines())
game_links = set()
for url in urls:
    game_links.update(set(extract_links(url)))
    print(game_links)
    game_links = game_links.difference(sites_to_remove)
    open("test.txt", "w").write("\n".join(game_links))
