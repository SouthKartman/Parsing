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



def download(url): #Код подходит и для больших файлов
    resp = requests.get(url, stream=True) #stream нужен для потоковой пердачи (постепенной загрузки)
    #это значит что видео/картинка/тд не вся грузится в ОЗУ а порционно (контроль памяти) 
    r = open("/home/nonphix/Server/parsing/img/" + url.split("/")[-1] ,"wb") # Запись в байты / write byte //// путь + название картинки + slplit делит по / + -1 тк split (нарезание)
    for value in resp.iter_content(1024*1024): #iter.content - 1мб = 1024*1024 / в байты за один проход 
        r.write(value)
    r.close()
    
    
    
    
    

# list_card_url = [] #Созбдаем список где будут ссылки

def get_url(): #Создание генератор вместо списка (Функции оптимизации для парсинга больших данных (например: 9000 карт)) 
 
    sleep(1) # 3 секунды на код (не дает сделать еще один запрос) - между запросами 3 секунды

    # url = "https://sp-man.ru/catalog/" сайт для примера

    url = f"http://localhost/php/catalogue.php" # для поиска
        
    response = requests.get(url, headers=headers) #Закидываем поддельные заголовки на страницу

    print (f"Сайт для парсинга {url}")
    print (response)


    # for count in range(1,8):  #Для пагинации*1 (последующий код будет внутри цикла (весь))
        # url = f"http://localhost/php/catalogue.php/?page={count}"  # для сайтов с пагинацией


    # time.sleep(1)

    #_____________________________________________________________


    # для кнопки подгрузки страницы - selenium, для сайтов с пагинацией по url он не нужен (смотри *1)

    #_____________________________________________________________


    driver = webdriver.Chrome() #Открывет Chrome
    driver.get(url)  # ДОБАВЛЕНО: нужно сначала перейти на страницу
    next_button = WebDriverWait(driver, 10).until(
        # EC.element_to_be_clickable((By.CSS_SELECTOR, ".grid.hover\\:mx-3"))
        EC.element_to_be_clickable((By.NAME, "submit"))
    )
    next_button.click()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "lxml") # если сайт с кнопокой то driver.page_source
    driver.quit() # Закрывает Selenium

    # ___________________________________________________________________
    


    # Отбираем товары
    data = soup.find_all("div", class_="grid items-center border-solid border-2 border-gray-200 rounded-md px-5 max-w-sm cardColorCardBG")

    for i in data:
        
        card_url = "http://localhost/" + i.find("a").get("href") #Берем первую попавшиесю ссылку
        # list_card_url.append(card_url) # Добавили в список ссылки
        
        yield card_url # yield - как return тока оптимизированный - ждет значения функция/после получения вырубаеться функция (в итоге 2 функции работают по очереди а не одновременно)

def array(): # Перекидываем массив данных в Excel
    

# т.к перешли на новую страницу
    for card_url in get_url():


        response = requests.get(card_url, headers=headers) # Закидываем опять заголовки уже на новую страницу
        
        # ___________________________________________________________________
        
        sleep(2)
        soup = BeautifulSoup(response.text, "lxml") # парсим
        
        # ___________________________________________________________________
        
        data = soup.find("div", class_="grid product p-5 sm:grid-cols-1 lg:grid-cols-2") #Сортируем 
        
        # Из карты товара
        name = data.find("h1")
        price = data.find("h2")
        desc = data.find("p",class_="text-justify")
        
        img_element = data.find("img", class_="object-scale-down h-80 w-80")
        url_img = "http://localhost/img/" + img_element.get("src", "") if img_element else "Нет изображения"  # .get - поиск по атрибутам (src и тд)
        
        download(url_img)
        
        # print(f"""Название: {name.text}, Цена: {price}, Описание: {desc}, Картинка {url_img}""")
        yield name.text, price.text, desc.text, url_img #Возвращаем кортеж данных
        