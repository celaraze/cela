import os

import yaml
from datetime import datetime

CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.cela', 'config.yml')


def trans(lang_id: str):
    try:
        if not os.path.exists(CONFIG_FILE_PATH):
            print(trans("config_file_not_found"))
            exit(1)
        try:
            with open(CONFIG_FILE_PATH, "r") as f:
                content = yaml.safe_load(f)
                lang = content['lang']
        except KeyError:
            lang = "en_US"
        try:
            with open(f"client/langs/{lang}.yml", "r") as f:
                content = yaml.safe_load(f)
            return content[lang_id]
        except TypeError:
            return lang_id
        except KeyError:
            return lang_id
    except yaml.YAMLError:
        return lang_id


def calculate_todo_minutes(work_list):
    time_diffs = []
    is_doing = work_list[-1]['flag'] == 0
    if is_doing:
        now = datetime.now()
        work_list.append({
            'created_at': now.strftime("%Y-%m-%dT%H:%M:%S"),
            'is_done': False,
        })
    for i in range(0, len(work_list) - 1, 2):
        start = datetime.strptime(work_list[i]['created_at'], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(work_list[i + 1]['created_at'], "%Y-%m-%dT%H:%M:%S")
        diff = end - start
        record = {
            'start': start,
            'end': end,
            'diff': diff,
            'is_doing': False,
        }

        if (i == len(work_list) - 2) and is_doing:
            record['is_doing'] = True
        time_diffs.append(record)
    return time_diffs
