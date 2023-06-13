import sqlite3, os, requests
from PIL import Image

pwd = os.getcwd()
data_folder = pwd + "\\data"

conn = sqlite3.connect("database.sqlite")
c = conn.cursor()

c.execute("SELECT id, title, img FROM games")
games = c.fetchall()[1:]

for game in games:
    c.execute("SELECT screenshot FROM screenshots WHERE game_id = ?", (game[0],))
    screenshots = [x[0] for x in c.fetchall()]
    print(sqlite3.Binary(requests.get(game[2]).content))
    # path = data_folder + "\\" + game[1]
    # if not os.path.exists(path):
    #     os.mkdir(path)
    #     Image.open(requests.get(game[2], stream=True).raw).save(path + "\\cover.jpg")
    #     for i, screenshot in enumerate(screenshots):
    #         Image.open(requests.get(screenshot[0], stream=True).raw).save(
    #             path + "\\" + str(i) + ".jpg"
    #         )
