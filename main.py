from pathlib import Path
import xml.etree.ElementTree as ET

xml_folder_path = Path(__file__).parent / "export" # Папка где хранятся xml файлы

# получаем рнк и докЕИС
def input_rnk():
    with open('input.txt', 'r', encoding='utf-8') as file:
        result = {}
        for i, line in enumerate(file, 1):
            if line.strip():
                result[i] = line.strip().split()
    return result

def create_output():
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write('Подгрузите пожалуйста приёмку\n')
# парсим все xml файлы в xml_folder_path
def search_in_xml_files(folder_path, rnk, dokEIS):
    found_files = []
    
    for xml_file in folder_path.glob('*.xml'):
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

dict_rnk = input_rnk() # Получаем словарь со всеми рнк и ид
create_output() # создаём или очищаем файл output.txt

# перебираем все элементы полученные рнк
for key, value in dict_rnk.items():
    rnk = value[0]
    new_name_file = f'{rnk}.xml'
    dokEIS = value[1:]
    print(f"\nПоиск для РНК: {rnk} и ДокЕИС: {dokEIS}")
    search_rnk = search_in_xml_files(xml_folder_path, rnk, dokEIS) # передаём в функцию search_in_xml_files рнк и список из докЕИС
    
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
                    file.write(f"ДокЕИС - {', '.join(doks)}, найдены не все ДокЕИС ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n\n")
    else:
        print(f"РНК {rnk} не найден ни в одном файле [FAIL]")
        with open('output.txt', 'a', encoding='utf-8') as file:
            file.write(f'РНК - {rnk} Не обнаружен ❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌\n\n')
    print('-' * 100)