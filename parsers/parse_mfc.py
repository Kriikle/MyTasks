import re
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FILE_NAME = 'mfc_data.csv'
SITE_TO_OPEN = 'https://gu.spb.ru/mfc/list/?page=1'


def value_clean(value):
    value = str(value).replace("\n", " ")
    value = re.sub('\t+', ' ', value)
    value = re.sub(' +', ' ', value)
    return value


driver = webdriver.Firefox()
driver.get(SITE_TO_OPEN)

pages = driver.find_element(By.CLASS_NAME, 'pagination__list')
pages = pages.text.split('\n')
pages.remove('...')
count_pages = max([int(x) for x in pages])
data = []
print("### Start data parsing ###")
for page in range(count_pages):
    pre_len = len(data)
    sleep(1)
    elem_ui = driver.find_element(By.ID, 'content-list')
    elements = elem_ui.find_elements(By.CLASS_NAME, 'cols')
    for elem in elements:
        dict_elem = {}
        sector = ''
        title = elem.find_element(By.CLASS_NAME, 'title-usual').text
        if title.find('Сектор') != -1:
            sector = title[:len('Сектор') + 2]
            zone = title[len('Сектор') + 3:]
            address = elem.find_element(By.CLASS_NAME, 'paragraph-base').text
        elif title.find('МФЦ') != -1:
            sector = title[:len('МФЦ') + 1]
            zone = title[len('МФЦ') + 1:]
            address = elem.find_element(By.CLASS_NAME, 'paragraph-base').text
        else:
            address = title
            zone = ''
        time_work = elem.find_element(By.TAG_NAME, 'dd').text
        zone = zone.replace('для бизнеса', '')
        dict_elem['title'] = title
        dict_elem['sector'] = sector
        dict_elem['zone'] = zone
        dict_elem['address'] = address.replace(';', ',')
        dict_elem['time_work'] = time_work.replace(';', ',').replace('\n', ',')
        data.append(dict_elem)
        # print(dict_elem)

    for elem in data[pre_len:]:
        if elem['zone'] == "":
            continue
        detail_button = driver.find_element(By.XPATH, '//h3[text()="' + elem['title'] + '"]')
        detail_button.click()
        sleep(0.3)
        tel = driver.find_element(By.XPATH,
                                  '/html/body/div[1]/div/div[3]/div[6]/div/div/div[1]/section/div/dl/div[2]/dd').text
        elem['tel'] = tel.replace(';', ',')
        driver.back()
    sleep(1)
    print("% of pages: ", (page + 1) / count_pages, "page: ", page + 1, " of ", count_pages)
    if page + 1 == count_pages:
        break
    button_next = driver.find_element(By.XPATH, '//span[text()="Следующая"]')
    button_next.click()
driver.close()

print("### Saving data ###")
with open(FILE_NAME, 'w') as fh:
    content = 'id;' + ';'.join([str(j) for j in data[0].keys()])
    fh.write(content + '\n')
    counter = 0
    for row in data:
        counter += 1
        row_str = str(counter) + ';'
        for atr in data[0].keys():
            if atr in row:
                row_str += row[atr] + ';'
            else:
                row_str += ';'
        fh.write(row_str + '\n')
print("saved to " + FILE_NAME)