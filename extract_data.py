import requests, sqlite3, random, re
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_size(string):
    return float(re.findall(r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", string)[0])


def extract_game_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    open("log", "w", encoding="utf-8").write(str(soup))
    magnet = soup.find("a", href=lambda href: href and "magnet:?xt=urn:btih:" in href)
    title = soup.find("strong").text.strip()
    imgs = soup.findAll("img")
    img = imgs[0]
    tagsText = ""
    companyText = ""
    sizeText = ""
    sizeText_mod = ""
    current = img
    while True:
        if not current.next_element:
            break
        current = current.next_element
        if "enre" in current.text:
            tagsText = current.next_element.text
        if "ompan" in current.text:
            companyText = current.next_element.text.split(",")
        if "epack" in current.text:
            sizeText = current.next_element.text
            sizeText_mod = sizeText.split("/")[0] if "/" in sizeText else sizeText
            break
    return {
        "title": title,
        "img": img["src"] if img else "",
        "tags": tagsText,
        "developer": companyText[0] if len(companyText) > 0 else "",
        "publisher": companyText[1] if len(companyText) > 1 else "",
        "size": get_size(sizeText_mod) * 1024
        if "gb" in sizeText.lower()
        else get_size(sizeText_mod),
        "screenshots": [
            x["src"]
            for x in imgs[1:]
            if not x["src"].endswith("192x192.jpg")
            and not x["src"].startswith("https://torrent-stats")
        ],
        "magnet": magnet["href"] if magnet else "",
    }


def create_db():
    links = open("links.txt", "r").readlines()

    conn = sqlite3.connect("database.sqlite")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT, title TEXT, img TEXT, developer TEXT, publisher TEXT, size REAL, magnet TEXT)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT UNIQUE)"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS game_tags (game_id INT NOT NULL, tag_id INT NOT NULL, FOREIGN KEY (game_id) REFERENCES games(id), FOREIGN KEY (tag_id) REFERENCES tags(id))"
    )
    c.execute(
        "CREATE TABLE IF NOT EXISTS screenshots (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INT NOT NULL, screenshot TEXT, FOREIGN KEY (game_id) REFERENCES games(id))"
    )
    for link in links:
        print(link)
        c.execute("SELECT * FROM games WHERE link = ?", (link.strip(),))
        if not c.fetchone():
            game_info = extract_game_info(link)

            try:
                img_data = sqlite3.Binary(requests.get(game_info["img"]).content)
            except:
                img_data = ""

            c.execute(
                "INSERT OR IGNORE INTO games (link, title, img, developer, publisher, size, magnet) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    link.strip(),
                    game_info["title"],
                    img_data,
                    game_info["developer"],
                    game_info["publisher"],
                    game_info["size"],
                    game_info["magnet"],
                ),
            )
            game_id = c.lastrowid
            for tag in game_info["tags"].split(","):
                c.execute("INSERT OR IGNORE INTO tags (tag) VALUES (?)", (tag.strip(),))
                tag_id = c.lastrowid
                c.execute(
                    "INSERT OR IGNORE INTO game_tags (game_id, tag_id) VALUES (?, ?)",
                    (game_id, tag_id),
                )
            for screenshot in game_info["screenshots"]:
                try:
                    screenshot_data = sqlite3.Binary(requests.get(screenshot).content)
                except:
                    screenshot_data = ""

                c.execute(
                    "INSERT OR IGNORE INTO screenshots (game_id, screenshot) VALUES (?, ?)",
                    (game_id, screenshot_data),
                )
            conn.commit()


# links = open("links.txt", "r").readlines()
# link = links[random.randint(0, len(links) - 1)]
# data = extract_game_info(link)
# # data = extract_game_info("https://fitgirl-repacks.site/35mm-v1-1/")
# print(link)
# print(data)
# # [print(data[x]) for x in data]

create_db()
