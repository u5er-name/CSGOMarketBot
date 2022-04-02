import login
import api_key_generator
import query
import json


API_KEY = api_key_generator.get_api_key() # получаем api-ключ и работаем с ним но конца сеанса, иначе каждый вызов будет генерироваться новый api-ключ

def get_market_items_db(current_db_file_name: str):
    """Возвращает базу данных всех вещей на продаже в фиксированный момент времени

    Args:
        current_db_file_name (str): имя файла базы данных, формат csv

    Returns:
        market_items_db (str): CSV-файл с данными в формате строки
    """
    db_file_url = f'https://market.csgo.com/itemdb/{current_db_file_name}' # url-адрес файла базы данных
    market_items_db = query.get_content(db_file_url) # получаем базу данных вещей
    return market_items_db 

def get_current_db_file_name():
    """Возвращает текущее имя файла базы данных

    Returns:
        current_db_file_name (str): имя файла базы данных, формат csv
    """
    url = 'https://market.csgo.com/itemdb/current_730.json' # адрес имени файла базы данных
    current_db_file_name = query.get_content(url, flag='json')['db'] # получение имени БД
    return current_db_file_name

def write_market_items_to_file(market_items_db: str):
    """Сохраняет базу данных вещей на продаже в фиксированный момент времени в csv-файл

    Args:
        market_items_db (str): CSV-файл с данными в формате строки
    """
    with open('market_items_db.csv', 'w', encoding='utf-8') as file:
        file.write(market_items_db)

def update_market_items():
    """Обновляет базу данных всех вещей на продаже в фиксированный момент времени

    Информация о предметах на главной странице сайте строится из предложений продавцов, 
    находящихся в данный момент онлайн на сайте. Она хранится в специальной базе данных и обновляется раз в минуту.
    Таким образом, сканировать главную или выполнять поиск по предметам чаще, чем раз в минуту, 
    не имеет смысла и создаёт избыточную нагрузку на наш сервер. (c) CSGO Market
    """
    current_db_file_name = get_current_db_file_name() # имя файла базы данных
    market_items_db = get_market_items_db(current_db_file_name) # сама база данных вещей
    write_market_items_to_file(market_items_db) # сохранение
    # write_market_items_to_file(get_market_items_db(get_current_db_file_name()))

def update_stickers():
    """Обновляет файл со стикерами, полученных с сервера.
    """
    url = f'https://market.csgo.com/api/GetStickers/?key={API_KEY}&lang=ru' # чтобы получить словарь стикеров, маркету необходим api-ключ
    stickers = query.get_content(url, flag='json') # получаем стикеры в json формате
    write_stickers_to_file(stickers) # сохраняем стикеры

def get_stickers():
    """Возвращает все возможные стикеры с их идентификаторами на торговой площадке.

    Returns:
        list: список словарей со стикерами
    """
    # считываем стикеры из файла
    with open('stickers.json', 'r', encoding='utf-8') as file:
        stickers = json.load(file)
    return stickers['stickers'] # возвращаем непосредственно список словарей со стикерами

def write_stickers_to_file(stickers):
    """Сохраняет все стикеры в json-файл
    """
    with open('stickers.json', 'w', encoding='utf-8') as file:
        json.dump(stickers, file, indent=4, ensure_ascii=False)

def main():
    if not login.login_to_steam():
        return False
    update_stickers()
    
if __name__ == '__main__':
    main()