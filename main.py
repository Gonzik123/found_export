__version__ = "1.1"  

from pathlib import Path
import xml.etree.ElementTree as ET
import os
import sys


# Создаём или очищаем output.txt
def create_output():
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write('Подгрузите пожалуйста приёмку\n')

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable) # Если запущено через exe, возвращаем папку с исполняемым файлом
    else: # если запустили напрямую, возвращаем папку со скриптом
        return os.path.dirname(os.path.abspath(__file__))

# пути к файлам
BASE_DIR = Path(get_base_dir())
INPUT_FILE = BASE_DIR / "input.txt"
EXPORT_FOLDER = BASE_DIR / "export"
OUTPUT_FILE = BASE_DIR / "output.txt"


# получаем рнк и докЕИС
def input_rnk():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Файл {INPUT_FILE} не найден!")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        result = {i: line.split() for i, line in enumerate(file, 1)}
    return result

# парсим все xml файлы в xml_folder_path
def search_in_xml_files(rnk, dokEIS):
    found_files = []
    for xml_file in EXPORT_FOLDER.glob('*.xml'):
        try:
            tree = ET.parse(xml_file)
            file_content = ET.tostring(tree.getroot(), encoding='unicode')
            if str(rnk) in file_content:
                found_doks = [dok for dok in dokEIS if dok in file_content]
                if found_doks:
                    found_files.append((xml_file.name, found_doks))
                    
        except ET.ParseError as e:
            print(f"Ошибка в файле {xml_file.name}: {e}")
    
    return found_files

# перебираем все элементы полученные рнк
flag = True
while flag == True:
    dict_rnk = input_rnk() # Получаем словарь со всеми рнк и ид
    create_output() # создаём или очищаем файл output.txt
    for key, value in dict_rnk.items():
        rnk = value[0]
        # new_name_file = f'{rnk}.xml' 
        dokEIS = value[1:]
        print(f"\nПоиск для РНК: {rnk} и ДокЕИС: {dokEIS}")
        search_rnk = search_in_xml_files(rnk, dokEIS) # передаём в рнк и список из докЕИС
        
        if search_rnk:
            for file_name, doks in search_rnk:
                with open('output.txt', 'a', encoding='utf-8') as file:
                    file.write(f'РНК - {rnk}\n')
                    print(f"РНК {rnk} найдено в файле: {file_name} [OK]")
                    if doks == dokEIS:
                        print(f"Совпадения ДокЕИС: {', '.join(doks)} [OK]")
                        file.write(f"ДокЕИС - {', '.join(doks)}\n\n")
                    else:
                        print(f"Совпадения ДокЕИС: {', '.join(doks)}, найдены не все ДокЕИС [WARNING]")
                        file.write(f"ДокЕИС - {', '.join(doks)}, найдены не все ДокЕИС ⚠️⚠️\n\n")
        else:
            print(f"РНК {rnk} не найден ни в одном файле [FAIL]")
            with open('output.txt', 'a', encoding='utf-8') as file:
                file.write(f'РНК - {rnk} Не обнаружен ❌❌\n\n')
        print('-' * 100)
    while True:
        user_input = input("Введите 'next' для повторения или 'q' для выхода: ").strip().lower()
        if user_input == 'q':
            print("Завершаем программу...")
            flag = False
            break    
        elif user_input != 'next':
            print("Некорректный ввод. Попробуйте снова.")
        else:
            break