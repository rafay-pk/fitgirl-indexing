# with open('sites-to-remove.txt', 'a+') as f:
#     [f.write(f'https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={x}#lcp_instance_0\n') for x in range(70)]
img = "http://i71.fastpic.ru/big/2015/0728/b0/abcf1d434ac1d2a36de6e1f5639483b0.jpg"

import requests

print(requests.get(img).content)
