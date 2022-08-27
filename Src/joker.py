def load_about_info() -> str:
    from random import randint as r_int
    try:
        with open('Src/database/data/about_text.txt', 'r', encoding='utf-8') as about_fl:
            text = about_fl.read().split('\n\n')
    except FileNotFoundError:
        with open('database/data/about_text.txt', 'r', encoding='utf-8') as about_fl:
            text = about_fl.read().split('\n\n')
    return text[r_int(0, len(text)-1)]


def write_down_questionnaire(que_data: dict) -> None:
    import json
    answers = pick_up_questionnaire()
    answers[que_data.pop('uid')] = que_data
    try:
        with open('Src/database/data/questionnaire.json', 'w', encoding='utf-8') as out_fl:
            json.dump(answers, out_fl, indent=4, ensure_ascii=False, sort_keys=False)
    except FileNotFoundError:
        with open('database/data/questionnaire.json', 'w', encoding='utf-8') as out_fl:
            json.dump(answers, out_fl, indent=4, ensure_ascii=False, sort_keys=False)


def pick_up_questionnaire() -> dict:
    import json
    try:
        with open('Src/database/data/questionnaire.json', 'r', encoding='utf-8') as in_fl:
            data = in_fl.read()
            quest = json.loads(data)
    except FileNotFoundError:
        with open('database/data/questionnaire.json', 'r', encoding='utf-8') as in_fl:
            data = in_fl.read()
            quest = json.loads(data)
    return quest


if __name__ == '__main__':      # This part is testing only
    print(load_about_info())
    tmp = {
        "uid": "5000110001",
        "1": "gfdgh",
        "2": "hffhf",
        "3": "jgfj",
        "4": "gfe"
    }
    write_down_questionnaire(tmp)
    print(pick_up_questionnaire())
