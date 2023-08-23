#   Тут і надалі під текою МОТЛОХ розуміється тека, що вказана користувачем в якості аргументу при запуску програми.
#   Програма створює поряд із текою МОТЛОХ теку SORTED, куди поміщає всі файли, знайдені в МОТЛОХ, та її вкладеннях.
#   При переміщенні назви всіх файлів транслітеруються. Пробіли, а також спецсімволи заміняються на "_". Розширення залишаються без змін.
#   В теці SORTED всі файли знаходяться у відповідних теках згідно розширення, а саме:
#           zip, gz, targ                           розпаковані у відповідні теки архіви, будуть знаходитись у теці ARCHIVES
#           mp3, ogg, wav, amr                      будуть знаходитись у теці AUDIO
#           doc, docx, txt, pdf, xls, xlsx, pptx    будуть знаходитись у теці DOCUMENTS
#           jpeg, png, jpg, svg                     будуть знаходитись у теці IMAGES
#           avi, mp4, mov, mkv                      будуть знаходитись у теці VIDEO
#           всі інші розширення                     будуть знаходитись у теці OTHERS
#   В процесі роботи програми генерується файл звіту ZVIT.TXT в якому наглядно відображено які файли де знаходяться, та їх попереднє 
#   місторозташування. Також під кожною групою файлів відображається їх кількість. А загальна кількість опрацьованих файлів є в кінці звіту.
#   Якщо при виконанні програма знайде попередню папку SORTED, користувачу буде повідомлено про це, а також запитано, чи потрібно продовжувати 
#   виконання програми, чи ні. Якщо користувач погоджується продовжувати, тека SORTED видаляється, та створюється знов з подальшим сортуванням.
#   Якщо користувач відмовляється від продовження роботи, програма завершує своє виконання, не вносячи ніякіх змін.
#   По закінченю роботи програми користувачу буде запропоновано видалити інформацію в попередньому вигляді, або зберегти її на 14 днів.
#   Якщо користувач погоджується на збереження інформації, тека МОТЛОХ переіменовується в теку ВИДАЛИТИ-ПІСЛЯ- та вказується дата, після якої
#   можна сміливо видаляти теку.  

import sys      
import re
import os
import shutil
import datetime

PATH = 'c:\Pastore\Py\Temp\Мотлох' # Строка аргументу, використовувалась при розробці.
sort_path = ''
root_path = ''
dic_arch = {}
dic_aud = {}
dic_doc = {}
dic_imag = {}
dic_oth = {}
dic_vid = {}
list_res = ['', '', '', '', '', '']
list_dic = [dic_arch, dic_aud, dic_doc, dic_imag, dic_oth, dic_vid]


def error_1(path_del): #    Функція помилки 1. Визивається коли програма знаходить результати попередньої роботи. Пропонує запит 
                        #   користувачу на вихід із програми, або продовження ії виконання.
    ans = ''
    print('Увага! Знайдено існуючи робочі теки програми! При продовжені роботи програми дані будуть перезаписані!')
    ans = input('Продовжувати? (Так/Ні)>>>')
    if ans.lower() == 'н' or ans.lower() == 'ні' or ans.lower() == 'n':
        print('Завершення роботи програми...')
        sys.exit()
    elif ans.lower() == 'т' or ans.lower == 'так' or ans.lower() == 'y':
        shutil.rmtree(path_del)
    else:
        print('Повторіть ввод, будь ласка...')
        error_1()


def format_res(ind, list_res, res): #   Функція перевіряє чи це є нове розширення файлу, якщо так, додає його до списку опрацьованих розширень.
    sovp = False
    res = ' ' + res
    for q in re.findall(' [a-zA-Z0-9]+', list_res[ind]):
        if res == q:
            sovp = True
            break
    if sovp == False:
        list_res[ind] += ' ' + res  
    return list_res


def last_chanse(PATH, root_path): # Функція інформує користувача про закінчення роботи програми, та пропонує вибір подальших дій.
    ans = ''
    date = datetime.datetime.now()
    res = date + datetime.timedelta(days=14)
    print('Робота програми завершена успішно. :) Сформовано теку SORTED поряд із Вашою текою, в якій класифіковані всі файли.')
    print('Детальний звіт в теці SORTED файлі ZVIT.TXT Попередня нформація ще доступна, тож будь ласка, оберіть, що з нею зробити?')
    print('     1. Видалити старі файли.')
    print(f'     2. Перейменувати стару теку {PATH} в ВИДАЛИТИ_ПІСЛЯ_{res.date()}.')
    while ans != '1' or ans != '2':    
        ans = input('?>>>')
        if ans == '1':
            shutil.rmtree(PATH)
            print(f'Видалення теки {PATH} успішно завершено.')
        elif ans == '2':
            shutil.move(PATH, root_path + '/ВИДАЛИТИ-ПІСЛЯ-' + str(res.date()))
            print(f'Стара тека успішно перейменовано в {root_path + "/ВИДАЛИТИ-ПІСЛЯ-" + str(res.date())}.')
            print('Не забудьте видалити теку після указаного сроку!')
            print('Завершення роботи програми.')
            sys.exit()
        else:
            print('Повторіть ввод, будь ласка...')


