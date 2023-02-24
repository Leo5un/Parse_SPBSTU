import requests
import matplotlib
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import sys


def check_link(choise, data_time, number_group, name_teacher):
    if choise == 1:
        add_link = number_group.replace('/', '%2F').replace(' ', '%20')
        url = 'https://ruz.spbstu.ru/search/groups?q='+add_link
        #print(url)
    else:
        add_link = name_teacher.replace(' ', '%20')
        url = 'https://ruz.spbstu.ru/search/teacher?q='+add_link

    print(url)

    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')

    found = soup.find('div', class_='schedule-page')
    #print(found.text)
    if found.text.find("не найдены") == -1:
        print('link good')
    else:
        sys.exit('Ошибка поиска, попробуйте ввести параметры заново!')

    if choise == 1:
        list_gr = soup.find_all('li', class_='groups-list__item') # кол-во груп на странице
    else:
        list_gr = soup.find_all('li', class_='search-result__item') #кол-во преподов на странице

    if len(list_gr) == 1:
        if choise == 2:
            url = 'https://ruz.spbstu.ru'+list_gr[0].find('a', class_='search-result__link').get('href')
        else:
            url = 'https://ruz.spbstu.ru'+list_gr[0].find('a', class_='groups-list__link').get('href')
    else:
        sys.exit('Ошибка поиска, попробуйте ввести параметры заново!\
                  Пользователей с таким ФИО >1')

    #print(url1)
    #data_time.split('.')
    #print(data_time.split('.')[0])
    url = url + f'?date=20{data_time.split(".")[2]}-{data_time.split(".")[1]}-{data_time.split(".")[0]}'
    print(url)

#url = "https://ruz.spbstu.ru/faculty/122/groups"
#url1= "https://ruz.spbstu.ru/faculty/124/groups/36631"
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    performance = [0, 0, 0, 0, 0, 0]
    prime_week = soup.find('h3', class_='page__h3')
    print(prime_week.text)
    # if prime_week.text.find('нечётная') == -1:
    #     print('чётная')
    # else:
    #     print('нечётная')
    list_shedule = soup.find_all('li', class_='schedule__day')
    if len(list_shedule) == 0:
        sys.exit('Расписание отсутсвует на выбранные даты')
    for day in list_shedule:
        dayOfweek = day.find('div', 'schedule__date')
        list_lesson = day.find_all('li', class_='lesson')
        # performance.append(len(list_lesson))
        # print(len(list_lesson))
        #print(day.find('div', 'schedule__date').text.split(',')[1])
        match (day.find('div', 'schedule__date').text.split(',')[1]):
            case " пн":
                performance[0] = len(list_lesson)
            case " вт":
                performance[1] = len(list_lesson)
            case " ср":
                performance[2] = len(list_lesson)
            case " чт":
                performance[3] = len(list_lesson)
            case " пт":
                performance[4] = len(list_lesson)
            case " сб":
                performance[5] = len(list_lesson)
            case _:
                print('error')
        fl=0
        for lesson in list_lesson:
            #time = lesson.find('span', class_='lesson__time')
            
            subject = lesson.find('div', class_='lesson__subject')
            #print(subject.text)
            place = lesson.find('div', class_='lesson__places').find('a', 'lesson__link')
            # print(dayOfweek.text.split()[0])
            # print(data_time.split()[0])
            if dayOfweek.text.split()[0] == data_time.split('.')[0]:
                if fl == 0:
                    fl = 1
                    print(dayOfweek.text)
                try:
                 #   print(dayOfweek.text)
                    teacher = lesson.find('div', class_='lesson__teachers').find('a', class_='lesson__link')
                    print(f'{subject.text} {place.text} {teacher.text}')
                except Exception:
                    print(f'{subject.text} {place.text}')
    if fl == 0:
        print(data_time, 'Нет пар')
    #print(performance)
    objects = ('Понедельник', 'Вторник', 'Cреда', 'Четверг', 'Пятница', 'Суббота')
    y_pos = np.arange(len(objects))

    plt.bar(y_pos, performance, align='center', alpha=1.0)
    plt.xticks(y_pos, objects)
    plt.ylabel('Количество пар')
    plt.title('Расписание на неделю')
    plt.show()
        # print(f'{subject.text} {place.text} {teacher.text}')
            #print(place.text)
            
            #try:
            #    teacher = lesson.find('div', class_='lesson__teachers').find('a', class_='lesson__link')
            #    #print(teacher.text)
            #except: 
            #    print()
            #print(time + ' ' + subject + ' ' + teacher)
            #print()


def inp():
    choise = 1
    data_time = '01.03.25'
    number_group = '4831001/10003'
    name_teacher = 'Ульянова Нина Сергеевна'
    #name_teacher = 'Ульянова'
    check_link(choise, data_time, number_group, name_teacher)
    # while True:
    #     try:
    #         choise = int(input("1 - Расписание по номеру группы\n\
    #                             \r2 - Расписание по преподавателю\n"))
    #         data_time = input("Введите дату в формате ДД.ММ.ГГ: ")
    #         if choise == 1:
    #             number_group = input("Введите номер группы: ")
    #         else:
    #             name_teacher = input("Введите ФИО преподавателя: \n")
    #         if choise == 1 or choise == 2:
    #             break
    #         else:
    #             print('Некорретный ввод')
    #     except ValueError:
    #         print('Некорретный ввод')
    #print(choise, data_time, number_group)
    #parse(choise, data_time)
    

def __main__():
    inp()


if __name__ == "__main__":
    __main__()