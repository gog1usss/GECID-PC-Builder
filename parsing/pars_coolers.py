import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time

from core.values import DB_config

CATALOG_URLS = [
    'https://telemart.ua/ua/city-1252/sistemy-oxlazhdenija/',
    'https://telemart.ua/ua/city-1252/readysetsofcbo/'
]
CSS_CARD = '.product-item'
CSS_TITLE = '.product-item__title'
CSS_PRICE = '.product-cost'
CSS_IMG = '.product-item__pic img'
PAGES_TO_PARSE = 5

def cooler_specs(full_name):
    name_upper = full_name.upper()
    brand_cooler = 'Unknown'
    vendors = ['DEEPCOOL', 'BE QUIET!', 'NOCTUA', 'ARCTIC', 'ID-COOLING', 'ZALMAN', 'NZXT', 'JONSBO', 'THERMALRIGHT', 'ASUS', 'MSI', 'SAMA', 'GAMEMAX', 'LIAN-LI','TRYX PANORAMA',
               'HEXO', 'APNX', 'QUBE', 'Ice Butterfly', 'Corsair']
    for v in vendors:
        if v in name_upper:
            if v == 'BE QUIET!': brand_cooler = 'be quiet!'
            elif v == 'ID-COOLING': brand_cooler = 'ID-Cooling'
            else: brand_cooler = v.capitalize()
            if brand_cooler == 'Nzxt': brand_cooler = 'NZXT'
            if brand_cooler == 'Msi': brand_cooler = 'MSI'
            if brand_cooler == 'Asus': brand_cooler = 'ASUS'
            break

    tdp = 150
    match = re.search(r'(\d{2,3})\s*(?:W|Вт|WATT)', name_upper)
    if match:
        tdp = int(match.group(1))
    elif 'ВОДЯНА' in name_upper or 'ВОДЯНАЯ' in name_upper or 'LIQUID' in name_upper or 'СЖО' in name_upper:
        tdp = 250

    clean_name = full_name.replace("Кулер для процесора", "").replace("Кулер", "").replace("Система рідинного охолодження", "").strip()
    clean_name = clean_name.split(' (')[0].strip()

    return brand_cooler, clean_name, tdp

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

                brand_cooler, clean_name, max_tdp = cooler_specs(raw_name)

                parsed_items.append(
                    {
                        'brand_cooler': brand_cooler,
                        'name': clean_name,
                        'max_tdp': max_tdp,
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
                                INSERT IGNORE INTO cooler (brand_cooler, name_cooler, max_tdp, price, review_url, image_url) 
                                VALUES (%s, %s, %s, %s, %s, %s)
                            '''
                cur.execute(sql_string, (
                    item['brand_cooler'], item['name'], item['max_tdp'],
                    item['price'], item['review_url'], item['image_url']
                ))

                if cur.rowcount > 0:
                    inserted_count += 1
        connection.commit()
        print(f"Coolers been added: {inserted_count}")
    except pymysql.MySQLError as e:
        print(f"Error in db {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    print(f"Push (Pages: {PAGES_TO_PARSE} per category) 🚀\n")
    all_gathered_items = []

    for base_url in CATALOG_URLS:
        print(f"\nCat_scan: {base_url} ---")
        for page_num in range(1, PAGES_TO_PARSE + 1):
            page_url = f"{base_url}?page={page_num}"
            items_from_page = parse_catalog_page(page_url)

            if not items_from_page: break
            all_gathered_items.extend(items_from_page)

            print("3sec...\n")
            time.sleep(3)

    if all_gathered_items:
        print(f"\nCoolers found: {len(all_gathered_items)}")
        save_items_db(all_gathered_items)