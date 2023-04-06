from itertools import islice

# from flask import url_for
# from wsgi import app
# TODO: VERY HACKY - redo with app.app_context !!!
from config import SERVER 

BG_COLOR = "#FFFFFF"
BUTTON_BG_COLOR = "#69C48A"

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

def keyboard(buttons_dict: dict, image=False):
    """generates keyboard JSON

    Args:
        buttons_dict (dict): dictionary of "button_name": "element_tree_tag"

    Returns:
        dict: keyboard JSON
    """
    
    KEYBOARD = {
        "Type": "keyboard",
        "BgColor": BG_COLOR,
        "DefaultHeight": "false",
        "Buttons": [],
    }
    
    for key, value in buttons_dict.items():
        KEYBOARD["Buttons"].append(
            {
                "Columns": 2,
                "Rows": 1,
                "BgColor": BUTTON_BG_COLOR,
                "Silent": "true",
                "ActionType": "reply",
                "ActionBody": value,
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "TextOpacity": 100,
                "Text": key,
                # "TextPaddings": [0,0,0,0],
            }
        )
        
    if image:
        for button in KEYBOARD["Buttons"]:
            button["BgMediaType"] = "picture"
            
    return KEYBOARD


def chunks(data, size):
    """slicing buttons into groups of size

    Args:
        data (_type_): dict with buttons
        size (_type_): size of chunks

    Yields:
        _type_: _description_
    """
    it = iter(data)
    for _ in range(0, len(data), size):
        yield {k:data[k] for k in islice(it, size)}

START_MESSAGE = {
    "Type": "rich_media",
    "BgColor": BG_COLOR,
    "ButtonsGroupRows": 3,
    # "Text": "Testing richmedia text",
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
            "TextOpacity": 100,
            "Text": "Начать",
        },
    ],
}

# not used for now cause of inability to share pgone number from PC
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
            "ActionBody": "_no_phone",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 100,
            "Text": "Поделиться",
        }
    ],
}

NEW_USER_MENU = keyboard({
    "Новый сотрудник": "_new_user",
    "Уже работаешь с нами": "_questions",
    "Вернуться на старт":"_restart",
})

EMPTY_MENU = {
    "Type": "keyboard",
    "Buttons": [{"Text": ""}],
}

EMPLOYED_USER_MENU = keyboard({
    "Гугл": "_questions_google", # 0
    "Линкедин": "_questions_linkedin", # 1
    "СРМ": "_questions_CRM",
    "Календарь": "_questions_calendar",# 3
    "Апдейт": "_questions_update",
    "Тайм-трекер": "_questions_time_tracker", #5
    "Контакты": "_questions_contacts",
    "Бонусы и ЗП": "_questions_bonus_n_salary", # 7
    "Лиды": "_questions_leads",
    "Шаблоны": "_questions_templates", # 9
    "Коннект": "_questions_connect",
    "Фоллоуап": "_questions_followup", # 11
    "Страна": "_questions_country",
    "Статус": "_questions_status", # 13
    "Вернуться на старт": "_restart",
    "Обратная связь": "_feedback", # 15
}, image=True)


EMPLOYED_USER_MENU["Buttons"][0]["Image"] = "https://img.icons8.com/dotty/512/corgi.png"
# EMPLOYED_USER_MENU["Buttons"][0]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2030.png"
EMPLOYED_USER_MENU["Buttons"][1]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2031.png"
EMPLOYED_USER_MENU["Buttons"][2]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2032.png"
EMPLOYED_USER_MENU["Buttons"][3]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2030-1.png"
EMPLOYED_USER_MENU["Buttons"][4]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2031-1.png"
EMPLOYED_USER_MENU["Buttons"][5]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2032-1.png"
EMPLOYED_USER_MENU["Buttons"][6]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2029.png"
EMPLOYED_USER_MENU["Buttons"][7]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2033.png"
EMPLOYED_USER_MENU["Buttons"][8]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2034.png"
EMPLOYED_USER_MENU["Buttons"][9]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2028.png"
EMPLOYED_USER_MENU["Buttons"][10]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2036.png"
EMPLOYED_USER_MENU["Buttons"][11]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2035.png"
EMPLOYED_USER_MENU["Buttons"][12]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2027.png"
EMPLOYED_USER_MENU["Buttons"][13]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2037.png"
EMPLOYED_USER_MENU["Buttons"][14]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2038.png"
EMPLOYED_USER_MENU["Buttons"][15]["Image"] = SERVER + "/static/pictures/menu_2/Frame%2026.png"

# with app.app_context():
#     EMPLOYED_USER_MENU["Buttons"][0]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2030.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][1]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2031.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][2]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2032.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][3]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2030-1.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][4]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2031-1.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][5]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2032-1.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][6]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2029.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][7]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2033.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][8]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2034.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][9]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2028.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][10]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2036.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][11]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2035.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][12]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2027.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][13]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2037.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][14]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2038.png", _external=True)
#     EMPLOYED_USER_MENU["Buttons"][15]["BgMedia"] = url_for("static", filename="pictures/menu_2/Frame%2026.png", _external=True)


