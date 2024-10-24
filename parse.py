import requests
from bs4 import BeautifulSoup

from write_items import DATA


def parse(url):
    response = requests.get(url)
    html_page = response.text
    soup = BeautifulSoup(html_page, "html.parser")
    ids = parse_id(soup)
    names, hrefs = parse_title_href(soup, ids)
    prices, old_prices = parse_price(soup, ids)
    add_item(ids, names, hrefs, prices, old_prices)


def parse_id(soup):
    page = soup.find("div", id="products-inner", class_="subcategory-or-type__products")

    product_cards = page.find_all('div',
        class_="catalog-2-level-product-card product-card subcategory-or-type__products-item with-prices-drop"
    )

    ids = []
    for card in product_cards:
        try:
            ids.append(card['id'])
        except:
            print('ошибка в парсинге id')
    return ids


def get_int_price(price_card):
    int_price = price_card.find('span', class_='product-price__sum-rubles')
    if int_price is not None:
        return int_price.text
    else:
        return ""


def get_penny_price(price_card):
    penny_price = price_card.find('span', class_='product-price__sum-penny')
    if penny_price is not None:
        return penny_price.text
    else:
        return ''


def get_actual_price(product):
    price_card = product.find('div', class_='product-unit-prices__actual-wrapper')
    int_price = get_int_price(price_card)
    penny_price = get_penny_price(price_card)
    if penny_price != '':
        return f'{int_price}{penny_price}'
    else:
        return int_price


def get_old_price(product):
    price_card = product.find('div', class_='product-unit-prices__old-wrapper')
    int_price = get_int_price(price_card)
    penny_price = get_penny_price(price_card)
    if penny_price != '':
        return f'{int_price}{penny_price}'
    else:
        return int_price


def parse_price(soup, ids):
    page = soup.find("div", id="products-inner")
    prices = []
    old_prices = []
    for id in ids:
        product1 = page.find('div', id=id)
        product = product1.find('div', class_='product-unit-prices__trigger')
        prices.append(get_actual_price(product))
        old_prices.append(get_old_price(product))
    return prices, old_prices


def parse_title_href(soup, ids):
    page = soup.find("div", id="products-inner")

    names = []
    hrefs = []
    for id in ids:
        product1 = page.find('div', id=id)
        product = product1.find('a', class_='product-card-photo__link reset-link')
        try:
            names.append(product['title'])
            hrefs.append(product['href'])
        except:
            print('ошибка в парсинге title или href')
    return names, hrefs


def add_item(ids, names, hrefs, prices, old_prices):
    for i in range(len(ids)):
        DATA.append([ids[i], names[i], hrefs[i], prices[i], old_prices[i]])