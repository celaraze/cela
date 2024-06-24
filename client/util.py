import yaml

from client.services.config import read_lang


def trans(lang_id: str):
    try:
        lang = read_lang()
        with open(f"client/lang/{lang}.yaml", "r") as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
        return content[lang_id]
    except KeyError:
        return lang_id