FEEDBACK_MENU = keyboard({
    "Вернуться назад": "_restart",
})

QUESTIONS_GOOGLE = keyboard({
    "Создать хром-пользователя": "_questions_create_chrome_user",
    "Найти коллег через Гугл": "_questions_find_colleagues",
    "Где Гугл-календарь": "_questions_find_calendar",
    "Операторы поиска Гугл": "_questions_google_search_operators",
    "Полезные расширения": "_questions_useful_extensions",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_LINKEDIN = keyboard({
    "Чистка старых заявок": "_questions_cleaning_old_orders",
    "Бан аккаунта": "_questions_account_ban",
    "Лимиты на аккаунте": "_questions_account_limits",
    "Как поменять страну": "_questions_how_to_change_country",
    "В какой вкладке найти лидов": "_questions_which_tab_to_look_for_leads",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_CRM = keyboard({
    "Как зайти в СРМ": "_questions_how_enter_CRM",
    "Как получить доступ": "_questions_how_to_get_access",
    "Аккаунт для работы в СРМ": "_questions_accounts_for_CRM",
    "Как добавить лида": "_questions_how_to_add_lead",
    "Вкладка Leads": "_questions_leads_tab",
    "Вкладка Lead Reports": "_questions_lead_reports_tab",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_CALENDAR = keyboard({
    "Почта для входа": "_questions_mail_for_login",
    "Ивент в календаре лида": "_questions_event_in_lead_calendar",
    "Внести ивент в календарь": "_questions_new_event_to_calendar",
    "Где взять календарь": "_questions_where_to_get_calendar",
    "Фоллоу-ап в календаре": "_questions_followup_in_calendar",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_UPDATE = keyboard({
    "Что такое апдейт": "_questions_what_update_is",
    "Зачем нужен апдейт": "_questions_why_update_needed",
    "Как найти апдейтов": "_questions_how_to_find_update",
    "Как сделать апдейт": "_questions_how_to_do_update",
    "Норма апдейтов в день": "_questions_standart_update_count",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_TIME_TRACKER = keyboard({
    "Включить тайм-трекер": "_questions_enable_time_tracker",
    "Настройка GoogleChrome": "_questions_google_chrome_setup",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_BONUS_N_SALARY = keyboard({
    "Мои бонусы": "_questions_my_bonuses",
    "Когда ЗП": "_questions_when_salary",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_LEADS = keyboard({
    "Каких лидов нужно искать": "_questions_which_leads_to_look_for",
    "Данные от лида": "_questions_data_from_lead",
    "Добавить лида": "_questions_add_lead",
    "Заполнить карту лида": "_questions_fill_lead_chart",
    "Кому делать фоллоу-ап": "_questions_when_to_follow_up",
    "Правильные лиды": "_questions_which_leads_to_look_for",
    "Сколько лидов я сделал": "_questions_how_much_leads_i_made",
    "Норма лидов в день": "_questions_standart_lead_count",
    "Как найти нужного лида": "_questions_how_to_find_correct_lead",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_TEMPLATES = keyboard({
    "1-й коннект с лидом": "_questions_first_lead_connect",
    "2-й коннект с лидом": "_questions_second_lead_connect",
    "3-й коннект с лидом": "_questions_third_lead_connect",
    "О специальностях": "_questions_about_specialities",
    "Об опыте сотрудников": "_questions_about_employees_experience",
    "Клиент не заинтересован": "_questions_client_not_interested",
    "Клиент заинтересован": "_questions_client_interested",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_CONNECT = keyboard({
    "1-й коннект с лидом": "_questions_first_lead_connect_2",
    "2-й коннект с лидом": "_questions_second_lead_connect_2",
    "3-й коннект с лидом": "_questions_third_lead_connect_2",
    "Отправить коннект лиду": "_questions_send_connect_to_lead",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_FOLLOWUP = keyboard({
    "Что такое фоллоу-ап": "_questions_what_is_follow_up",
    "Фоллоу-ап в календаре": "_questions_follow_up_in_calendar",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_COUNTRY = keyboard({
    "С какой страной я работаю": "_questions_country_i_work_with",
    "Можно ли изменить страну": "_questions_can_i_change_country",
    "Страны: *НЕ* работаем": "_questions_countries_not_working_with",
    "Страны: *работаем*": "_questions_countriues_working_with",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

QUESTIONS_STATUS = keyboard({
    "Статус при назначении ивента": "_questions_status_on_event",
    "Статус апдейт": "_questions_status_update",
    "Виды статусов в СРМ": "_questions_status_categories_in_CRM",
    "Обратная связь": "_feedback",
    "Назад": "_questions",
})

