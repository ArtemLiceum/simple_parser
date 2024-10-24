import requests
from bs4 import BeautifulSoup

from parse import parse
from write_items import write_item


def get_col_lists(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return int(soup.find_all('a', class_='v-pagination__item catalog-paginate__item')[-1].text)


def creat_url(url, num):
    if '?page=' not in url:
        return url + f'?page=' + str(num)
    else:
        return url[:url.rfind('=') + 1] + str(num)


def get_page():
    url = "https://online.metro-cc.ru/category/bakaleya/rastitelnoe-maslo"  # ?page=n
    col_list = get_col_lists(url)
    for num_page in range(1, col_list + 1):
        new_url = creat_url(url, num_page)
        parse(new_url)
        write_item()


if __name__ == '__main__':
    get_page()
