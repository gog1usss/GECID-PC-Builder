import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time
from core.values import DB_config
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CATALOG_URL = 'https://telemart.ua/ua/city-1252/motherboard/'
CSS_CARD = '.product-item'
CSS_TITLE = '.product-item__title'
CSS_PRICE = '.product-cost'
CSS_IMG = '.product-item__pic img'
PAGES_TO_PARSE = 5

def mb_specs(full_name):
    name_upper = full_name.upper()

    brand_mother = 'Unknown'
    vendors = ['ASUS', 'MSI', 'GIGABYTE', 'ASROCK', 'BIOSTAR', 'NZXT']
    for v in vendors:
        if v in name_upper:
            brand_mother = 'ASRock' if v == 'ASROCK' else v.capitalize()
            if brand_mother == 'Asus': brand_mother = 'ASUS'
            if brand_mother == 'Msi': brand_mother = 'MSI'
            if brand_mother == 'Nzxt': brand_mother = 'NZXT'
            break

    socket_mother = 'Unknown'
    if 'AM5' in name_upper: socket_mother = 'AM5'
    elif 'AM4' in name_upper: socket_mother = 'AM4'
    elif '1700' in name_upper: socket_mother = 'LGA1700'
    elif '1200' in name_upper: socket_mother = 'LGA1200'
    elif '1151' in name_upper: socket_mother = 'LGA1151'

    form_factor = 'ATX'
    if 'MICRO' in name_upper or 'MATX' in name_upper or 'M-ATX' in name_upper: 
        form_factor = 'Micro-ATX'
    elif 'MINI' in name_upper or 'ITX' in name_upper: 
        form_factor = 'Mini-ITX'
    elif 'E-ATX' in name_upper or 'EATX' in name_upper: 
        form_factor = 'E-ATX'

    ram_type = 'DDR5' if 'DDR5' in name_upper else 'DDR4'

    clean_name = full_name.replace("Материнська плата", "").replace("Материнская плата", "").strip()
    clean_name = clean_name.split(' (')[0].strip()

    return brand_mother, clean_name, socket_mother, form_factor, ram_type

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
        print(f'Cards found: {len(cards)}')

        for card in cards:
            try:
                title_elem = card.select_one(CSS_TITLE)
                if not title_elem : continue
                raw_name = title_elem.text.strip()

                link = title_elem.get('href','')
                if title_elem.name != 'a':
                    a_tag = card.select_one('a')
                    link = a_tag['href'] if a_tag else ''

                if link.startswith('/'):
                    link = 'https://telemart.ua' + link

                price_elem = card.select_one(CSS_PRICE)
                if not price_elem: continue
                price = int(re.sub(r'\D','',price_elem.text))

                img_elem = card.select_one(CSS_IMG)
                image_url = ''
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src') or ''

                brand_mother, clean_name, socket_mother, form_factor, ram_type = mb_specs(raw_name)

                if socket_mother == 'Unknown': continue

                parsed_items.append(
                    {
                        'brand_mother': brand_mother,
                        'name': clean_name,
                        'socket_mother': socket_mother,
                        'form_factor': form_factor,
                        'ram_type': ram_type,
                        'price': price,
                        'review_url': link,
                        'image_url': image_url
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
                                INSERT IGNORE INTO motherboard (brand_mother, name_mother, socket_mother, form_factor, ram_type, price_mother, review_url, image_url) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            '''
                cur.execute(sql_string, (
                    item['brand_mother'], item['name'], item['socket_mother'],
                    item['form_factor'], item['ram_type'], item['price'], 
                    item['review_url'], item['image_url']
                ))

                if cur.rowcount > 0:
                    inserted_count += 1
        connection.commit()
        print(f"Motherboards been added: {inserted_count}")
    except pymysql.MySQLError as e:
        print(f"Error in db {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    print(f"Push (Pages: {PAGES_TO_PARSE}) \n")
    all_gathered_items = []

    for page_num in range(1, PAGES_TO_PARSE + 1):
        page_url = f"{CATALOG_URL}?page={page_num}"
        items_from_page = parse_catalog_page(page_url)

        if not items_from_page: break
        all_gathered_items.extend(items_from_page)

        print("3sec...\n")
        time.sleep(3)

    if all_gathered_items:
        print(f"Motherboards found: {len(all_gathered_items)}")
        save_items_db(all_gathered_items)