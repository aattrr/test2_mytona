from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import datetime as DT
import csv


# Функция для проверки введённых дат
def date_validate(start_date, end_date):
    try:
        DT.datetime.strptime(start_date, '%d.%m.%Y') and DT.datetime.strptime(end_date, '%d.%m.%Y')
    except:
        return False
    else:
        return True

print("Выгрузка курса валют ЦБ РФ за определённый период времени")
start_date_input = input('Введите начальную дату в формате DD.MM.YYYY: ')
end_date_input = input('Введите конечную дату в формате DD.MM.YYYY: ')


# Функция для парсинга и записи данных в csv файл
def parse(start_date_input, end_date_input):
    if not date_validate(start_date_input, end_date_input):
        raise ValueError("Ошибка ввода, пожалуйста повторите ввод в формате DD.MM.YYYY")

    start_date = DT.datetime.strptime(start_date_input, '%d.%m.%Y').date()
    end_date = DT.datetime.strptime(end_date_input, '%d.%m.%Y').date()

    # Создаём файл содержащий заголовок таблицы
    with open("exchange_rate.csv", "w", newline="") as f:
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONE)
        writer.writerow(["date", "currency_code", "rate"])

    day_count = (end_date - start_date).days + 1
    print('Идёт запись...')
    for single_date in (start_date + timedelta(n) for n in range(day_count)):

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.'
                                 '124 Safari/537.36 OPR/77.0.4054.203'}
        ENDPOINT_EXRATE = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' + single_date.strftime("%d/%m/%Y") + ''
        request_page = requests.get(ENDPOINT_EXRATE, headers)
        soup = BeautifulSoup(request_page.content, 'html.parser')

        # Находим все теги charcode и value, получаем содержащиеся в них значения и создаём словарь
        content = soup.find_all(["charcode", "value"])
        content = [every_td.getText() for every_td in content]
        content = dict(zip(content[::2], content[1::2]))

    # Дописываем данные за каждый день в exchange_rate.csv
        with open("exchange_rate.csv", "a", newline="") as f:
            writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONE)
            for key, value in content.items():
                writer.writerow([single_date.strftime("%Y-%m-%d"), key, value])

    f.close()
    print('Выполнена выгрузка в файл exchange_rate.csv за период: ' + start_date_input + '-' + end_date_input)


if __name__ == '__main__':
    parse(start_date_input, end_date_input)
