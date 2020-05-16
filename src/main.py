import requests
from bs4 import BeautifulSoup
from config import url, count_dis, path_dict_urls_forum, time_couple
import webbrowser
import datetime
import time


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
    return text


def get_dict_urls_forum():
    dictionary = {}
    with open(path_dict_urls_forum, 'r', encoding='utf-8') as input_file:
        text = input_file.read().split("\n")
    i = 1
    for text_line in text:
        is_one = True
        name = ''
        url_forum = ''
        for c in text_line:
            if is_one and c != '|':
                name = name + c
            elif not is_one and c != '|':
                url_forum = url_forum + c
            elif c == '|':
                is_one = False
        dictionary[i] = [name, url_forum]
        i = i + 1
    return dictionary


def open_url_in_browser(name_val: str, name: str, url_forum: str):
    time = datetime.datetime.now()
    h = time.hour
    m = time.minute
    tc = time_couple

    if tc[0][0][0] <= h <= tc[0][2][0] and tc[0][1][0] <= m <= tc[0][3][0] or tc[1][0][0] <= h <= tc[1][2][0] and tc[1][1][0] <= m <= tc[1][3][0] or tc[2][0][0] <= h <= tc[2][2][0] and tc[2][1][0] <= m <= tc[2][3][0] or tc[3][0][0] <= h <= tc[3][2][0] and tc[3][1][0] <= m <= tc[3][3][0]:
        if name_val != name:
            name_val = name
            webbrowser.open(url_forum, new=2)
    return name_val


def main():
    count_sleep = 0
    exiting = False
    name_val = ''
    while not exiting:
        if count_sleep > 980:
            exiting = True
        else:
            time.sleep(600)
        page = requests.get(url)
        # page = read_file('C:\\Users\\Ristal\\Documents\\index.html')
        soup = BeautifulSoup(page.text, "html.parser")
        e = [e.get_text() for e in soup.find_all('td', {'style': 'border: 3px dashed #FF6464; font-size:0.9em'})]
        if e.__len__() == 0:
            continue
        else:
            e = e[0].split('●')
            dictionary = get_dict_urls_forum()
            name_dis = e[2]
            br = False
            for i in range(count_dis):
                if i == 0:
                    continue
                elif br:
                    break
                forum = dictionary.get(i)
                name = forum[0]
                url_forum = forum[1]
                for j in range(6):
                    if name_dis[j] == name[j]:
                        if j == 5:
                            open_url_in_browser(name_val=name_val, name=name, url_forum=url_forum)
                    elif name_dis[j + 1] == name[j]:
                        if j == 5:
                            name_val = open_url_in_browser(name_val=name_val, name=name, url_forum=url_forum)
                            br = True
                            break
                    else:
                        break


if __name__ == '__main__':
    main()
