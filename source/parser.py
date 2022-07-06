import re


def parse(items, soup, item_type=''):
    _type = soup.find('div', class_="col-lg-6 col-md-6 col-sm-6 col-xs-12").get_text()

    for i, item in enumerate(soup.find_all('div', class_="os_list_box2_all")):
        name = item.a.get_text()
        link = 'https://www.fotoimpex.com' + item.a.get('href')

        aval = item.find('div', class_='os_list_shipt1').get_text() if item.find('div',
                                                                                 class_='os_list_shipt1') is not None else 'Sold out (#NA)'

        pricelist = item.find_all('td', class_="sprtab")
        prices = list(filter(lambda x: '*' in x, list(p.get_text() for p in pricelist)))
        prices = list(re.search('[0-9].?,[0-9].?', p).group(0).replace(',', '.') for p in prices)

        priceqtylist = item.find_all('td', class_="")
        priceqty = list(filter(lambda x: x != "",
                               list(p.get_text() for p in priceqtylist)))

        # list(zip(priceqty, prices))

        # print(name, link, aval, )

        obj = {
            'name': name,
            'link': link,
            'type': _type,
            'availability': aval,
            # 'prices' : list(zip(priceqty, prices)),
            'From 1': float(prices[0]),
            'From 5': float(prices[1]) if len(prices) > 2 else None,
            'From 10': float(prices[-1]) if len(prices) > 1 else None

        }

        items.append(obj)