def make_dirs(PATH): #  Функція створює відповідні теки в теці, розташованій на ступінь вище переданого шляху. 
                     #  При наявності вже створеної будь якої з них, викликає функцію error_1.
    path_sorted = PATH
    os.chdir(path_sorted)
    os.chdir('..')
    path_sorted = os.getcwd()
    root_path = path_sorted
    if os.path.exists(os.path.join(path_sorted, 'sorted')) == True:
        error_1(os.path.join(path_sorted, 'sorted'))
    path_sorted = os.path.join(path_sorted, 'sorted')
    os.mkdir(path_sorted)
    os.mkdir(os.path.join(path_sorted, 'archives'))
    os.mkdir(os.path.join(path_sorted, 'audio'))
    os.mkdir(os.path.join(path_sorted, 'documents'))
    os.mkdir(os.path.join(path_sorted, 'images'))
    os.mkdir(os.path.join(path_sorted, 'others'))
    os.mkdir(os.path.join(path_sorted, 'video'))
    return path_sorted, root_path


def normalize(file_name): # Функція транслітерації імені файлу із заміною всіх спецзнаків та пробілів на "_". Розширення не змінюється.
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    res = ''
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION): # Злиття словників для в ітоговий для транслітерації
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()   
    print(file_name)
    file_name = os.path.splitext(file_name)[0]
    res = os.path.splitext(file_name)[1]
    print(res)
    file_name = file_name.translate(TRANS) # Транслітерація
    if file_name.isalnum() == False:  # Перевірка на входження до строки будь-яких елементів окрім цифр та літер, та заміна таких символів на '_'
        for ind in file_name:
            if (ind.isalnum() or ind.isdigit()) == False:
                file_name = file_name.replace(ind, '_', 1) 
    print(f'file name>>> {file_name}, res>>> {res}')
    file_name += res # Повертає розширення в ім'я файлу
    res = res[1::]
    print(f'file name>>>rrrr {file_name}, res>>> {res}')
    return file_name, res


def search_res(val_key, list_res):  # Функція формує список проаналізованих розширень для виводу в звіт до конкретної категорії файлів.
    dir_name = re.findall('\/[a-zA-Zа-яА-Я0-9._]+$', val_key)
    dir_name = val_key.replace(dir_name[0],'')
    str_name = re.findall('\/[a-zA-Zа-яА-Я0-9]+$', dir_name)
    if str_name[0] == '/archives':
        str_name = list_res[0]
    elif str_name[0] == '/audio':
        str_name = list_res[1]
    elif str_name[0] == '/documents':
        str_name = list_res[2]
    elif str_name[0] == '/images':
        str_name = list_res[3]
    elif str_name[0] == '/video':
        str_name = list_res[4]
    elif str_name[0] == '/others':
        str_name = list_res[5]
    return str_name, dir_name


def sort_arch(cur_path, file_obj, sort_path, filen, dic_arch):  # Функція копіює та розпаковує архів в теку з ім'ям файлу в нове місце розташування.
    print(f'Знайдено новий файл {filen}. Копіюємо...')
    shutil.copy2(cur_path + '/' + file_obj, sort_path + '/archives/' + filen)
    new_path = unpack_arch(filen, sort_path + '/archives/')
    dic_arch.update([(cur_path + '/' + file_obj, new_path)])


def sort_aud(cur_path, file_obj, sort_path, filen): # Функція копіює файл в відповідне нове місце розташування.
    print(f'Знайдено новий файл {filen}. Копіюємо...')
    shutil.copy2(cur_path + '/' + file_obj, sort_path + '/audio/' + filen)
    dic_aud.update([(cur_path + '/' + file_obj, sort_path + '/audio/' + filen)])
    

def sort_doc(cur_path, file_obj, sort_path, filen):  # Функція копіює файл в відповідне нове місце розташування.
    print(f'Знайдено новий файл {filen}. Копіюємо...')
    shutil.copy2(cur_path + '/' + file_obj, sort_path + '/documents/' + filen)
    dic_doc.update([(cur_path + '/' + file_obj, sort_path + '/documents/' + filen)])


def sort_imag(cur_path, file_obj, sort_path, filen): # Функція копіює файл в відповідне нове місце розташування.
    print(f'Знайдено новий файл {filen}. Копіюємо...')
    shutil.copy2(cur_path + '/' + file_obj, sort_path + '/images/' + filen)
    dic_imag.update([(cur_path + '/' + file_obj, sort_path + '/images/' + filen)])


def sort_vid(cur_path, file_obj, sort_path, filen): # Функція копіює файл в відповідне нове місце розташування.
    print(f'Знайдено новий файл {filen}. Копіюємо...')
    shutil.copy2(cur_path + '/' + file_obj, sort_path + '/video/' + filen)
    dic_vid.update([(cur_path + '/' + file_obj, sort_path + '/video/' + filen)])


