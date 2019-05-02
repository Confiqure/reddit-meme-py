import praw
from urllib.request import urlopen

reddit = praw.Reddit(client_id='C_NfnH766ESvtw',
                     client_secret='VG7nZxkuJiY1O0bn2pckP8E_3kE',
                     user_agent='my user agent')


def grab_links():
    links = []
    for submission in reddit.subreddit('memeeconomy').hot(limit=100):
        links.append([submission.title, submission.url, submission.url.split("/")[-1]])

    return links


def download_img(source, name, folder):
    f = open(folder + '/' + name, 'wb')
    f.write(urlopen(source).read())
    f.close()


with open("memes/!index.txt", "a") as file:
    for link in grab_links()[1:]:
        file.write(str(link[0] + ": " + link[2]) + "\n")
        download_img(link[1], link[2], "memes")



