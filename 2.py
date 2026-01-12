# Полезные видосы 
# https://vkvideo.ru/video-229776486_456239044
# https://vkvideo.ru/video-229776486_456239044

# Активируй виртуальное окружение если еще не активировано
# cmd - source .venv/bin/activate

# библиотеки для парсинга
import time
import requests
from bs4 import BeautifulSoup # парсер
import re # для работы поиска (по спец символами) и т.д.
from time import sleep # Для оптимизации (замедлении парсера) от программ которые блочат парсеры и меньшей нагрузки на атакуемые парсером сайты

# для работы с элементами js на странице (Нажатие кнопки пример:далее)
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import random

# Заголовки для имитации браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://www.google.com/'
}

# Список User-Agent для ротации
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

def get_random_headers():
    """Генерация случайных заголовков"""
    headers['User-Agent'] = random.choice(user_agents)
    return headers

def make_request_with_retry(url, max_retries=3):
    """Функция для запроса с повторными попытками при ошибке 503"""
    for attempt in range(max_retries):
        try:
            sleep(random.uniform(2, 5))  # Случайная задержка между запросами
            headers = get_random_headers()
            
            # Используем сессию для сохранения cookies
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response, session
            elif response.status_code == 503:
                print(f"Попытка {attempt + 1}/{max_retries}: Сервер недоступен (503). Ждем...")
                sleep(random.uniform(10, 30))  # Увеличиваем задержку при 503
            else:
                print(f"Попытка {attempt + 1}/{max_retries}: Ошибка {response.status_code}")
                sleep(random.uniform(5, 10))
                
        except requests.exceptions.RequestException as e:
            print(f"Попытка {attempt + 1}/{max_retries}: Ошибка соединения: {e}")
            sleep(random.uniform(5, 15))
    
    return None, None

def setup_selenium_driver():
    """Настройка Selenium драйвера с опциями"""
    chrome_options = Options()
    
    # Добавляем различные опции для обхода блокировок
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Случайный User-Agent для Selenium
    user_agent = random.choice(user_agents)
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Для режима без интерфейса (раскомментировать если нужно)
    # chrome_options.add_argument('--headless')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Изменяем свойства браузера чтобы выглядеть как человек
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"Ошибка при запуске Selenium: {e}")
        return None

# Основной код
sleep(3)

# search = input("Введите название продукта (сортировка по категориям)")
# Пока закомментируем ввод для теста
search = ""

# поиск по товарам
if search:
    url = f"http://localhost/php/catalogue.php?category={search}"
else:
    url = "https://www.eldorado.ru/c/noutbuki/"

print(f"Сайт для парсинга: {url}")

# Пытаемся получить данные через requests
response, session = make_request_with_retry(url)

if response and session:
    print(f"Успешный запрос. Статус: {response.status_code}")
    
    # Если сайт требует JavaScript, используем Selenium
    if response.text.find("elUP") == -1:  # Если на странице нет нужных элементов
        print("Требуется JavaScript, запускаем Selenium...")
        
        driver = setup_selenium_driver()
        if driver:
            try:
                driver.get(url)
                # Ждем загрузки страницы
                sleep(random.uniform(3, 7))
                
                # Пытаемся найти и нажать кнопку если есть
                try:
                    # Пробуем разные селекторы для кнопок
                    button_selectors = [
                        "button[type='submit']",
                        "button[class*='load']",
                        "button[class*='more']",
                        ".load-more",
                        ".show-more",
                        "a[class*='load']",
                        "input[type='submit']",
                        "input[name='submit']"
                    ]
                    
                    for selector in button_selectors:
                        try:
                            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                            if buttons:
                                for button in buttons:
                                    if button.is_displayed():
                                        print(f"Найдена кнопка с селектором: {selector}")
                                        # Прокручиваем к кнопке
                                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                                        sleep(1)
                                        button.click()
                                        sleep(random.uniform(3, 5))
                                        break
                        except:
                            continue
                            
                except Exception as e:
                    print(f"Не удалось найти/нажать кнопку: {e}")
                
                # Получаем HTML после взаимодействия
                html = driver.page_source
                driver.quit()
                soup = BeautifulSoup(html, "lxml")
                
            except Exception as e:
                print(f"Ошибка в Selenium: {e}")
                if driver:
                    driver.quit()
                # Используем HTML из requests как запасной вариант
                soup = BeautifulSoup(response.text, "lxml")
        else:
            soup = BeautifulSoup(response.text, "lxml")
    else:
        soup = BeautifulSoup(response.text, "lxml")
else:
    print("Не удалось получить данные через requests, пробуем только Selenium...")
    driver = setup_selenium_driver()
    if driver:
        try:
            driver.get(url)
            sleep(random.uniform(5, 10))
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            driver.quit()
        except Exception as e:
            print(f"Ошибка при получении данных через Selenium: {e}")
            soup = None
            if driver:
                driver.quit()
    else:
        soup = None

if soup:
    # Отбираем товары
    data = soup.find_all("li", class_="elUP")
    
    # Если не нашли по классу elUP, пробуем другие варианты
    if not data:
        print("Не найдены элементы с классом 'elUP', пробуем другие селекторы...")
        # Пробуем разные селекторы
        possible_selectors = [
            "div[class*='product']",
            "div[class*='item']",
            "div[class*='card']",
            "article[class*='product']",
            "li[class*='product']"
        ]
        
        for selector in possible_selectors:
            data = soup.select(selector)
            if data:
                print(f"Найдены элементы с селектором: {selector}")
                break
    
    # Счетчик товаров
    product_count = 0
    
    if data:
        for i in data:
            try:
                # Заголовок
                product_count += 1
                name_element = i.find("a", class_="el2P")
                name = name_element.text.strip() if name_element else "Не указано"
                
                # Цена по символам
                price_pattern = soup.find_all("span", class_="eldY")
                price_text = i.find(string=price_pattern)
                price = price_text.strip() if price_text else "Не указана"
                
                # Картинка (закомментировано, так как нет соответствующего класса)
                # img_element = i.find("img", class_="object-scale-down h-48 w-48")
                # url_img = "http://localhost/img/" + img_element.get("src", "") if img_element else "Нет изображения"
                
                # Вывод
                print(f"Товар #{product_count}:")
                print(f"  Название: {name}")
                print(f"  Цена: {price}")
                # print(f"  Изображение: {url_img}")
                print("-" * 40)
                
            except Exception as e:
                print(f"Ошибка при обработке товара: {e}")
                continue
                
        print(f"\nВсего найдено товаров: {product_count}")
    else:
        print("Товары не найдены. Проверьте:")
        print("1. Правильность классов на сайте")
        print("2. Не изменилась ли структура сайта")
        print("3. Сохраните HTML для анализа:")
        if soup:
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("HTML сохранен в debug_page.html")
else:
    print("Не удалось получить или распарсить HTML. Возможные причины:")
    print("1. Сайт заблокировал доступ")
    print("2. Требуется капча")
    print("3. Проблемы с сетью")
    print("4. Сайт временно недоступен")