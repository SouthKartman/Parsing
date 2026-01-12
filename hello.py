
# Полезные видосы 
# https://vkvideo.ru/video-229776486_456239044
# https://vkvideo.ru/video-229776486_456239044


# Проход по каталогам и подтягивание инфы


# Активируй виртуальное окружение если еще не активировано
# cmd - source .venv/bin/activate

# библиотеки для парсинга
import time
import requests
from bs4 import BeautifulSoup #парсер
import re #для работы поиска (по спец символами) и т.д.
from time import sleep #Для оптимизации (замедлении парсера) от программ которые блочат парсеры и меньшей нагрузки на атакуемые парсером сайты

#для работы с элементами js на странице (Нажатие кнопки пример:далее)
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# Загаловки
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'} #Подделка заголовка от программ блочащих парсер (тип зашел user из Mozilla)



# for count in range(1,8):  #Для пагинации*1 (последующий код будет внутри цикла (весь))
    # url = f"http://localhost/php/catalogue.php/?page={count}"  # для сайтов с пагинацией
    
sleep(3) # 3 секунды на код (не дает сделать еще один запрос) - между запросами 3 секунды

# url = "https://sp-man.ru/catalog/" сайт для примера

url = f"http://localhost/php/catalogue.php" # для поиска
    
    
        
response = requests.get(url, headers=headers)
print (f"Сайт для парсинга {url}")
print (response)

#Если сайт обычный
#soup = BeautifulSoup(response.text, "lxml") #есть еще html.parser и др
 
# print(response.text)

time.sleep(1)

search = input("Введите название продукта (сортировка по категориям)")

# поиск по товарам
if search:
    url = f"http://localhost/php/catalogue.php?category={search}"
else:
    url = "http://localhost/php/catalogue.php"

# для кнопки подгрузки страницы - selenium, для сайтов с пагинацией по url он не нужен (смотри *1)
try:
    
    chrome_options = Options() 
    #_____________________________________________________________
    
    driver = webdriver.Chrome(options=chrome_options) # options=chrome_options для очистки куки
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    
    #_____________________________________________________________
    
    driver.get(url)  # ДОБАВЛЕНО: нужно сначала перейти на страницу
    next_button = WebDriverWait(driver, 10).until(
        # EC.element_to_be_clickable((By.CSS_SELECTOR, ".grid.hover\\:mx-3"))
        EC.element_to_be_clickable((By.NAME, "submit"))
    )
    next_button.click()
    time.sleep(4)
    driver.quit()
    soup = BeautifulSoup(driver.page_source, "lxml") # если сайт с кнопокой то driver.page_source
      # Закрыть драйвер после использования# Ждем загрузки
except Exception as e: # Если кнопки нету
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(4)
    print(f"Кнопки нету")
    # Если Selenium не сработал
    soup = BeautifulSoup(driver.page_source, "lxml")
    print("Использован обычный requests")
    
   
time.sleep(2)
driver.quit() # Закрывает Selenium

#Позже так как нужно сначало подгрузить весь каталог


# soup = BeautifulSoup(response.text, "lxml") обычный парсинг без selenium (взаимодействия с js)


# Отбираем товары
data = soup.find_all("div", class_="grid items-center border-solid border-2 border-gray-200 rounded-md px-5 max-w-sm cardColorCardBG")


#Example -  name = soup.find("p", class_="font-bold line-clamp-1 text-lg")
#Example1/2 - img_element = soup.find("img", class_="object-scale-down h-48 w-48")
#Example2/2 - url_img = "http://localhost/php/catalogue.php/" + img_element.get("src", "") if img_element else "Нет изображения"  # .get - поиск по атрибутам (src и тд)

# Счетчик товаров
product_count = 0

if data is not None:
    for i in data:
        # Заголовок
        product_count += 1
        name = i.find("p", class_="font-bold line-clamp-1 text-lg")
        # Цена по символам
        price_pattern = re.compile(r'\$?\d+[.,]\d{2}|\d+\s*(?:руб|USD|EUR|₽)')
        price = i.find(string=price_pattern)
        # Картинка
        img_element = i.find("img", class_="object-scale-down h-48 w-48")
        url_img = "http://localhost/img/" + img_element.get("src", "") if img_element else "Нет изображения"  # .get - поиск по атрибутам (src и тд)
        # Вывод
        print(url_img)
        print(f"""Название: {name.text}, Цена: {price}, Изображение: {url_img}""")
        print (f"Счетчик товаров: {product_count} товаров")
else:
    print("элемент не найден")