def sort_oth(cur_path, file_obj, sort_path, filen): # Функція копіює файл в відповідне нове місце розташування.
    print(f'Знайдено новий файл {filen}. Копіюємо...')
    shutil.copy2(cur_path + '/' + file_obj, sort_path + '/others/' + filen)
    dic_oth.update([(cur_path + '/' + file_obj, sort_path + '/others/' + filen)])


def sorting(cur_path, sort_path, list_dic, list_res): # Функція сортування файлів за розширенням. Перебирає об'єкти в поточній теці, якщо об'єкт 
                                                      # є текою, - входить до рекурсивної перевірки. якщо об'єкт є файлом, копіює його у теку,
                                                      # що відповідає типу розширення.
    new_path = ''
    ind = 0
    for file_obj in os.listdir(cur_path):
        if os.path.isdir(os.path.join(cur_path, file_obj)) == True:          
            sorting(os.path.join(cur_path, file_obj), sort_path, list_dic, list_res)          
        elif os.path.isfile(os.path.join(cur_path, file_obj)) == True:
            filen, res = normalize('геморроидальная№ шишка4.exe')      #file_obj)
        print(f'file name>>> {filen}, res>>> {res}')
        sys.exit()
        #     if res.lower() == 'zip' or res.lower() == 'gz' or res.lower() == 'targ':
        #         sort_arch(cur_path, file_obj, sort_path, filen, dic_arch)
        #         ind = 0
        #         list_res = format_res(ind, list_res, res)
        #     elif res.lower() == 'mp3' or res.lower() == 'ogg' or res.lower() == 'wav' or res.lower() == 'amr':
        #         sort_aud(cur_path, file_obj, sort_path, filen)
        #         if list_res[1].find(res) == -1:
        #             list_res[1] = list_res[1] + ' ' + res          
        #     elif res.lower() == 'doc' or res.lower() == 'docx' or res.lower() == 'txt' or res.lower() == 'pdf' or res.lower() == 'xls'\
        #                                                                          or res.lower() == 'xlsx' or res.lower() == 'pptx':
        #         sort_doc(cur_path, file_obj, sort_path, filen)
        #         if list_res[2].find(res) == -1:
        #             list_res[2] = list_res[2] + ' ' + res
        #     elif res.lower() == 'jpeg' or res.lower() == 'png' or res.lower() == 'jpg' or res.lower() == 'svg':
        #         sort_imag(cur_path, file_obj, sort_path, filen)
        #         if list_res[3].find(res) == -1:
        #             list_res[3] = list_res[3] + ' ' + res
        #     elif res.lower() == 'avi' or res.lower() == 'mp4' or res.lower() == 'mov' or res.lower() == 'mkv':
        #         sort_vid(cur_path, file_obj, sort_path, filen)
        #         if list_res[4].find(res) == -1:
        #             list_res[4] = list_res[4] + ' ' + res
        #     else:
        #         sort_oth(cur_path, file_obj, sort_path, filen) 
        #         if list_res[5].find(res) == -1:
        #             list_res[5] = list_res[5] + ' ' + res

def unpack_arch(cur_file, cur_path):    # Функція розпаковки архіву, створює теку відповідно імені архиву, після розпаковки до неї, видаляє архів.
                                        # Якщо знаходить вже розпакований архів, видаляє його, та розпаковує наново.
    filen, res = normalize(cur_file)
    filen = filen.replace('.' + res, '')
    try:
        os.mkdir(cur_path + filen)
    except FileExistsError:
        shutil.rmtree(cur_path + filen)
        os.mkdir(cur_path + filen)
    shutil.unpack_archive(cur_path + cur_file, cur_path + filen)
    os.remove(cur_path + cur_file)
    return cur_path + filen


def write_file(sort_path, list_dic):    # Функція зберігає звіт до файлу SORTED\ZVIT.TXT. В процесі підготовки інформації до зберігання звертається
                                        # до функції search_res(), яка виконує пошук різманітних розширень опрацьованих програмою.
    print_str = ''
    all_num = 0
    with open(sort_path, 'w') as fa:
        for dicts in list_dic:
            num = 0
            fa.write(('-' * 187) + '\n')
            for dict_key, val_key in dicts.items():
                num += 1
                all_num += 1
                print_str = ('|{:>3}|{:<90}|{:<90}|\n'.format(num, val_key, dict_key))
                fa.write(print_str)
            fa.write(('-' * 187) + '\n')
            if num != 0:
                str_name, dir_name = search_res(val_key, list_res)
                fa.write('|Загалом ідентифіковано {} файл(а/ів) в теці {}. Знайдено файли з наступними розширеннями: {}\n'.format(str(num), dir_name, str_name))
        fa.write(('-' * 187) + '\n')
        fa.write('|Загалом відсортовано {} файл(а/ів)\n'.format(str(all_num)))
        fa.write(('-' * 187) + '\n')

# PATH = sys.argv[1]  # Считування місцезнаходження папки з командної строки. Прописано вище в константах.
sort_path, root_path = make_dirs(PATH)
sorting(PATH, sort_path, list_dic, list_res)
write_file(sort_path + '/ZVIT.TXT', list_dic)
last_chanse(PATH, root_path)
