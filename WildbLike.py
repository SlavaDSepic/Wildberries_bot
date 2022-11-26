from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests
import json
from selenium.webdriver.firefox.options import Options
import random
from fake_useragent import UserAgent

# os.environ['MOZ_HEADLESS'] = '1'

n = int(input('Введите количество авторизаций: '))

def get_likes():
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.binary_location = r"C:\Program Files\Firefox Developer Edition\firefox.exe"
    options.add_argument(f'user-agent={user_agent}')
    options.set_preference("dom.webdriver.enabled", False)

    with open('Product_list.txt', encoding='utf-8') as file_in:
        lines = file_in.readlines()
        products = {}
        for line in lines:
            keywords = []
            line = list(line.split(','))
            other = line[1:]
            for word in other:
                keywords.append(word.strip())
            products[line[0].strip()] = keywords


    print(products)

    driver = webdriver.Firefox(options=options, executable_path=r'C:\geckodriver' \
                                                              r'.exe')

    # Заходим на сайт:

    driver.get("https://www.wildberries.ru")
    sleep(2)

    def get_like(products):
        # Получение номера на сервисе OnlineSim:

        api_key = '6104cdf2aa594a6a6fce642b03fd63f2'  # введите свой API, этот указан для примера
        get_number_url = f'https://onlinesim.ru/api/getNum.php?apikey=' \
            f'{api_key}&service=wildberries&number=1'

        get_number = requests.get(get_number_url)
        get_number = json.loads(get_number.text)
        my_number = get_number['number']
        my_number = my_number[2:]
        my_tzid = get_number['tzid']
        print(f"Номер телефона: {my_number}")
        driver.get_screenshot_as_file(f'{my_number}\\{my_number}.png')

        # Авторизируемся на сайте:

        login_menu = driver.find_element_by_link_text('Войти')
        login_menu.click()
        sleep(4)
        input_number = driver.find_element_by_class_name('input-item')
        input_number.send_keys(my_number)
        sleep(1)
        driver.save_screenshot('\\'+my_number+'\\'+my_number+'.png')
        other_pc = driver.find_element_by_class_name('item-checkbox-decor')
        other_pc.click()
        sleep(1)
        get_sales = driver.find_element_by_class_name('item-checkbox-text')
        get_sales.click()
        sleep(1)
        request_code = driver.find_element_by_id('requestCode')
        request_code.click()
        sleep(15)



        # Получаем код из сервиса OnlineSim:

        get_code_url = f'https://onlinesim.ru/api/getState.php?apikey' \
            f'={api_key}'
        params = {
            'tzid': my_tzid,
            'message_to_code': '1'
        }
        get_code_req = requests.get(get_code_url, params=params)
        get_code = json.loads(get_code_req.text)
        get_code = get_code[0]
        try:
            code = get_code['msg']
        except Exception:
            code = ''
            print('Смс не пришло')
        print(code)
        sleep(2)

        # Вводим код на сайте Wildberries:

        input_code = driver.find_element_by_css_selector('.symbols-4')
        input_code.send_keys(code)
        sleep(4)


        def like_product(product_id, product_keywords):
            nonlocal my_number
            while True:
                product_keyword = random.choice(product_keywords)
                search_tb = driver.find_element_by_id('tbSrch')
                search_tb.clear()
                search_tb.send_keys(product_keyword)
                search_tb.send_keys(Keys.ENTER)
                sleep(2)
                result = None
                for i in range(2, 10000):
                    try:
                        tovar = driver.find_element_by_id(f'c{product_id}')
                        tovar.click()
                        sleep(2)
                        like_button = driver.find_element_by_class_name('to-poned')
                        like_button.click()
                        # product_screen_name = my_number + '\\' + \
                        #                       product_keyword + '.png'
                        driver.save_screenshot(f'{product_id}.png')
                        sleep(1)
                        result = 'Like OK'
                        print(product_keyword, ': ', result)
                        return result
                    except Exception:
                        try:
                            next_page = driver.find_element_by_link_text(str(i))
                            next_page.click()
                            sleep(1)
                        except Exception:
                            print(f"{product_keyword}: Товар не найден")
                            result = 'Product not found'
                            return result


        for key, value in products.items():
            like_product(key, value)


        sleep(3)
        driver.close()
    get_like(products)

if __name__ == '__main__':
    for _ in range(n):
        get_likes()
