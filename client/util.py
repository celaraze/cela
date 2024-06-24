import os

import yaml

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
        except KeyError:
            return lang_id
    except yaml.YAMLError:
        return lang_id
