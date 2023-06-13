import requests, random, sys, json, sqlite3
from bs4 import BeautifulSoup

# def extract_links(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     post_links = soup.find_all('a')
#     return [link['href'] for link in post_links]

def extract_game_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # open('log','w',encoding='utf-8').write(str(soup))
    title = soup.find('strong').text.strip()
    imgs = soup.findAll('img')
    img = imgs[0]
    tags = img.next_element.next_element.next_element
    tagsText = tags.text
    company = tags.next_element.next_element.next_element.next_element.next_element
    companyText = company.text.split(',')
    size = company.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element
    sizeText = size.text
    magnet = soup.find('a', href=lambda href: href and "magnet:?xt=urn:btih:" in href)
    # size = soup.find('strong', text=' Repack Size: ').next_sibling.strip()
    # screenshots = [img['src'] for img in soup.find_all('img', class_='attachment-thumbnail')]
    # magnet_link = soup.find('a', href=lambda href: href and "magnet:?xt=urn:btih:" in href)['href']

    return {
        'title': title,
        'img': img['src'] if img else '',
        'tags': tagsText,
        'developer': companyText[0] if len(companyText) > 0 else '',
        'publisher': companyText[1] if len(companyText) > 1 else '',
        'size': sizeText,
        'screenshots': [x['src'] for x in imgs[1:] if not x['src'].endswith('192x192.jpg') and not x['src'].startswith('https://torrent-stats')],
        'magnet': magnet['href'] if magnet else ''
    }

# urls = ["https://fitgirl-repacks.site/all-my-repacks-a-z/"]
# urls.extend([f'https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={x}#lcp_instance_0' for x in range(71) if x >= 2])
# sites_to_remove = set(open('sites-to-remove.txt', 'r').readlines())
# game_links = set()

# print(extract_links(urls[0]))

# for url in urls:
#     game_links.update(set(extract_links(url)))
#     print(game_links)
#     game_links = game_links.difference(sites_to_remove)
#     open('links.txt', 'w').write('\n'.join(game_links))


# post_links = extract_links(urls)
# [print(link, sep='\n') for link in post_links]

# for link in post_links:
    # game_info = extract_game_info(link)
    # print(game_info)

# sys.stdout = open('log', 'w')
links = open('links.txt', 'r').readlines()
# print(json.dumps(extract_game_info(links[round(random.random() * len(links))]), indent=4))

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, img TEXT, developer TEXT, publisher TEXT, size TEXT, magnet TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT UNIQUE)')
c.execute('CREATE TABLE IF NOT EXISTS game_tags (game_id INT NOT NULL, tag_id INT NOT NULL, FOREIGN KEY (game_id) REFERENCES games(id), FOREIGN KEY (tag_id) REFERENCES tags(id))')
c.execute('CREATE TABLE IF NOT EXISTS screenshots (id INT NOT NULL UNIQUE, game_id INT NOT NULL, screenshot TEXT, FOREIGN KEY (game_id) REFERENCES games(id))')
for link in links:
    game_info = extract_game_info(link)
    c.execute('INSERT INTO games (title, img, developer, publisher, size, magnet) VALUES (?, ?, ?, ?, ?, ?)', (game_info['title'], game_info['img'], game_info['developer'], game_info['publisher'], game_info['size'], game_info['magnet']))
    game_id = c.lastrowid
    for tag in game_info['tags'].split(','):
        c.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag.strip(),))
        tag_id = c.lastrowid
        c.execute('INSERT OR IGNORE INTO game_tags (game_id, tag_id) VALUES (?, ?)', (game_id, tag_id))
    for screenshot in game_info['screenshots']:
        c.execute('INSERT OR IGNORE INTO screenshots (game_id, screenshot) VALUES (?, ?)', (game_id, screenshot))
    conn.commit()