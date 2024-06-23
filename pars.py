from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import csv
import time

def get_skin_info(url, extension_path):
    # Установка драйвера для Chrome
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_extension(extension_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(10)
    # Увеличение времени ожидания до 3 минут
    max_wait_time = 180
    poll_interval = 5

    skin_elements = []
    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        try:
            skin_elements = WebDriverWait(driver, poll_interval).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'market_listing_row'))
            )
            if skin_elements:
                break
        except Exception as e:
            print(f"Waiting for skin elements: {e}")
            time.sleep(poll_interval)  # Ожидание перед повторной попыткой

    if not skin_elements:
        print(f"Elements not found within {max_wait_time} seconds.")
        driver.quit()
        return None

    skin_infos = []
    for skin_element in skin_elements:
        try:
            # Получаем название и цену скина
            name = skin_element.find_element(By.CLASS_NAME, 'market_listing_item_name').text

            # Открываем теневой DOM элемент, чтобы получить float значение
            shadow_root = skin_element.find_element(By.CSS_SELECTOR, 'csfloat-item-row-wrapper').shadow_root
            float_row = shadow_root.find_element(By.CLASS_NAME, 'float-row-wrapper')
            float_value = float_row.text.split('Float:')[1].split()[0]

            skin_infos.append({
                'name': name,
                'float': float_value
            })
        except Exception as e:
            print(f"An error occurred while processing a skin element: {e}")

    # Создание CSV-файла с информацией о скинах
    csv_filename = 'skin_info.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'float']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for info in skin_infos:
            writer.writerow(info)

    print(f'CSV файл {csv_filename} успешно создан.')

    # Закрытие браузера
    driver.quit()

    return csv_filename