import requests
from bs4 import BeautifulSoup
import re
import pymysql
import time

from values import DB_config

CATALOG_URL = 'https://telemart.ua/ua/city-1252/case/'
CSS_CARD = '.product-item'
CSS_TITLE = '.product-item__title'
CSS_PRICE = '.product-cost'
PAGES_TO_PARSE = 5


def extract_case_specs(full_name):

    name_upper = full_name.upper()

    brand_case = 'Unknown'
    vendors = [
        'DEEPCOOL', 'NZXT', 'FRACTAL DESIGN', 'BE QUIET!', 'CORSAIR',
        'MSI', 'ASUS', 'LIAN LI', 'AeroCool', 'COUGAR', 'ZALMAN',
        'APNX', 'THERMALTAKE', 'Thermalright', 'VINGA', '1STPLAYER',
        'CHIEFTEC', 'GAMEMAX', 'QUBE', 'JONSBO', 'SAMA', 'TRYX', 'GAMDIAS', 'PCCooler', 'Ocypus', 'HEXO', 'Gygabite'
    ]

    for v in vendors:
        if v in name_upper:
            if v == 'BE QUIET!':
                brand_case = 'be quiet!'
            elif v == 'FRACTAL DESIGN':
                brand_case = 'Fractal Design'
            elif v == 'LIAN LI':
                brand_case = 'Lian Li'
            elif v == 'COOLER MASTER':
                brand_case = 'Cooler Master'
            elif v == '1STPLAYER':
                brand_case = '1stPlayer'
            else:
                brand_case = v.capitalize()

            if brand_case == 'Msi': brand_case = 'MSI'
            if brand_case == 'Asus': brand_case = 'ASUS'
            if brand_case == 'Nzxt': brand_case = 'NZXT'
            break

    clean_name = full_name.replace("Корпус", "").strip()

    max_gpu_length = 350

    return brand_case, clean_name, max_gpu_length


def parse_catalog_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8'
    }

    print(f"⏳ Сканируем страницу: {url}")
    parsed_items = []

    try:
        responce = requests.get(url, headers=headers)
        responce.raise_for_status()
        soup = BeautifulSoup(responce.text, 'html.parser')

        cards = soup.select(CSS_CARD)
        if not cards: return []

        print(f'📦 Найдено карточек: {len(cards)}')

        for card in cards:
            try:
                title_elem = card.select_one(CSS_TITLE)
                if not title_elem: continue
                raw_name = title_elem.text.strip()

                link = title_elem.get('href', '')
                if title_elem.name != 'a':
                    a_tag = card.select_one('a')
                    link = a_tag['href'] if a_tag else ''

                if link.startswith('/'):
                    link = 'https://telemart.ua' + link

                price_elem = card.select_one(CSS_PRICE)
                if not price_elem: continue
                price = int(re.sub(r'\D', '', price_elem.text))

                brand_case, clean_name, max_gpu = extract_case_specs(raw_name)

                parsed_items.append({
                    'brand_case': brand_case,
                    'name': clean_name,
                    'max_gpu': max_gpu,
                    'price': price,
                    'review_url': link
                })
            except Exception as e:
                continue
        return parsed_items
    except Exception as e:
        print(f"❌ Ошибка загрузки каталога: {e}")
        return []


def save_items_db(items):
    print("\n💾 ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ...")
    try:
        connection = pymysql.connect(**DB_config)
        inserted_count = 0

        with connection.cursor() as cur:
            for item in items:
                sql_string = '''
                    INSERT IGNORE INTO cases (brand_case, name_case, max_gpu_length_mm, price, review_url) 
                    VALUES (%s, %s, %s, %s, %s)
                '''
                cur.execute(sql_string, (
                    item['brand_case'],
                    item['name'],
                    item['max_gpu'],
                    item['price'],
                    item['review_url']
                ))

                if cur.rowcount > 0:
                    inserted_count += 1
        connection.commit()
        print(f"✅ Успешно! Добавлено корпусов: {inserted_count} из {len(items)}")
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка в БД: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()


if __name__ == "__main__":
    print(f"🚀 ЗАПУСК МАССОВОГО ПАРСИНГА КОРПУСОВ (СТРАНИЦ: {PAGES_TO_PARSE}) 🚀\n")
    all_gathered_items = []

    for page_num in range(1, PAGES_TO_PARSE + 1):
        page_url = f"{CATALOG_URL}?page={page_num}"
        items_from_page = parse_catalog_page(page_url)

        if not items_from_page: break
        all_gathered_items.extend(items_from_page)

        print("Ожидание 3 секунды...\n")
        time.sleep(3)

    if all_gathered_items:
        print(f"🎉 Всего собрано чистых корпусов: {len(all_gathered_items)}")
        save_items_db(all_gathered_items)