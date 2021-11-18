import requests
from bs4 import BeautifulSoup as BS
import csv
import time


def get_content(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, * / *;q = 0.8"
              }
    session = requests.Session()
    resp = requests.get(url, headers=header)
    rows = []
    if resp.status_code == 200:
        page = BS(resp.text, "html.parser")
        table = page.find(id='offers_table')
        tr_list = table.find_all('tr', attrs={'class': 'wrap'})
        for tr in tr_list:
            title_cell = tr.find('td', attrs={'class': 'title-cell'})
            title = title_cell.find('h3')
            title_text = title.text.replace('\n', '')
            href = title.a['href'].replace(';promoted', '')
            td_price = tr.find('td', attrs={'class': 'td-price'})
            price_str = td_price.text.replace('\n', '')
            price = int(''.join(c for c in price_str if c.isdigit()))
            tmp = {'title': title_text, 'price_str': price_str, "price": price,
                   'url': href}
            rows.append(tmp)
    return rows


    # with open('olx.html', 'w') as f:
    #     f.write(resp.text)


def parse_content():
    # url = 'https://www.olx.ua/elektronika/kompyutery-i-komplektuyuschie/komplektuyuschie-i-aksesuary/videokarty/'
    url = 'https://www.olx.ua/elektronika/kompyutery-i-komplektuyuschie/komplektuyuschie-i-aksesuary/videokarty/?page={}'
    rows = []
    for i in range(1, 3):
        _url = url.format(i)
        rows += get_content(_url)
        time.sleep(2)

    csv_title = ['title', 'price_str', "price", 'url']
    with open('olx.csv', 'w') as f:
        wr = csv.DictWriter(f, fieldnames=csv_title, delimiter=';')
        wr.writeheader()
        wr.writerows(rows)

if __name__ == '__main__':
    parse_content()

