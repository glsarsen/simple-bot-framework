from itertools import islice

BG_COLOR = "#FFFFFF"
BUTTON_BG_COLOR = "#69C48A"

START_MESSAGE = {
    "Type": "rich_media",
    "BgColor": BG_COLOR,
    "ButtonsGroupRows": 3,
    "Text": "Testing richmedia text",
    "Buttons": [
        {
            "Columns": 6,
            "Rows": 2,
            "Silent": "true",
            "ActionType": "none",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "Text": "Добро пожаловать в компанию!\nЧтобы подписаться на бота нажми кнопку 'Начать'",
        },
        {
            "Columns": 6,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_start",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 99,
            "Text": "Начать",
        },
    ],
}

SHARE_PHONE_MENU = {
    "Type": "keyboard",
    "BgColor": BG_COLOR,
    "Buttons": [
        {
            "Columns": 6,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "share-phone",
            "ActionBody": "no_phone",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 99,
            "Text": "Поделиться",
        }
    ],
}

NEW_USER_MENU = {
    "Type": "keyboard",
    "BgColor": BG_COLOR,
    "Buttons": [
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_new_user",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 99,
            "Text": "Новый сотрудник",
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 99,
            "Text": "Уже работаешь с нами",
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_restart",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 99,
            "Text": "Вернуться на старт",
        },
    ],
}

EMPLOYED_USER_MENU = {
    "Type": "keyboard",
    "BgColor": BG_COLOR,
    # "CustomDefaultHeight": 40, # percent of screen to keyboard 40..70
    # "ButtonsGroupColumns": 2,
    "Buttons": [
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_google",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 99,
            "Text": "Гугл",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_linkedin",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 99,
            "Text": "Линкедин",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_CRM",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "СРМ",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_calendar",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Календарь",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_update",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Апдейт",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_time_tracker",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Тайм-трекер",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_contacts",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Контакты",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_bonus_n_salary",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Бонусы и ЗП",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_leads",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Лиды",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_templates",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Шаблоны",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_connect",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Коннект",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_followup",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Фоллоуап",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_country",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Страна",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_questions_status",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Статус",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_restart",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Вернуться на старт",
            "TextPaddings": [0, 0, 0, 0],
        },
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_feedback",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Обратная связь",
            "TextPaddings": [0, 0, 0, 0],
        },
    ],
}


FEEDBACK_MENU = {
    "Type": "keyboard",
    "BgColor": BG_COLOR,
    "Buttons": [
        {
            "Columns": 2,
            "Rows": 1,
            "BgColor": BUTTON_BG_COLOR,
            "Silent": "true",
            "ActionType": "reply",
            "ActionBody": "_restart",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Вернуться назад",
        }
    ],
}

EMPTY_MENU = None


def buttons(buttons_dict: dict):
    """generates buttons JSON

    Args:
        buttons_dict (dict): dictionary of "button_name": "element_tree_tag"

    Returns:
        dict: buttons JSON
    """
    buttons_count = len(buttons_dict) if 0 < len(buttons_dict) <= 7 else 7
    RICH_MEDIA = {
        "Type": "rich_media",
        "BgColor": BG_COLOR,
        "ButtonsGroupRows": buttons_count,
        # "ButtonsGroupRows": 1, # it has no effect compared to previous line somehow
        "Buttons": [],
    }
    for key, value in buttons_dict.items():
        RICH_MEDIA["Buttons"].append(
            {
                "Columns": 6,
                "Rows": 1,
                "BgColor": BUTTON_BG_COLOR,
                "Silent": "true",
                "ActionType": "reply",
                "ActionBody": value,
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "TextOpacity": 100,
                "Text": key,
                "TextPaddings": [0,0,0,0],
            }
        )
    return RICH_MEDIA


def urls(urls_dict: dict):
    """generates buttons with urls JSON

    Args:
        urls_dict (dict): dictionary of "button_name": "url"

    Returns:
        dict: buttons with urls JSON
    """
    urls_count = len(urls_dict) if 0 < len(urls_dict) <= 7 else 7
    RICH_MEDIA = {
        "Type": "rich_media",
        "BgColor": BG_COLOR,
        "ButtonsGroupRows": urls_count,
        "Buttons": [],
    }
    for key, value in urls_dict.items():
        RICH_MEDIA["Buttons"].append(
            {
                "Columns": 6,
                "Rows": 1,
                "BgColor": BUTTON_BG_COLOR,
                "Silent": "true",
                "ActionType": "open-url",
                "ActionBody": value,
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "TextOpacity": 100,
                "Text": key,
            }
        )
    return RICH_MEDIA

def chunks(data, size):
    it = iter(data)
    for _ in range(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}
