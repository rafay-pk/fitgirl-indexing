import requests
from bs4 import BeautifulSoup

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    post_links = soup.find_all('a', class_='post-title-link')
    return [link['href'] for link in post_links]

def extract_game_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='post-title').text.strip()
    size = soup.find('strong', text='Size:').next_sibling.strip()
    screenshots = [img['src'] for img in soup.find_all('img', class_='attachment-thumbnail')]
    magnet_link = soup.find('a', href=lambda href: href and "magnet:?xt=urn:btih:" in href)['href']

    return {
        'title': title,
        'size': size,
        'screenshots': screenshots,
        'magnet_link': magnet_link
    }

main_url = "https://fitgirl-repacks.site/all-my-repacks-a-z/"
post_links = extract_links(main_url)

# Limiting to the first 10 links for demonstration purposes
# Remove the slicing to process all links
for link in post_links[:10]:
    game_info = extract_game_info(link)
    print(game_info)