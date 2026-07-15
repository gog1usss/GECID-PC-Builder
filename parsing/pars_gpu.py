import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time
from core.values import DB_config

CATALOG_URL = 'https://telemart.ua/ua/city-1252/videocard/'
CSS_CARD = '.product-item'
CSS_TITLE = '.product-item__title'
CSS_PRICE = '.product-cost'
PAGES_TO_PARSE = 5


def gpu_brand_socket(full_name):

    name_upper = full_name.upper()

    chip_prod = 'Unknown'
    if 'RTX' in name_upper or 'GTX' in name_upper:
        chip_prod = 'NVIDIA'
    elif 'Radeon' in name_upper or 'RX' :
        chip_prod = 'AMD'
    elif 'ARC' in name_upper:
        chip_prod = 'Intel'

    brand_gpu = 'unknown'
    vendors = ['ASUS', 'MSI', 'GIGABYTE', 'PALIT', 'INNO3D', 'ZOTAC', 'SAPPHIRE', 'POWERCOLOR', 'ASROCK', 'XFX', 'PNY', 'ACER', 'SPARKLE']
    for v in vendors:
        if v in name_upper:
            brand_gpu = 'ASRock' if v == 'ASROCK' else v.capitalize()
            if brand_gpu == 'Asus': brand_gpu = 'ASUS'
            if brand_gpu == 'Msi': brand_gpu = 'MSI'

            break

    tdp = 200

    if '5090' in name_upper:
        tdp = 600
    elif '5080' in name_upper:
        tdp = 400
    elif '5070 TI' in name_upper:
        tdp = 300
    elif '5070' in name_upper:
        tdp = 250
    elif '5060 TI' in name_upper:
        tdp = 175
    elif '5060' in name_upper:
        tdp = 145
    elif '5050' in name_upper:
        tdp = 130

    elif '4090' in name_upper:
        tdp = 450
    elif '4080' in name_upper:
        tdp = 320
    elif '4070 TI' in name_upper:
        tdp = 285
    elif '4070' in name_upper:
        tdp = 200
    elif '4060 TI' in name_upper:
        tdp = 160
    elif '4060' in name_upper:
        tdp = 115

    elif '3060 TI' in name_upper:
        tdp = 200
    elif '3060' in name_upper:
        tdp = 170
    elif '3050' in name_upper:
        tdp = 130

    elif '9900 XTX' in name_upper:
        tdp = 400
    elif '9900 XT' in name_upper:
        tdp = 350
    elif '9070 XT' in name_upper:
        tdp = 304
    elif '9070 ' in name_upper:
        tdp = 220
    elif '9060 XT' in name_upper:
        tdp = 160
    elif '9060' in name_upper:
        tdp = 132

    elif '8900 XTX' in name_upper:
        tdp = 350
    elif '8800 XT' in name_upper:
        tdp = 260
    elif '8700 XT' in name_upper:
        tdp = 220
    elif '8600' in name_upper:
        tdp = 150

    elif '7900 XTX' in name_upper:
        tdp = 355
    elif '7900 XT' in name_upper:
        tdp = 315
    elif '7900 GRE' in name_upper:
        tdp = 260
    elif '7800 XT' in name_upper:
        tdp = 263
    elif '7700 XT' in name_upper:
        tdp = 245
    elif '7600' in name_upper:
        tdp = 165

    elif '6700' in name_upper:
        tdp = 230
    elif '6600' in name_upper:
        tdp = 132

    clean_name = full_name.replace("Відеокарта", "").replace("Видеокарта", "").strip()
    clean_name = re.split(r'\s+\d+GB|\s+\d+MB', clean_name, flags=re.IGNORECASE)[0]
    clean_name = clean_name.strip()

    return brand_gpu, clean_name, chip_prod, tdp

def parse_catalog_page(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8'
    }

    print("Scanning")

    parsed_items = []

    try:

        responce = requests.get(url, headers=headers)
        responce.raise_for_status()
        soup = BeautifulSoup(responce.text, 'html.parser')

        cards = soup.select(CSS_CARD)
        print(f'Cards found: {cards}')

        for card in cards:
            try:
                title_elem = card.select_one(CSS_TITLE)
                if not title_elem : continue
                raw_name = title_elem.text.strip()

                link = title_elem.get('href','')
                if title_elem.name != 'a':
                    a_tag = card.select_one('a')
                    link = a_tag['href'] if a_tag else ''

                #if link.startswith('/'):
                    link = 'https://telemart.ua' + link

                price_elem = card.select_one(CSS_PRICE)
                if not price_elem: continue
                price = int(re.sub(r'\D','',price_elem.text))

                brand_gpu, clean_name, chip_prod, estimated_tdp = gpu_brand_socket(raw_name)

                parsed_items.append(
                    {
                        'brand_gpu': brand_gpu,
                        'name': clean_name,
                        'chip_prod': chip_prod,
                        'tdp': estimated_tdp,
                        'price': price
                    }
                )
            except Exception as e:
                print(f'Error: {e}')
                continue
        return parsed_items
    except Exception as e:
        print(f"Error with catalog: {e}")

def save_items_db(items):

    try:
        connection = pymysql.connect(**DB_config)
        inserted_count = 0

        with connection.cursor() as cur:
            for item in items:

                sql_string = '''
                                INSERT IGNORE INTO gpu (brand_gpu, name_gpu, chip_prod, tdp, price_gpu) 
                                VALUES (%s, %s, %s, %s, %s)
                            '''
                cur.execute(sql_string, (item['brand_gpu'], item['name'], item['chip_prod'],
                    item['tdp'], item['price']))

                if cur.rowcount > 0:
                    inserted_count += 1
        connection.commit()
        print(f"Videocards been added: {inserted_count}")
    except pymysql.MySQLError as e:
        print(f"Error in db {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()


if __name__ == "__main__":
    print(f"Push (Pages: {PAGES_TO_PARSE}) 🚀\n")
    all_gathered_items = []

    for page_num in range(1, PAGES_TO_PARSE + 1):
        page_url = f"{CATALOG_URL}?page={page_num}"
        items_from_page = parse_catalog_page(page_url)

        if not items_from_page: break
        all_gathered_items.extend(items_from_page)

        print("3sec...\n")
        time.sleep(3)

    if all_gathered_items:
        print(f"GPUS found: {len(all_gathered_items)}")
        save_items_db(all_gathered_items)
































'''def get_price(url, css_selector):

        headers =  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6'
        }
        try:
            print(f"Scanning web {url}")

            responce = requests.get(url, headers = headers)

            responce.raise_for_status()

            soup = BeautifulSoup(responce.text, 'html.parser')

            price_element = soup.select_one(css_selector)

            if price_element:

                raw_price = price_element.text
                print(f"Price found: {raw_price.strip()}")

                final_db_price = re.sub(r'\D','',raw_price)

                return int(final_db_price)

            else:
                print("Failed to find price")

        except requests.exceptions.HTTPError as e:
            print(f'Access denied')
        except Exception as e:
            print(f'Unknown error: {e}')

        return None

if __name__ == '__main__':

    test_url = 'https://telemart.ua/ua/products/amd-ryzen-7-7700-3853ghz-32mb-sam5-box-100-100000592box/'

    target_css_class = '.card-block__price-summ'

    if test_url != '':
        price = get_price(test_url,target_css_class)
        if price:
            print(f"Price for db: {price}")
        else:
            print("Enter link for the good: ")'''
