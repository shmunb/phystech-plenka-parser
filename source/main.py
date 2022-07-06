import requests as r
import pandas as pd
from bs4 import BeautifulSoup
import gspread
import datetime as dt
import time
from parser import parse


pages = ['https://www.fotoimpex.com/films/35mm-films/', 'https://www.fotoimpex.com/films/medium-format-films-120/']

items = []

for url in pages:

    reqs = r.get(url)
    soup = BeautifulSoup(reqs.content, 'html.parser')

    forward = soup.find('a', rel="next", class_="os_list_navi")

    # print(forward.get_text(),  forward.get('href'))

    if forward is not None and forward.get_text() == 'forward ' and forward.get('href') != "":
        pages.append('https://www.fotoimpex.com' + forward.get('href'))

    parse(items=items, soup=soup)

    time.sleep(0.01)

    print(pages)

print(len(items), 'Parsed')

df = pd.DataFrame.from_dict(items)
# df = df.fillna('')

df['name'] = df['name'].str.replace(pat=r'[\r\n"\\]', repl='', regex=True)
df['type'] = df['type'].str.replace(pat=r'[\r\n"\\]', repl='', regex=True)
df['availability'] = df['availability'].str.replace(pat=r"[\r\n'\\]", repl='', regex=True)

df['From 5'].fillna(df['From 1'], inplace=True)
df['From 10'].fillna(df['From 5'], inplace=True)

df['Priority'] = df['name'].map(lambda p: 'kodak' in p.lower()
                                or 'fuji' in p.lower()
                                or 'lomo' in p.lower()
                                or 'cinestill' in p.lower()
                                or 'lomo' in p.lower()
                                or 'revolog' in p.lower())

df = df.sort_values(by='type')

now = dt.datetime.now().strftime('%m%d%H%M')
df.to_excel(f'../excels/photoimpex{now}.xlsx')


gc = gspread.service_account(filename='../creds/gsheets-cresds.json')
sh = gc.open("физтех.пленка импорт")
print(sh.worksheets())
ws = sh.worksheet("stock_t")

ws.clear()
result = ws.update([df.columns.values.tolist()] + df.values.tolist())

print(result)