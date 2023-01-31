import os
from config import LOG_LEVEL
from config import CHECK_MINUTES
from datetime import datetime
from datetime import timedelta


def _get_list_of_log_files() -> list:
    """
    Получаем список файлов в директориях
    """
    projects_path = '../'
    log_files = []

    for root, dirs, files in os.walk(projects_path):
        for name in files:
            file_name = os.path.join(root, name)
            if '.log' in file_name:
                log_files.append(file_name)
                
    return log_files

def _get_level_rows(log_files : list) -> list:
    """
    Получаем строки в логах соответствующие заданному уровню. 
    """
    new_rows = []
    LOG_LEVELS = {'DEBUG' : ['DEBUG', 'INFO', 'WARNING', 'CRITICAL', 'FATAL'],
                    'INFO' : ['INFO', 'WARNING', 'CRITICAL', 'FATAL'],
                    'WARNING' : ['WARNING', 'CRITICAL', 'FATAL'],
                    'CRITICAL' : ['CRITICAL', 'FATAL'],
                    'FATAL' : ['FATAL'],
                    }
    for log in log_files:
        with open (log, 'r') as file:
            lines = file.readlines()
            for line in lines:
                for level in LOG_LEVELS[LOG_LEVEL]:
                    if level in line:
                        new_rows.append(line)
    
    return new_rows

def _get_rows_to_send(level_rows : list) -> list:
    """
    Получаем строки для отправки пользователю
    """
    rows_to_send = []
    for row in level_rows:
        row_time = row.split(' - ')[0].split(',')[0]
        future_time = datetime.now() + timedelta(minutes=-CHECK_MINUTES)
        future_time = future_time.strftime('%d.%b.%Y %H:%M')
        if row_time == future_time:
            rows_to_send.append(row)
            
    return rows_to_send


def parse_log_files() -> list:
    list_of_log_files = _get_list_of_log_files()
    level_rows = _get_level_rows(list_of_log_files)
    rows_to_send = _get_rows_to_send(level_rows)
    
    return rows_to_send
