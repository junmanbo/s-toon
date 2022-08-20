import time
import logging
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from urllib.request import build_opener, install_opener
import os


def save_img(images, webtoon_name, ep):
    for i, image in enumerate(images):
        urlretrieve(
            image['src'], f'webtoon/{webtoon_name}/{ep}/img_{i}.jpg')


def get_img_src(webtoon_id, ep):
    url = f'https://comic.naver.com/webtoon/detail?titleId={webtoon_id}&no={ep}'
    req = requests.get(url)
    html = req.text
    soup = bs(html, 'html.parser')

    img_group = soup.find_all('div', class_='wt_viewer')[0]
    images = img_group.find_all('img')
    return images


def get_ep(webtoon_id):
    url = f'https://comic.naver.com/webtoon/detail?titleId={webtoon_id}'
    req = requests.get(url)
    html = req.text
    soup = bs(html, 'html.parser')

    webtoon_name = soup.find('span', class_='title').get_text()
    if not os.path.isdir(f'webtoon/{webtoon_name}'):
        os.mkdir(f'webtoon/{webtoon_name}')

        thumb = soup.find_all('div', class_='thumb')[0]
        thumb = thumb.find('img')['src']
        urlretrieve(thumb, f'webtoon/{webtoon_name}/thumbnail.jpg')
    get_a = soup.find_all('a')
    ep = []
    for a in get_a:
        try:
            get_data = a.get('href').split('=')
            w_id = get_data[1].split('&')[0]
            w_ep = get_data[2].split('&')[0]
            if w_id == webtoon_id:
                ep.append(int(w_ep))
        except:
            pass
    last_ep = max(ep)
    return last_ep, webtoon_name


if __name__ == '__main__':
    # Access Denied 에러 우회
    opener = build_opener()
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    install_opener(opener)

    if not os.path.isdir('webtoon'):
        os.mkdir('webtoon')

    # 769209: 화산귀환
    # 798172: 내곁엔 없을까
    webtoons = ['798172']

    # 웹툰
    try:
        for webtoon in webtoons:
            last_ep, webtoon_name = get_ep(webtoon)
            print(f'"{webtoon_name}" 의 최종화: {last_ep}')

            # 에피소드
            try:
                for ep in range(1, last_ep+1):
                    if not os.path.isdir(f'webtoon/{webtoon_name}/{ep}'):
                        os.mkdir(f'webtoon/{webtoon_name}/{ep}')

                        images = get_img_src(webtoon, ep)
                        save_img(images, webtoon_name, ep)
                        print(f'{webtoon_name} - {ep}화 저장 완료')

            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
