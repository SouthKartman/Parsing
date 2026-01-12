import xlsxwriter
from incard_parser import array

def writer(parametr):
    
    generator = parametr()  # Вызываем функцию
    data_list = list(generator)  # Преобразуем генератор в список
    
    book = xlsxwriter.Workbook(r"/home/nonphix/Server/parsing/products.xlsx") #создаем файл
    page = book.add_worksheet("товар") #создаем таблицы
    
    # Заголовки
    headers = ["Название", "Цена", "Описание", "Изображение"]
    for col, header in enumerate(headers):
        page.write(0, col, header)
    
    page.set_column("A:A", 20)   #выбираем столбцы для работы
    page.set_column("B:B", 20)
    page.set_column("C:C", 50)
    page.set_column("D:D", 50)
    
    # Данные (начинаем с 1 строки, т.к. 0 - заголовки)
    row = 1
    for item in data_list: #записываем данные
        page.write(row, 0, item[0])  # название
        page.write(row, 1, item[1])  # цена
        page.write(row, 2, item[2])  # описание
        page.write(row, 3, item[3])  # изображение
        row += 1
    
    book.close()
    print(f"Создан файл с {len(data_list)} товарами")

writer(array) #Функция сортировки данных