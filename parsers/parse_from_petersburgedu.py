import asyncio

import requests
from bs4 import BeautifulSoup

PAKS_TO_WORK = 10
SITE_TO_PARSE = 'https://petersburgedu.ru'
ORG_ON_PAGE = 10
FILE_NAME = 'shools.csv'
COUNT_ORG_STRING_START = 'Найдено:'
COUNT_ORG_STRING_END = 'организаций'
LIST_DATA_TO_FIND = [
    'href',
    'Номер ОО',
    'Полное наименование ОО по Уставу',
    'Краткое наименование',
    'Адрес электронной почты',
    'Адрес ОО',
    'ОКТМО',
    'ОКПО',
    'Должность руководителя',
    'ФИО руководителя',
    'Организационно-правовая форма',
    'Тип ОО',
    'Вид ОО',
    'Телефон',
    'Район',
    'Расположение',
    'Подведомственность',
    'Статус сервиса "Электронный дневник"',
    'ОГРН',
    'Статус',
    'Адрес электронной почты из Параграф.Регион',
    'Тип местности',
    'Адрес сайта в сети Интернет',
    'Название',
    'Адрес электронной почты',
    'Адрес сайта',
    'Город',
    'Улица',
    'Дом',
    'Литерал',
    'Индекс',
    'Год постройки',
    'Количество мест',
    'ИНН',
    'КПП',
    'rosobr_id',
]


def value_clean(value):
    value = value.strip()
    return value


def get_pages(page, dict_detail_org):
    counter = (page - 1) * ORG_ON_PAGE
    response = requests.get(SITE_TO_PARSE + '/institution/content/search/page/' + str(page) + '?')
    soup = BeautifulSoup(response.text, 'html.parser')
    f = soup.find(attrs={'class': 'pbdou-search-results'})
    f = f.find(attrs={'class': 'list'})
    f = f.find_all(name='li')
    for org in f:
        counter += 1
        href_org = org.find(name='a', href=True)['href']
        dict_detail_org[counter] = {'href': href_org}
    return 0


def get_details(item_data):
    request_result = requests.get(SITE_TO_PARSE + item_data['href'])
    soup_text = BeautifulSoup(request_result.text, 'html.parser')
    data = soup_text.find_all("div", class_='row')
    for atr_school in data:
        if atr_school.b:
            b_info_atr = atr_school.b.text if atr_school.b.text[-1] != ' ' else atr_school.b.text[:-1]
            if 'ОУ' in b_info_atr:
                b_info_atr = b_info_atr.replace('ОУ', 'ОО')
                item_data[b_info_atr] = value_clean(atr_school.div.text)
                continue
            if b_info_atr in LIST_DATA_TO_FIND:
                item_data[b_info_atr] = value_clean(atr_school.div.text)
    return item_data


async def packet_work(pre_pages, count_pages, counter):
    dict_detail_org = {}
    print("### Collecting pre data ###")
    loop = asyncio.get_event_loop()
    tasks = []
    for page in range(pre_pages + 1, count_pages + 1):
        tasks.append(loop.run_in_executor(None, get_pages, page, dict_detail_org))
    for i in tasks:
        await i
    href_count = len(dict_detail_org)
    print('Hrefs collected: ', href_count)
    print("### Collecting data ###")

    tasks = []
    count_tasks_completed = 0
    count_percent = 0.043
    for key, item in dict_detail_org.items():
        tasks.append([loop.run_in_executor(None, get_details, item), key])
    for i in tasks:
        dict_detail_org[i[1]] = await i[0]
        count_tasks_completed += 1
        if count_tasks_completed > href_count * count_percent:
            count_percent += 0.043
            print('#', end='')
    await asyncio.sleep(0.3)
    print("")

    print("### Saving data ###")
    with open(FILE_NAME, 'a', encoding='UTF-8') as fh:
        for row in dict_detail_org.values():
            counter += 1
            row_str = str(counter) + ';'
            for atr in LIST_DATA_TO_FIND:
                if atr in row:
                    row_str += row[atr] + ';'
                else:
                    row_str += ';'
            fh.write(row_str + '\n')
    print("saved to " + FILE_NAME + ' Second part')
    return counter


async def main():
    dict_detail_org = {}
    r = requests.get(SITE_TO_PARSE + '/institution/content/search')
    soup = BeautifulSoup(r.text, 'html.parser')
    f = soup.find(attrs={'class': 'total-results-count'})
    text = f.text
    cont_org_start = text.find(COUNT_ORG_STRING_START) + len(COUNT_ORG_STRING_START)
    cont_org_end = text.find(COUNT_ORG_STRING_END)
    cont_org = int(text[cont_org_start:cont_org_end])
    count_pages = cont_org // ORG_ON_PAGE + 1
    all_pages = count_pages
    count_pages = round(count_pages / PAKS_TO_WORK)
    print("### Collecting pre data ###")
    loop = asyncio.get_event_loop()
    tasks = []
    for page in range(1, count_pages + 1):
        tasks.append(loop.run_in_executor(None, get_pages, page, dict_detail_org))
    for i in tasks:
        await i
    href_count = len(dict_detail_org)
    print('Hrefs collected: ', href_count)
    print("### Collecting data ###")

    tasks = []
    for key, item in dict_detail_org.items():
        tasks.append([loop.run_in_executor(None, get_details, item), key])
    for i in tasks:
        dict_detail_org[i[1]] = await i[0]

    print("### Saving data ###")
    with open(FILE_NAME, 'w', encoding='UTF-8') as fh:
        content = 'id;' + ';'.join([str(j) for j in LIST_DATA_TO_FIND])
        fh.write(content + '\n')
        counter = 0
        for row in dict_detail_org.values():
            counter += 1
            row_str = str(counter) + ';'
            for atr in LIST_DATA_TO_FIND:
                if atr in row:
                    row_str += row[atr] + ';'
                else:
                    row_str += ';'
            fh.write(row_str + '\n')
    del dict_detail_org
    print("saved to " + FILE_NAME + ' First part')

    for i in range(2, PAKS_TO_WORK):
        count_pages = round(all_pages / PAKS_TO_WORK) * i % all_pages
        pre_pages = round(all_pages / PAKS_TO_WORK) * (i - 1) % all_pages
        print('Page from ', pre_pages, ' to ', count_pages)
        counter = await packet_work(pre_pages, count_pages, counter)
    print('Page from ', count_pages, ' to ', all_pages)
    await packet_work(count_pages, all_pages, counter)


if __name__ == "__main__":
    asyncio.run(main())
