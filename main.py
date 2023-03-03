import os
from datetime import datetime
from dateutil import parser

# Считываем имена файлов из исходного файла
with open('чеки.txt', 'r', encoding='utf-8') as f:
    filenames = [line.strip() for line in f.readlines()]

# Создаем папки для каждого месяца и перемещаем файлы в соответствующие папки
for filename in filenames:
    parts = filename.split('_')
    month_str = parts[1].capitalize()
    try:
        month = parser.parse(month_str).strftime('%m')
    except ValueError:
        print(f'Не удалось распознать месяц в файле {filename}')
        continue
    folder_path = os.path.join(month, '')
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    old_path = os.path.join('', filename)
    new_path = os.path.join(folder_path, filename)
    os.rename(old_path, new_path)

# Формируем файл с информацией о неоплаченных услугах
with open('чеки_по_папкам.txt', 'w', encoding='utf-8') as f:
    for month_num in range(1, 13):
        month = datetime(1900, month_num, 1).strftime('%B').lower()
        folder_path = os.path.join(month, '')
        files = os.listdir(folder_path)
        services = set([filename.split('_')[0] for filename in files])
        unpaid_services = []
        for service in services:
            service_files = [filename for filename in files if filename.startswith(service)]
            if len(service_files) < 1:
                unpaid_services.append(service)
        if unpaid_services:
            f.write(f'не оплачены:\nмесяц: {month}\n')
            for service in unpaid_services:
                f.write(f'{service}\n')
            f.write('\n')
