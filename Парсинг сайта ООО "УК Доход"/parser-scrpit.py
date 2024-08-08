"""
Скрипт для выгрузки компаний с сайта УК Доход, 
у которых в этом месяце DCF-потенциал равен 19.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re


def connect_site(url):
    """
    :param url: Адрес сайта для соединения
    :return: Возврат HTML текста
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver


def parsing_site(driver, dcf_target):
    """
    :param driver: Получение HTML текста сайта
    :param dcf_target: Параметр DCF-потенциала компаний, используется для сортировки компаний по данному параметру
    :return: Возвращает словарь с компаниями у которых DCF-потенциал равен 19
    """
    elements = driver.find_elements(By.XPATH, '//*[@id="table-stock-share"]/tbody/tr')
    dcf_dict = {}
    for element in elements:
        text = element.text
        match = re.search(r'(\D+)\s+(\d{1,2})', text)
        if match:
            company_name = match.group(1).strip()
            dcf_value = int(match.group(2))
            if dcf_value == dcf_target:
                if dcf_value in dcf_dict:
                    dcf_dict[dcf_value].append(company_name)
                else:
                    dcf_dict[dcf_value] = [company_name]
    return dcf_dict


def csv_file(path, data):
    """
    :param path: Путь для сохранения полученных результатов
    :param data: Полученный словарь с компаниями из функции parsing_site
    :return: Итоговый результат это файл CSV формата с двумя колонками компаний у которых в этом месяце DCF-потенциал равен 19.
    """
    with open(path, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')  # Используем ; как разделитель
        writer.writerow(['DCF', 'Название компании'])  # Заголовок колонок
        for key, values in data.items():
            for value in values:
                writer.writerow([key, value])  # Запись данных


def main_process(url, dcf, path):
    """
    :param url: Адрес сайта для передачи в функцию connect_site и создания  соединения
    :param dcf: Параметр DCF-потенциала компаний, передается в функцию parsing_site для сортировки
    :param path: Путь для сохранения полученных результатов, передается в функцию csv_file
    :return: После завершения всех функций, происходит завершение процесса.
    """
    global driver
    try:
        driver = connect_site(url)
        result_data = parsing_site(driver, dcf)
        if result_data:
            csv_file(path, result_data)
    except Exception as e:
        print(f"Соединение не удалось: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    url = r'https://www.dohod.ru/ik/analytics/share' # Адрес сайта
    path = r'C:\Users\User\Desktop\test\result.csv' # Итоговый файл
    dcf = 19 # Параметр DCF-потенциала по которому будут выгружены компании
    main_process(url, dcf, path)
