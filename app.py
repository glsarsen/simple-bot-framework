import threading
import sched
import time

from flask import Flask, request, Response
from flask_migrate import Migrate
from flask_login import LoginManager

import simplebot.bot_messages as bm
from simplebot.viber_config import viber
from simplebot.config import SERVER, SSL_CONTEXT, HOST, PORT, DEVELOPMENT, SECRET_KEY
from simplebot.database import db
from simplebot.handler import ViberHandler
from simplebot.question_worker import QuestionWorker
from simplebot.message_tree import ElementTree
from simplebot.blueprints import stats_page, index_page, register_page, login_page, logout_page
from simplebot.admin import Admin # DB model imported to be visible for flask-migration


question_worker = QuestionWorker(
    intents_file="intents.json", model_file="data.pth")
element_tree = ElementTree()
rhandler = ViberHandler(question_worker=question_worker,
                        element_tree=element_tree)

element_tree.add_element("branch", "_start")
element_tree.add_element("keyboard", bm.EMPTY_MENU)
element_tree.add_element("text", "Добро пожаловать в компанию!")
element_tree.add_element("timer", 2)
element_tree.add_element("text", "Как тебя зовут?")
element_tree.add_element("input", "user_name")
element_tree.add_element(
    "text",
    "И введи свой номер телефона пожалуйста:\nНапиши телефон прямо в чат (В формате +38...)",
)
element_tree.add_element("input", "user_phone")
element_tree.add_element("action", "gs_write_user")
element_tree.add_element("trigger", "_restart")
element_tree.add_element("text", "Выбери нужный вариант в меню ниже:")
element_tree.add_element("keyboard", bm.NEW_USER_MENU)

element_tree.add_element("branch", "_new_user")
element_tree.add_element(
    "text", "Ты подписал *договор и заполнил карту сотрудника*?")
element_tree.add_element(
    "button",
    {"Сделано! Что дальше?": "_contract_done", "Еще нет.": "_contract_not_done"},
)
element_tree.add_element("branch", "_contract_not_done")
element_tree.add_element(
    "text", "Пожалуйста, напиши рекрутеру, который с тобой общался."
)
element_tree.add_element(
    "button", {"Далее": "_contract_done", "Обратная связь": "_feedback"}
)
element_tree.add_element("branch", "_contract_done")
element_tree.add_element("text", "Ты уже создал *Гугл-почту*?")
element_tree.add_element(
    "button",
    {
        "Сделано! Что дальше?": "_google_mail_done",
        "Еще нет, покажи как.": "_google_mail_not_done",
    },
)
element_tree.add_element("branch", "_google_mail_not_done")
element_tree.add_element(
    "text",
    'Окей. Я помогу тебе это сделать.\n*Зайди на Gmail и нажми "Создать аккаунт"*',
)
element_tree.add_element(
    "url", {"Gmail": "https://www.google.com/intl/uk/gmail/about/"}
)
element_tree.add_element("timer", 2)
element_tree.add_element("text", "Далее следуй инструкции Gmail...")
element_tree.add_element(
    "button", {"И вот еще подсказки": "_google_mail_not_done_2"})
element_tree.add_element("branch", "_google_mail_not_done_2")
element_tree.add_element(
    "text", 'Запрос на закрепление номера телефона к аккаунту - нажми "Пропустить"'
)
element_tree.add_element("timer", 2)
element_tree.add_element(
    "text",
    "*Номер телефона не указывай!*\nКак резервную почту, можешь указать - niko@rh-s.com\nУкажи свою дату рождения и свой пол.",
)
element_tree.add_element("timer", 2)
element_tree.add_element(
    "text",
    "*Принимай правила Google*, пролистывай их до конца.\nhttps://youtu.be/7rVH13AHp5o",
)
element_tree.add_element("timer", 2)
element_tree.add_element("text", "Вуаля! Почта готова!")
element_tree.add_element(
    "button", {"Круто! Что дальше?": "_google_mail_done",
               "Обратная связь": "_feedback"}
)
element_tree.add_element("branch", "_google_mail_done")
element_tree.add_element("text", "Ты уже настроил Хром-пользователя?")
element_tree.add_element(
    "button",
    {
        "Сделано! Что дальше?": "_chrome_user_done",
        "Нет, покажи как.": "_chrome_user_not_done",
    },
)
element_tree.add_element("branch", "_chrome_user_not_done")
element_tree.add_element(
    "text",
    "Окей. Я помогу тебе это сделать.\nОткрой браузер Гугл Хром. Нажми на окошко пользователя в верхнем правом углу. Кликай *Управлять пользователями*",
)
element_tree.add_element("timer", 3)
element_tree.add_element("picture", "хромпользователь1.png")
element_tree.add_element("timer", 3)
element_tree.add_element(
    "text",
    "Выбери *Добавить пользователя* в нижнем правом углу.\nНазови своего пользователя так *ИМЯ_LinkedIn*.\nДобавь аватарку.\nПоставь галочку *Создать ярлык этого профиля на рабочем столе*.\nНажми *Добавить*.",
)
element_tree.add_element("timer", 3)
element_tree.add_element("picture", "хромпользователь3.png")
element_tree.add_element("timer", 3)
element_tree.add_element(
    "text",
    "Подключи рабочую почту, которую ты создал, к Хром-пользователю.\nhttps://youtu.be/7rVH13AHp5o",
)
element_tree.add_element("timer", 10)
element_tree.add_element(
    "text",
    "Вуаля! Новый пользователь ГуглХром готов.\n_Автоматически откроется новая вкладка Хрома под новым пользователем_.\n_На рабочем столе появился ярлык для входа именно в этого пользователя_.",
)
element_tree.add_element(
    "button", {"Круто! Что дальше?": "_chrome_user_done",
               "Обратная связь": "_feedback"}
)
element_tree.add_element("branch", "_chrome_user_done")
element_tree.add_element("text", "Молодец!\nА *Линкедин-аккаунт* уже сделал?")
element_tree.add_element(
    "button",
    {
        "Сделано! Что дальше?": "_linkedin_account_done",
        "Еще нет, покажи, как.": "_linkedin_account_not_done",
    },
)
element_tree.add_element("branch", "_linkedin_account_not_done")
element_tree.add_element(
    "text", "Окей, я помогу тебе создать аккаунт на Линкедин\n_Нажми на кнопку_"
)
element_tree.add_element(
    "button", {"Шаг первый": "_linkedin_account_not_done_1"})
element_tree.add_element("branch", "_linkedin_account_not_done_1")
element_tree.add_element(
    "text",
    "1) Зайди на LinkedIn.\n2) Начни регистрацию.\n3) *Зарегистрируй профиль Линкедин на Гугл-почту, которую ты создал ранее*.\nВАЖНО: *вся информация в твоем профиле должна быть на английском* так, как вся переписка с лидами ведется именно на этом языке.\nhttps://youtu.be/SlvxQQTFFxg",
)
element_tree.add_element("url", {"LinkedIn": "https://www.linkedin.com/"})
element_tree.add_element("timer", 3)
element_tree.add_element("text", "Готов?\nПереходи ко второму шагу")
element_tree.add_element(
    "button", {"Шаг второй": "_linkedin_account_not_done_2"})
element_tree.add_element("branch", "_linkedin_account_not_done_2")
element_tree.add_element(
    "text",
    '*Укажи свои настоящие имя и фамилию на английском языке*.\nЗапрещено: указывать никнеймы или сокрашения имени.\n*Загрузи свое фото* \nПараметры фото: портрет, без лишнего фона, желательно более официальное.\n*Переведи профиль на английский язык*\nКак это сделать:\n- в правом верхнем углу ты видишь свое фото\n- нажми на стрелочку под фото\n- откроется меню\n- выбери "Язык/Language"\nЕсли готов, переходи к третьему шагу',
)
element_tree.add_element(
    "button", {"Шаг третий": "_linkedin_account_not_done_3"})
element_tree.add_element("branch", "_linkedin_account_not_done_3")
element_tree.add_element(
    "text",
    'Поле *Образование/Education*\nУкажи актуальные данные о своем высшем образовании на английском языке.\nЕсли ты еще студент, в поле "Дата окончания" укажи 2020 год или более ранний, а в поле "Дата начала" - год на 4-5 лет раньше.\nГотов? Жми кнопку',
)
element_tree.add_element(
    "button", {"Шаг четвертый": "_linkedin_account_not_done_4"})
element_tree.add_element("branch", "_linkedin_account_not_done_4")
element_tree.add_element(
    "text",
    "Поле *Опыт работы/Edit experience*\n*Заполни в точности по инструкции*\n- должность: Account manager\n- график работы: Full-time\n- компания: Remote Helpers\n- локация: твое текущее местоположение (Город, Украина)\n- время работы в компании: любой месяц/год до настоящего времени + поставь галочку to present.\nГотово? Жми кнопку",
)
element_tree.add_element(
    "button", {"Шаг пятый": "_linkedin_account_not_done_5"})
element_tree.add_element("branch", "_linkedin_account_not_done_5")
element_tree.add_element(
    "text",
    "Поле *Навыки/Skills*\n*Указывай скиллы на английском языке*.\nСписок твоих возможных скиллов:\n- Email marketing\n- Lead Generation\n- Social media marketing\n- Online Advertising\n- Data Analysis\n- Searching skills\n- Targeting\n- WordPress\n- English language\n- Design\n- и другие навыки из выпадающего списка.\n*Используй штук 5-8*\nГотово? Жми кнопку",
)
element_tree.add_element(
    "button", {"Шаг шестой": "_linkedin_account_not_done_6"})
element_tree.add_element("branch", "_linkedin_account_not_done_6")
element_tree.add_element(
    "text",
    "Замени *статус профиля*.\nКак это сделать:\n- открой свой профиль\n- нажми на карандашик справа от фото профиля\n- замени поле *Headline/Статус*\nВарианты замены:\n_Hire online full-time remote employees| Marketing| Content Managers| SMM| Designers| Devs_\n_Dedicated virtual assistants in Ukraine: Lead Generation| SMM| Media| Design| Developers_\n_Build your online team in few clicks| Lead Generation| Marketing| Media| Design| Devs_\nТебе не обязательно копировать слово в слово. Основной посыл: мы предлагаем клиентам расширить их команду, наняв удаленных сотрудников из Украины, специальности видите выше.\nГотово? Жми кнопку",
)
element_tree.add_element(
    "button", {"Шаг седьмой": "_linkedin_account_not_done_7"})
element_tree.add_element("branch", "_linkedin_account_not_done_7")
element_tree.add_element(
    "text",
    "*Красивая ссылка на твой профиль*\nКак это сделать:\n- зайди на свою страницу\n- _в правом верхнем углу наведи мышку на свое фото, откроется выпадающий список_\n- выбери на нем _View profile_\n- на открывшейся странице в правом верхнем углу нажимаем _Edit public profile & URL_\n- снова в правом верхнем углу нажми на _Edit your custom URL_, внизу будет твоя ссылка и значок карандаша\n- нажми на карандашик и удали все ненужные цифры и символы. Оставь только свое имя и фамилию.\n- нажми _Save_.\nURL обновится в течении нескольких минут.\nГотово? Жми кнопку",
)
element_tree.add_element(
    "button", {"Шаг восьмой": "_linkedin_account_not_done_8"})
element_tree.add_element("branch", "_linkedin_account_not_done_8")
element_tree.add_element(
    "text",
    "Расширь сеть своих контактов. Добавь в друзья своих коллег.\n*Вариант 1 - зайди на страницу компании Remote Helpers в Линкедин, в раздел сотрудники*\n*Вариант 2 - используй поиск в Гугл*\nsite:linkedin.com remote helpers",
)
element_tree.add_element(
    "url", {"Вариант 1": "https://www.linkedin.com/mynetwork/"})
element_tree.add_element(
    "url",
    {
        "Вариант 2": "https://www.google.com/search?q=site%3Alinkedin.com+remote+helpers&oq=site%3Alinkedin.com+remote+helpers&aqs=chrome.0.69i59j69i58j69i60.1079j0j7&sourceid=chrome&ie=UTF-8"
    },
)
element_tree.add_element("timer", 10)
element_tree.add_element("text", "Вуаля! Профиль в Линкедин готов!")
element_tree.add_element(
    "button", {"Далее": "_linkedin_account_done",
               "Обратная связь": "_feedback"}
)
# TODO: check access transferred tag
element_tree.add_element("branch", "_linkedin_account_done")
element_tree.add_element(
    "text", "*Отправь логин к Гугл-почте*\n*Пиши прямо в чат*")
element_tree.add_element("input", "google_login")
element_tree.add_element(
    "text", "*Отправь пароль к Гугл-почте*\n*Пиши прямо в чат*")
element_tree.add_element("input", "google_password")
element_tree.add_element(
    "text", "*Отправь логин к Линкедин*\n*Пиши прямо в чат*")
element_tree.add_element("input", "linkedin_login")
element_tree.add_element(
    "text", "*Отправь пароль к Линкедин*\n*Пиши прямо в чат*")
element_tree.add_element("input", "linkedin_password")
element_tree.add_element("text", "Спасибо!\nДля продолжения нажми _Далее_")
element_tree.add_element(
    "button", {"Далее": "_academy_registration", "Обратная связь": "_feedback"}
)
element_tree.add_element("action", "gs_write_user")
# TODO: add tag access_transferred
element_tree.add_element("branch", "_academy_registration")
element_tree.add_element(
    "text",
    "Теперь *нажми на кнопку и зарегистрируйся в нашей Академии*. \nДля регистрации можешь использовать данные гугл-почты, которую ты создал сегодня.\nЧтобы легче и быстрее начать работу в отделе Лидогенерации, мы создали целый курс.",
)
element_tree.add_element(
    "url", {"Академия RE": "https://oa-y.com/courses/lead-generation/"}
)
element_tree.add_element(
    "button", {"Далее": "_last_message", "Обратная связь": "_feedback"}
)
element_tree.add_element("branch", "_last_message")
element_tree.add_element("picture", "any_questions.jpg")
element_tree.add_element("text", "Я помогу найти ответы.\nНажми на кнопку.")
element_tree.add_element("button", {"Ответы": "_questions_start"})

######################################################
##  Employed user menu
######################################################

element_tree.add_element("branch", "_questions_start")
element_tree.add_element(
    "text",
    "Привет!\nТы находишься в меню, в котором собраны ответы на популярные вопросы по работе отдела LeadGeneration.\nВыбери категорию своего вопроса:",
)
element_tree.add_element("trigger", "_questions")
element_tree.add_element("keyboard", bm.EMPLOYED_USER_MENU)


######################################################
##  Google questions menu
######################################################

element_tree.add_element("branch", "_questions_google")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_GOOGLE)

element_tree.add_element("branch", "_questions_create_chrome_user")
element_tree.add_element(
    "text",
    "Я помогу тебе это сделать.\n*Открой браузер Гугл Хром*. Нажми на окошко пользователя в верхнем правом углу. Кликай *Управлять пользователями*.",
)
element_tree.add_element("picture", "хромпользователь1.png")
element_tree.add_element(
    "text",
    "Выбери *Добавить пользователя* в нижнем правом углу.\nНазови своего пользователя так *ИМЯ_LinkedIn*.\nДобавь аватарку.\nПоставь галочку *Создать ярлык этого профиля на рабочем столе*.\nНажми *Добавить*.",
)
element_tree.add_element("picture", "хромпользователь3.png")
element_tree.add_element(
    "text", "Подключи рабочую почту, которую ты создал, к Хром-пользователю."
)
element_tree.add_element(
    "text",
    "Вуаля! Новый пользователь ГуглХром готов.\n_Автоматически откроется новая вкладка Хрома под новым пользователем_.\n_На рабочем столе появился ярлык для входа именно в этого пользователя_.",
)
element_tree.add_element("branch", "_questions_find_colleagues")
element_tree.add_element(
    "text",
    "Чтобы *найти своих коллег с помощью Гугл-поиска и добавить из в друзья на Линкедин*, в строке поиска вбей оператор:\nsite:linkedin.com remote helpers",
)
element_tree.add_element(
    "url",
    {
        "Открой ссылку": "https://www.google.com/search?q=site%3Alinkedin.com+remote+helpers&oq=site%3Alinkedin.com+remote+helpers&aqs=chrome..69i57j69i58.980j0j7&sourceid=chrome&ie=UTF-8"
    },
)
element_tree.add_element("branch", "_questions_find_calendar")
element_tree.add_element(
    "text",
    "Где взять *Гугл-календарь* :\nОткрой новую вкладку в браузере гугл-хром.\n*В правом верхнем углу, нажми на меню *(в виде точек).\nОткроется меню расширений Гугл.\n*Выбери Календарь*\n_Если тебе нужно назначить ивент, открой календарь с корпоративной почты info@rh-s.com_.",
)
element_tree.add_element("branch", "_questions_google_search_operators")
element_tree.add_element(
    "text",
    "*Операторы поиска Гугл*\n*Поиск по должностям*\n- site : (адрес сайта) пробел (должности)\nпример: site:linkedin.com\nCEO - Такой запрос в гугле выдаст Вам все страницы на сайте линкедина упоминающие должности гендиректоров.\n- OR (заглавными буквами между словами через пробел)\nпример: site:linkedin.com CEO OR Founder OR Director\n- (Минус) - \nпример: site:linkedin.com CEO OR Founder OR Director -news -Institute -become -jobs -wewwork -amazon -netflix -million\n*Поиск по компаниям*\n- (Тире) – (ставятся между цифрами: 2-50)\nпример site:linkedin.com Company size: 2-50 employees\nИспользуем именно такие размеры компаний, потому что они прописаны в шаблонах самого LinkedIn – 2-50, 51-200, 201-500 и т.д.\n- AND - (совмещает оба запроса в поисковой выдаче)\nпример: site:linkedin.com Founded: 2005..2019 AND Company size: 51-200 employees\n- (Кавычки) “…” – фразовый оператор, используется для того, чтобы искать именно фразу, а не каждое слово по отдельности\nпример site:linkedin.com “Specialties: Email Marketing”\n- (звездочка) * \nпример: site:linkedin.com “Specialties: Email Marketing”*\n- Headquarters: (локация)\nпример: site:linkedin.com Founded: 2005..2019 AND Company size: 51-200 employees OR Headquarters: France",
)
element_tree.add_element("branch", "_questions_useful_extensions")
element_tree.add_element("text", "Полезные *расширения в гугл* для работы:")
element_tree.add_element(
    "url",
    {
        "Contact Out": "https://chrome.google.com/webstore/detail/find-anyones-email-contac/jjdemeiffadmmjhkbbpglgnlgeafomjo",
        "RocketReach": "https://chrome.google.com/webstore/detail/rocketreach-chrome-extens/oiecklaabeielolbliiddlbokpfnmhba",
        "Free VPN": "https://chrome.google.com/webstore/detail/free-vpn-for-chrome-vpn-p/majdfhpaihoncoakbjgbdhglocklcgno",
    },
)

######################################################
##  Linkedin questions menu
######################################################

element_tree.add_element("branch", "_questions_linkedin")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_LINKEDIN)
element_tree.add_element("branch", "_questions_cleaning_old_orders")
element_tree.add_element(
    "text",
    "Зайди на свой рабочий аккаунт на Линкедин.\nВверху перейди на *вкладку My Network*, справа нажми на *вкладку Manage*.\nТебе откроется вкладка с исходящими и входящими приглашениями.\nПерейди на *вкладку Sent*. Ты видишь список заявок, которые были отправлены лидам.\n*Нажми на кнопку Withdraw* и удали старый коннект.\nУдали все заявки которые были отосланы 2 и более недель назад.Если за это время лид не одобрил коннект, он будет висеть пока ты его не удалишь.\nПроводи такую чистку на всех своих рабочих аккаунтах.",
)
element_tree.add_element(
    "url",
    {
        "My network - Sent": "https://www.linkedin.com/mynetwork/invitation-manager/sent/"
    },
)
element_tree.add_element("branch", "_questions_account_ban")
element_tree.add_element(
    "text",
    "*Как избежать попадания в бан на Линкедин*\n1) Делай *паузы между повторяющимися действиями* (коннект, копирование инфы, рассылка и т.д.);\n2) C 10-ю коннектами не стучись в друзья к президенту;\n3) *Не спамить, вести себя максимально естественно*. Общение должно быть живым, хоть и построено в деловом стиле.\n4) Пользоваться *отдельным юзером Гугл Хрома для входа в свой Линкедин*.\n5) *Раздели работу на части*. Например, минут 10-15 добавляешь людей (каждые 30 секунд), потом переключаешься на рассылку писем по почте. И так несколько подходов.\n6) В идеале веди профиль. Максимально заполни аккаунт информацией, фото, постами. Это привлекает внимание потенциальных клиентов, которые САМИ захотят связаться с тобой. Система соцсети не подумает, что здесь что-то не так. Нужно также делать репосты из группы нашей компании, лайкай посты контактов.",
)
element_tree.add_element("branch", "_questions_account_limits")
element_tree.add_element(
    "text", "Если появился *лимит на аккаунте* Линкедин, *обратись к аккаунт-менеджеру*"
)
element_tree.add_element("text", "Влад\n+380981101090")
# TODO: change to contact
element_tree.add_element("branch", "_questions_how_to_change_country")
element_tree.add_element(
    "text",
    "_Твой аккаунт Линкедин закреплен за определенной страной. Эти данные может заменить только аккаунт-менеджер_",
)
element_tree.add_element("branch", "_questions_which_tab_to_look_for_leads")
element_tree.add_element(
    "text",
    "*Зайди* на свою страницу в Линкедин, затем *во вкладку My Network*, расположенную на верхней панели сайта.\nВнизу страницы ты найдешь все профили (connections), которые могут быть тебе полезны.",
)
element_tree.add_element(
    "url", {"My network": "https://www.linkedin.com/mynetwork/"})

######################################################
##  CRM questions menu
######################################################

element_tree.add_element("branch", "_questions_CRM")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_CRM)
element_tree.add_element("branch", "_questions_how_enter_CRM")
element_tree.add_element("text", "Зайди в СРМ.")
element_tree.add_element("url", {"СРМ RemoteHelpers": "https://crm-s.com/"})
element_tree.add_element(
    "text", "Используй доступы, которые выдал тебе наш аккаунт-менеджер."
)
element_tree.add_element("branch", "_questions_how_to_get_access")
element_tree.add_element(
    "text", "Доступы к СРМ и рабочим аккаунтам выдает аккаунт-менеджер. Напиши ему."
)
element_tree.add_element("text", "Влад\n+380981101090")
element_tree.add_element("branch", "_questions_accounts_for_CRM")
element_tree.add_element(
    "text",
    "Зайди в свою СРМ.\nНажми вкладку *Add new lead*\n*Выбери Линкедин-аккаунт, который закреплен за тобой* (аккаунт, который тебе выдал аккаунт-менеджер специально для работы)",
)
element_tree.add_element("url", {"СРМ RemoteHelpers": "https://crm-s.com/"})
element_tree.add_element("branch", "_questions_how_to_add_lead")
element_tree.add_element(
    "text",
    "Чтобы *добавить лида в СРМ* :\n1) Открой СРМ\n2) Перейди на *вкладку Leads*, в правом верхнем углу нажми на *кнопку Add new lead*.\n3) Заполни необходимую информацию о лиде.\nПоля помеченые красной звездочкой* обязательно должны быть заполнены, иначе новый лид не будет сохранен.\n4) Поля, которые *заполняются автоматически: LG Manager, Lead Source, Lead Status и Country*.\n5) В *поле Linkedin accounts* выбери аккаунт на котором сейчас работаешь.\n6) В *поле Company* добавь компанию лида.\n7) В *Company Size, Industry и Position* выбери подходящий вариант из выпадающего списка.\n8) Нажми *Save*.",
)
element_tree.add_element("url", {"CRM RemoteHelpers": "https://crm-s.com/"})

element_tree.add_element("branch", "_questions_leads_tab")
element_tree.add_element(
    "text",
    "*Всех лидов ты можешь просмотреть во вкладке Leads в своей СРМ*.\nДля того, чтобы найти конкретного лида, используй фильтры.",
)

element_tree.add_element("branch", "_questions_lead_reports_tab")
element_tree.add_element(
    "text",
    "На *вкладке Lead Reports* ты можешь просмотреть всех лидов, которых ты внес в СРМ.\nДля удобства используй фильтры.\nНапоминаем - *норма 70-80 лидов в день*.",
)

######################################################
##  Calendar questions menu
######################################################

element_tree.add_element("branch", "_questions_calendar")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_CALENDAR)
element_tree.add_element("branch", "_questions_mail_for_login")
element_tree.add_element(
    "text", "Зайди в Гугл Календарь с корпоративной почты info@rh-s.com"
)
element_tree.add_element("branch", "_questions_event_in_lead_calendar")
element_tree.add_element(
    "text",
    "_Когда лид соглашается на звонок и сбрасывает ссылку на свой календарь, в нем нужно забронировать встречу в удобное и для нас, и для него время_\n*Перейди по ссылке, которую он отправил*.\n*Открой наш календарь. Здесь найди свободное время для звонка. Вернись в календарь лида и выбери дату и время, которые нам подходят*.\nВнизу *выбери наш часовой пояс (GMT +3)*. Время переводить не нужно, поскольку мы выбираем часы по киевскому времени.\nПосле того как ты *выбрал дату и время, нажми confirm*.\nЗаполни *название ивента, добавь почту sales@rh-s.com. В комментариях обязательно добавь описание ивента*.\nНажми *кнопку add guests, и добавь почту info@rh-s.com*.\nПодтверди и сохрани наш ивент в календаре клиента.\n*Зайди в наш календарь с почты info@rh-s.com*. Найди этот ивент, открой его и добавь всю необходимую информацию о клиенте, которая есть у тебя (сайты компаний, комментарий, имя менеджера и тд).",
)
element_tree.add_element("branch", "_questions_new_event_to_calendar")
element_tree.add_element(
    "text",
    "*Зайди в Гугл Календарь с корпоративной почты* info@rh-s.com .\n*Выбери дату и время*, на которые вы договорились с клиентом.\n*Учитывай часовые пояса* при назначении звонка. В календаре стоит Киевское время (GMT+2). Чтобы не считать время и быть точно уверенным в правильности, используй запрос в гугле: EST to Ukraine time. Гугл выдаст тебе ссылки на онлайн конверторы времени.\n*AM* – это ночное и утреннее время (с полночи 12am до полудня 12pm), *PM* – наоборот дневное и вечернее время (с полудня 12pm до полночи 12am).\nЗвонки вноси в календарь с ПН по ПТ, с 9:00 до 18:00. Любое другое время необходимо согласовать с Sales-отделом.",
)
element_tree.add_element(
    "url",
    {
        "EST to Ukraine time": "https://www.google.com/search?q=EST+to+Ukraine+time&oq=EST+to+Ukraine+time&aqs=chrome..69i57j0i22i30l2.1408j0j7&sourceid=chrome&ie=UTF-8"
    },
)
element_tree.add_element(
    "button", {"Далее": "_questions_add_event_to_calendar_2"})
element_tree.add_element("branch", "_questions_add_event_to_calendar_2")
element_tree.add_element(
    "text",
    'Выбери *кнопку "More options"* и перейди в расширенное меню настроек ивента.\nВажно - длительность ивента должна быть 30 мин. Обычно дольше разговор не длится.\nЗаполни пустые поля.\nЗаголовок *Сompany name - Remote Helpers*\nОписание:\nWe are going to discuss options for partnership in managing human resources for "Name of the partner-company" in Ukraine.\nWebsite: rh-s.com\nWebsite: "his website"',
)
element_tree.add_element(
    "button", {"Далее": "_questions_add_event_to_calendar_3"})
element_tree.add_element("branch", "_questions_add_event_to_calendar_3")
element_tree.add_element(
    "text",
    "Поле *Notifications/Напоминания*.\nРекомендуем ставить 2 напоминания: за 20 мин и за 10 мин.\nЕсли у тебя только одно поле с уведомлением, то нажми add notification, чтобы добавить второе.\n*Поле Comments/Комментарий* о заказчике: обязательно пишем имя клиента и ссылку на его линкедин аккаунт, кто ему нужен и зачем (исходя из переписки на линкеде или почте, все что может пригодиться на звонке: инфа о его компании, свободной вакансии; или же он просто сказал, что хочет узнать по какой модели строится наша работа).\nВсе комментарии писать на английском, чтобы клиент тоже понимал о чем речь.",
)
element_tree.add_element(
    "button", {"Далее": "_questions_add_event_to_calendar_4"})
element_tree.add_element("branch", "_questions_add_event_to_calendar_4")
element_tree.add_element(
    "text",
    "*Manager: Your name* (это в Ваших интересах, чтобы мы знали кому дать бонус )\n*Поле Guests* – сюда внеси имейлы всех тех, кого мы хотим видеть на звонке:\n- нашу почту sales@rh-s.com,\n- почту клиента (с его стороны также может быть несколько почт, если он попросил подключить на звонок к примеру его партнера).\nИм придет оповещение о данном звонке на почту, и перед самым звонком появится оповещение из календаря.\nНажимаем *SAVE*, и когда появится *Invite external guests, нажимаем YES*.",
)
element_tree.add_element("button", "_questions_add_event_to_calendar_5")
element_tree.add_element("branch", "_questions_add_event_to_calendar_5")
element_tree.add_element(
    "text",
    "В СРМ измени статус Лида на Event,  добавь дату и время звонка.\nЗа 30 мин до звонка, вежливо напомни клиенту, о том, что у нас назначена беседа.\nЕсли возникают какие-то обстоятельства и звонок не состоится, сообщи об этом sales менеджеру.\nПосле звонка, нужно связаться с sales менеджером и поинтересоваться результатами, после чего поставить статус Call.",
)
element_tree.add_element("button", {"Обратная связь": "_feedback"})
element_tree.add_element("branch", "_questions_where_to_get_calendar")
element_tree.add_element(
    "text",
    "Открой *новую вкладку в браузере гугл-хром*.\nВ правом верхнем углу, *нажми на меню* (в виде точек).\nОткроется меню расширений Гугл.\nВыбери *Календарь*.\nДля *назначения ивента, открой календарь с корпоративной почты info@rh-s.com*.",
)
element_tree.add_element("branch", "_questions_followup_in_calendar")
element_tree.add_element(
    "text",
    "1. Открой _Гугл-календарь_. Создай новое напоминание.\n*Заголовок* календарного события – *“название компании” FollowUp*\n2. *Выбери дату* на которую надо сделать напоминание и продолжительность: *ставь галочку НА ВЕСЬ ДЕНЬ*. Так твои ивенты будут отображаться вверху календаря.\n3. Важно: в календаре *выделяем фоллоу-апы ОРАНЖЕВЫМ цветом*.\n4. *Заполни карточку напоминания*\n- в описании укажи *описание клиента, его вопросы/ответы, его контакты*.\n- обязательно укажи *Manager* - себя, чтобы мы знали, кто привел лида.\n- в *Guests* - обязательно добавь почту sales@rh-s.com чтобы твое напоминание отобразилось и у ребят, которые непосредственно созваниваются с клиентами.",
)

######################################################
##  Update questions menu
######################################################

element_tree.add_element("branch", "_questions_update")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_UPDATE)
element_tree.add_element("branch", "_questions_what_update_is")
element_tree.add_element(
    "text",
    "*Апдейты* - это лиды, которые уже есть в СРМ, были добавлены тобой или другим менеджером более трех месяцев назад.\nТаким лидам *мы пишем повторные сообщения и отправляем повторный коннект*.",
)
element_tree.add_element("branch", "_questions_why_update_needed")
element_tree.add_element(
    "text",
    "Эти лидам мы пишем повторные сообщения и отправляем повторный коннект.\n*Так мы напоминаем потенциальным клиентам о себе и своих услугах. Со временем в компаниях меняются задачи, появляются новые проекты и мы можем предложить сотрудничество в нужный момент для лида.*",
)

element_tree.add_element("branch", "_questions_how_to_find_update")
element_tree.add_element(
    "text",
    'Как найти апдейтов:\n- В своей СРМ открой вкладку Leads.\n- Выбери необходимые тебе поля:\n*Country* - страна с которой сейчас  работаешь\n*Lead Status* - все статусы, кроме Call  Not relevant\n- Нажми *Apply*.\nДалее откроется список всех лидов, которые были внесены за все время под нужным тебе статусом и страной, с которой ты сейчас работаешь.\n- Листай вниз страницы, и начинай работать с лидами с конце списка, т.е. с самыми старыми - которые были сделаны 3 и более месяцев назад.\n- Проверь дату, когда лид был создан "CREATED ON" и дату, когда лиду был сделан последний апдейт UPDATE ON. Обрати внимание на комментарии.',
)
element_tree.add_element("url", {"СРМ Remote Helpers": "https://crm-s.com/"})
element_tree.add_element("branch", "_questions_how_to_do_update")
element_tree.add_element(
    "text",
    "Зайди в карту лида, и перейди по ссылке *Contact’s LinkedIn* на страничку лида в LinkedIn.\nОтправь ему повторный коннект вместе с шаблоном: connect-add note.\nДалее в СРМ в карте лида нажми *Edit* и отредактируй информацию:\n- поле *Active Agents* - укажи свои данные, чтобы лид был засчитан именно тебе.\n- поле *LinkedIn Accounts* - укажи аккаунт с которого ты отправил коннект. \n- поле *Lead Status* - поставь статус Sent Request\n- поле *Note* - укажи комментарий - updated (лид обновлен)\nВ завершение редактирования карты лида нажми *Update*.",
)
element_tree.add_element("branch", "_questions_standart_update_count")
element_tree.add_element("text", "Норма апдейтов - 120+ компаний.")

######################################################
##  Time tracker questions menu
######################################################

element_tree.add_element("branch", "_questions_time_tracker")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_TIME_TRACKER)
element_tree.add_element("branch", "_questions_enable_time_tracker")
element_tree.add_element(
    "text",
    "Зайди в СРМ.\nНажми кнопку Login в правом верхнем углу экрана.\nВведи свою электронную почту в поле Email и пароль в поле Password и нажми кнопку LOG IN.\nПри переходе на следующую страницу (вкладка Dashboard) браузер выведет окно запроса на *доступ к данным о твоем местоположении. Нажми “Разрешить”.*\nИтог: *Начало рабочего дня >>> Clock In >>> Обеденный перерыв >>> Clock Out >>> Возвращение с обеденного перерыва >>> Clock In >>> Окончание рабочего дня >>> Clock Out*",
)
element_tree.add_element("url", {"Открой СРМ": "https://crm-s.com/"})
element_tree.add_element("branch", "_questions_google_chrome_setup")
element_tree.add_element(
    "text",
    "Нажми кнопку _меню в правом верхнем углу окна браузера_, в появившемся списке нажми на вкладку *Настройки*.\nВ списке слева выбери *вкладку Конфиденциальность и безопасность*.\nПролистай немного вниз пока не встретишь *вкладку Настройки сайтов*, нажми на нее.\nНажми на *вкладку Посмотреть текущие разрешения и сохраненные данные сайтов*.\n*В поисковой строке в правом верхнем углу введи crm-s.com*, нажми на появившуюся кнопку с этим адресом.\nВ появившемся списке найди *строку Геоданные* и справа выбери вариант *Разрешить*.",
)

######################################################
##  Contacts questions menu
######################################################

element_tree.add_element("branch", "_questions_contacts")
element_tree.add_element(
    "text",
    "Влад (аккаунт-менеджер)\n+380981101090\n\nКатя Истомина (Бухгалтерия)\n+380714184225\n\nЮлия Мартынив (Тимлид Sales)\n+380662227034\n\nМария Бигун (Тимлид LeadGeneration)\n+380634345683",
)
element_tree.add_element("button", {"Обратная связь": "_feedback"})

######################################################
##  Bonus n salary questions menu
######################################################

element_tree.add_element("branch", "_questions_bonus_n_salary")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_BONUS_N_SALARY)
element_tree.add_element("branch", "_questions_my_bonuses")
element_tree.add_element(
    "text",
    "Мы предлагаем бонус за каждый назначенный и состоявшийся звонок. Детальнее разберем бонусную систему ниже.\n\n200 грн - стандартный бонус за назначенный и состоявшийся звонок с клиентом.\n+200 грн - если вы назначили звонок, на котором сразу будет собеседование с конкретными кандидатами/кандидатом (без сейлзов).\n+500 грн - если совершена продажа нашего сотрудника.\n\nЗвонок засчитывается только если:\nа) звонок с клиентом состоялся;\nб) клиент в полной мере понял, какие услуги мы предлагаем (т.е. Информация предоставлена клиенту корректно);\nв) лид релевантный.\n\nБонусы подводятся в конце каждого месяца.\nДанные суммы не предел, все зависит от вас и ваших стараний.\nДанные бонусы могут быть первыми признаками вашего карьерного роста в нашей компании, но отнюдь не их пределом.",
)
element_tree.add_element("branch", "_questions_when_salary")
element_tree.add_element(
    "text",
    "Зарплата начисляется два раза в месяц с 5 по 10 и с 20 по 25 числа каждого месяца на карточку или наличными.",
)

######################################################
##  Leads questions menu
######################################################

element_tree.add_element("branch", "_questions_leads")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_LEADS)
element_tree.add_element("branch", "_questions_which_leads_to_look_for")
element_tree.add_element(
    "text",
    "Обрати внимание:\n\n- на _род деятельности лида_.\n*Добавляем: CEO, COO, Founder, CTO, Owner, Director, co-Founder* (хотя если есть возможность добавить не сооснователя, то отдайте предпочтение другой должности), *Entrepreneur*.\n\n- на _страну лида_.\n*Работаем с: Australia, Austria, Belgium, Canada, Denmark, Estonia, Finland, France, Germany, Ireland, Italy, Israel, Luxembourg, Netherlands, Norway, Spain, Sweden, Switzerland, United Kingdom, USA*.\n\n- имя и внешность лида.\nЕсли в профиле у человека стоит одна из вышеперечисленных стран, но тебя смущает его имя или внешность, например он вылитый индус или афроамериканец (упоминаю их, потому что они часто маскируются), то такие люди нам тоже не подходят.\n\n- _наличие общих профилей_.\nМожет оказаться, что наши менеджеры уже с ним связывались, возможно, мы уже имеем с этим человеком какие-либо деловые отношения. Всегда проверяйте наличие компании, в которой работает лид, в нашей СРМ системе.\nЕсли общих профилей больше 8 – это не значит, что не стоит обращать на человека внимание. Все эти люди могут не относиться к нашей компании. Главное – проверить.\nПроверить можно, кликнув на строчку с количеством общих профилей.\n\nЕсли все ок, то жми кнопку *Connect*.",
)
element_tree.add_element("branch", "_questions_data_from_lead")
element_tree.add_element(
    "text",
    "Если клиент заинтересован и хочет назначить звонок, твоя задача уточнить у него:\n- *время*, когда ему будет удобно созвониться\n- *временную зону или город* в котором он находится\n- *почту*, куда отправить приглашение на звонок\n- где ему удобней было бы созвониться: Skype, Whatsapp, Hangout, Zoom.\n\nТакже *не забывай всю информацию о лиде (компания, страна, любые контакты, и тд - все, что может быть полезно для последу.щей коммуникации с клиентом)*.",
)
element_tree.add_element("branch", "_questions_add_lead")
element_tree.add_element(
    "text",
    "Чтобы добавить лида в СРМ:\n\nОткрой СРМ\nПерейди на вкладку *Leads*, в правом верхнем углу нажми на кнопку *Add new lead*.\n\nЗаполни необходимую информацию о лиде.\nПоля помеченые красной звездочкой* обязательно должны быть заполнены, иначе новый лид не будет сохранен.\n\nПоля, которые *заполняются автоматически: LG Manager, Lead Source, Lead Status и Country*.\n\nВ *поле Linkedin accounts* выбери аккаунт на котором сейчас работаешь.\n\nВ *поле Company* добавь компанию лида.\n\nВ *Company Size, Industry и Position* выбери подходящий вариант из выпадающего списка.\n\nНажми *Save*.",
)
element_tree.add_element("url", {"СРМ Remote Helpers": "https://crm-s.com/"})
element_tree.add_element("branch", "_questions_fill_lead_chart")
element_tree.add_element(
    "text",
    "*В карту нового лида необходимо внести всю информацию о нем, которую тебе удалось собрать в процессе коммуникации.*\nПоля помеченые красной звездочкой* обязательно должны быть заполнены, иначе новый лид не будет сохранен.\n\n*Поля, которые заполняются автоматически* : LG Manager, Lead Source, Lead Status и Country.\n\nВ *поле Linkedin accounts* выбери аккаунт на котором сейчас работаешь.\n\nВ *поле Company* добавь компанию лида.\n\nВ *Company Size, Industry и Position* выбери подходящий вариант из выпадающего списка.\n\nНажми *Save*.",
)
element_tree.add_element("branch", "_questions_when_to_follow_up")
element_tree.add_element(
    "text",
    "*Если клиент просит связаться с ним позже или отвечает, что сейчас наши услуги не актуальны, но через пару месяцев он начинает новый проект и они понадобятся, нужно ставить клиента на фоллоу ап*.\n\nЕсли ты отправлял презентацию, этот инструмент также может пригодиться чтобы спросить, что клиент о ней думает.",
)
element_tree.add_element("branch", "_questions_how_much_leads_i_made")
element_tree.add_element(
    "text",
    "Зайди в свою СРМ. Открой вкладку *Lead Reports*.\n\nИспользуя фильтры ты можешь просмотреть всех лидов, которых ты внес в СРМ.",
)
element_tree.add_element("branch", "_questions_standart_lead_count")
element_tree.add_element("text", "Норма - *40-50 лидов в день*.")
element_tree.add_element("branch", "_questions_how_to_find_correct_lead")
element_tree.add_element(
    "text",
    "Всех лидов ты можешь просмотреть во вкладке *Leads* в своей СРМ.\nДля того, чтобы найти конкретного лида, используй фильтры.",
)

######################################################
##  Templates questions menu
######################################################

element_tree.add_element("branch", "_questions_templates")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_TEMPLATES)
element_tree.add_element("branch", "_questions_first_lead_connect")
element_tree.add_element(
    "text",
    "Приветствие:\nHello %Name%,\nWould you like to hire our Remote Marketing Employees from Ukraine part-time or full-time?\nCan we connect?\n",
)
element_tree.add_element("branch", "_questions_second_lead_connect")
element_tree.add_element(
    "text",
    "Варианты коннекта:\nВторое сообщение после коннекта:\nWhat information are you interested in?\n1) more info about our company;\n2) available positions to choose from (departments)\n3) prices and conditions\n4) Do you want to share your company needs?\nAppreciate your answer,\nRemote Helpers,\nhttps://www.rh-s.com\n\nВторое сообщение (негативный ответ/отказ):\nOk, thanks your answer \nMay I ask you for an email to send our presentation in case of your future needs?",
)
element_tree.add_element("branch", "_questions_third_lead_connect")
element_tree.add_element(
    "text",
    "Третье сообщение (после ответа на второе сообщение):\nМы описываем для тебя несколько вариантов ответов, в зависимости от того, о чем тебя может спросить клиент.\nПрезентация - https://docs.google.com/presentation/d/e/2PACX-1vSleEpaKL1TOz8NV7d2OY7wtS111idiEdrSM_f88_GiCe-F4pqdzX7SUwZn3vDOog/pub?start=true&loop=true&delayms=15000&slide=id.g1180199a397_3_22 \nWe have candidates:\n-Sales (lead generation managers (B2B), sales)\n-Admin (project managers, administrators, personal assistants, finance)\n-Creative (designers, illustrators, video editors, motion designers)\n-Paid advertisement (google, facebook, linkedin, media buying)\n-Content marketing (smm, copywriting, influence managers, content managers)\n-Development (frontend/backend)\nWhat sphere are you interested in?\nConditions:\nNo prepayment\nOpen termination date\nOnly dedicated employees\nPrices(full time):\nAdmin and sales 1000 EUR\nContent marketing 1400 EUR\nCreative 1200-1400 EUR\nDevelopment 1900 EUR\nPlease share what you would be interested in?\n",
)
element_tree.add_element("branch", "_questions_about_specialities")
element_tree.add_element(
    "text",
    "Если *клиент спрашивает о специальностях*, вариант твоего ответа:\n\nCandidates we offer you to hire can work in the following positions: Lead Generation Managers, Customer Support, Personal Assistants, Social Media Managers, Designers, Media Buyers, PPC, SEO, AdOps, English teachers etc. Can we set a call to see if we can find a fit for you?\n\n*Следующее сообщение может использоваться в случаях, когда клиент спрашивает про частичную занятость или о конкретном заказе*. Например клиент интересуется не могли бы мы сделать для него сайт?\n\n“To keep price advantages comparing to freelancers that charge minimum 15€ per hour, our maximum cost is 7,5€ per hour. But there should be enough work for a full time – it is 160 hours a month, 5 days a week,  8 hours a day. So the final prices are 1200€ for designers, 1200€ for marketers and 1000€ for managers per month. Can we set a call to discuss all the details?”",
)
element_tree.add_element("branch", "_questions_about_employees_experience")
element_tree.add_element(
    "text",
    "How much experience do they have? Can you send me some CVs?\n“Most of our employees have a good knowledge of English, worked a while in digital marketing, but still there should be a team lead from your side to run training. Each company has its own specifics and employees need time to get into things.”\nAnyway you can find CVs of available employees on our Telegram channel or website:\nhttps://t.me/RemoteHelpers\nhttps://www.rh-s.com/\nПодбор кандидатов:\nLet me share the most suitable candidates for you, you can look through their CVs and let me know who is the best match for you:\n...link\n...link\n...link\nWhat about setting up a call with candidates? This will be the best way to get to know them and learn more about their experience, skills, and so on.",
)
element_tree.add_element("branch", "_questions_client_not_interested")
element_tree.add_element(
    "text",
    "Если ответ отрицательный ( по типу “not interested” или “ Now I don’t need your services”) то ответ должен быть таким:\n“Thank you for the reply. May I send you our presentation and prices in case you will need our services in the future?”\nОтправляешь, а потом уточняешь у клиента, получил ли он твое письмо, есть ли какие-то вопросы. Нужно отправлять письма всегда, после того, как клиент отправил свою почту, так он не потеряет наши контакты и сможет обратиться в нужный момент.\nПосле этого не забудь поставить в календаре ивент на FollowUp, чтобы не потерять контакт, и связаться с ним в будущем + статус FollowUp и дату в CRM..",
)
element_tree.add_element("branch", "_questions_client_interested")
element_tree.add_element(
    "text",
    "Если *клиент заинтересован и хочет назначить звонок*, твоя задача уточнить у него:\n- время, когда ему будет удобно созвониться\n- часовую зону или город в котором он находится\n- почту, куда отправить приглашение на звонок\n- где ему удобней было бы созвониться: скайп, вотсап, хэнгаут, zoom\nПосле чего, нужно будет сравнить сколько это будет по нашему времени и создать ивент в календаре",
)

######################################################
##  Connect questions menu
######################################################

element_tree.add_element("branch", "_questions_connect")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_CONNECT)
element_tree.add_element("branch", "_questions_first_lead_connect_2")
element_tree.add_element(
    "text",
    "Приветствие:\nHello %Name%,\nWould you like to hire our Remote Marketing Employees from Ukraine part-time or full-time?\nCan we connect?\n",
)
element_tree.add_element("branch", "_questions_second_lead_connect_2")
element_tree.add_element(
    "text",
    "Варианты коннекта:\nВторое сообщение после коннекта:\nWhat information are you interested in?\n1) more info about our company;\n2) available positions to choose from (departments)\n3) prices and conditions\n4) Do you want to share your company needs?\nAppreciate your answer,\nRemote Helpers,\nhttps://www.rh-s.com\n\nВторое сообщение (негативный ответ/отказ):\nOk, thanks your answer \nMay I ask you for an email to send our presentation in case of your future needs?",
)
element_tree.add_element("branch", "_questions_third_lead_connect_2")
element_tree.add_element(
    "text",
    "Третье сообщение (после ответа на второе сообщение):\nМы описываем для тебя несколько вариантов ответов, в зависимости от того, о чем тебя может спросить клиент.\nПрезентация - https://docs.google.com/presentation/d/e/2PACX-1vSleEpaKL1TOz8NV7d2OY7wtS111idiEdrSM_f88_GiCe-F4pqdzX7SUwZn3vDOog/pub?start=true&loop=true&delayms=15000&slide=id.g1180199a397_3_22 \nWe have candidates:\n-Sales (lead generation managers (B2B), sales)\n-Admin (project managers, administrators, personal assistants, finance)\n-Creative (designers, illustrators, video editors, motion designers)\n-Paid advertisement (google, facebook, linkedin, media buying)\n-Content marketing (smm, copywriting, influence managers, content managers)\n-Development (frontend/backend)\nWhat sphere are you interested in?\nConditions:\nNo prepayment\nOpen termination date\nOnly dedicated employees\nPrices(full time):\nAdmin and sales 1000 EUR\nContent marketing 1400 EUR\nCreative 1200-1400 EUR\nDevelopment 1900 EUR\nPlease share what you would be interested in?\n",
)
element_tree.add_element("branch", "_questions_send_connect_to_lead")
element_tree.add_element(
    "text",
    "Зайди на свою страницу в Линкедин, затем во вкладку My Network, расположенную на верхней панели сайта.\n\nВнизу страницы ты найдешь все профили (connections), которые могут быть тебе полезны.\n\nОбрати внимание:\n\n- на _род деятельности лида_.\n*Добавляем: CEO, COO, Founder, CTO, Owner, Director, co-Founder* (хотя если есть возможность добавить не сооснователя, то отдайте предпочтение другой должности), *Entrepreneur*.\n\n- на _страну лида_.\n*Работаем с: Australia, Austria, Belgium, Canada, Denmark, Estonia, Finland, France, Germany, Ireland, Italy, Israel, Luxembourg, Netherlands, Norway, Spain, Sweden, Switzerland, United Kingdom, USA*.\n\n- имя и внешность лида.\nЕсли в профиле у человека стоит одна из вышеперечисленных стран, но тебя смущает его имя или внешность, например он вылитый индус или афроамериканец (упоминаю их, потому что они часто маскируются), то такие люди нам тоже не подходят.\n\n- _наличие общих профилей_.\nМожет оказаться, что наши менеджеры уже с ним связывались, возможно, мы уже имеем с этим человеком какие-либо деловые отношения. Всегда проверяйте наличие компании, в которой работает лид, в нашей СРМ системе.\nЕсли общих профилей больше 8 – это не значит, что не стоит обращать на человека внимание. Все эти люди могут не относиться к нашей компании. Главное – проверить.\nПроверить можно, кликнув на строчку с количеством общих профилей.\n\nЕсли все ок, то жми кнопку *Connect*.",
)
element_tree.add_element(
    "url", {"My Network - LinkedIn": "https://www.linkedin.com/mynetwork/"}
)

######################################################
##  Followup questions menu
######################################################

element_tree.add_element("branch", "_questions_followup")
# # element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_FOLLOWUP)
element_tree.add_element("branch", "_questions_what_is_follow_up")
element_tree.add_element(
    "text",
    "Фоллоу-ап -это такой удобный инструмент, чтобы напомнить о себе человеку, который, возможно, о нас забыл. *Фоллоу-ап необходим для того, чтобы поддерживать интерес заказчика, ведь вероятность того, что сделка совершится, больше, если между нами и клиентом выстроены доверительные отношения.*\n\n*Если какой-либо клиент просит связаться с ним позже или отвечает, что сейчас наши услуги не актуальны, но через пару месяцев он начинает новый проект и они понадобятся, нужно ставить клиента на фоллоу ап.*\n\nЕсли вы отправляли презентацию, этот инструмент также может пригодиться чтоб спросить, что клиент о ней думает.",
)
element_tree.add_element("branch", "_questions_follow_up_in_calendar")
element_tree.add_element(
    "text",
    "Открой *Гугл-календарь*. Создай *новое напоминание*.\nЗаголовок календарного события – *“название компании” FollowUp*\n\n*Выбери дату на которую надо сделать напоминание и продолжительность: ставь галочку НА ВЕСЬ ДЕНЬ*. Так твои ивенты будут отображаться вверху календаря.\n\nВажно: в календаре *выделяем фоллоу-апы ОРАНЖЕВЫМ цветом*.\n\n*Заполни карточку напоминания*\n- в описании укажи все описание о клиенте, его вопросах/ответах, его контакты.\n- обязательно укажи Manager - себя, чтобы мы знали, кто привел лида.\n- в Guests - обязательно добавь почту sales@rh-s.com чтобы твое напоминание отобразилось и у ребят, которые непосредственно созваниваются с клиентами.",
)
element_tree.add_element(
    "url", {"Google Календарь": "https://calendar.google.com/"})

######################################################
##  Country questions menu
######################################################

element_tree.add_element("branch", "_questions_country")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_COUNTRY)
element_tree.add_element("branch", "_questions_country_i_work_with")
element_tree.add_element(
    "text",
    '*Каждый менеджер лидогенерации работает с определенной страной*. Т.е. за тобой уже закреплена определенная страна, в которой тебе нужно искать лидов.\n\nДля того, чтобы ты начал поиск лидов, нужно узнать, с какой страной ты работаешь на определенном аккаунте. Для этого:\n\n- зайди в свою СРМ\n\n- нажми кнопку *Add new lead*\n- *выбери Линкедин-аккаунт, который закреплен за тобой* (аккаунт, который тебе выдал аккаунт-менеджер специально для работы)\n- *в СРМ в поле "Country" появится название страны, с которой тебе нужно работать*\nЭто поле нельзя отредактировать. Его настраивает аккаунт-менеджер.',
)
element_tree.add_element(
    "url", {"CRM Remote Helpers": "https://crm-s.com/"})
element_tree.add_element("branch", "_questions_can_i_change_country")
element_tree.add_element(
    "text",
    "Твой аккаунт Линкедин закреплен за определенной страной. Эти данные может заменить только аккаунт-менеджер.",
)
element_tree.add_element("branch", "_questions_countries_not_working_with")
element_tree.add_element(
    "text",
    "Страны, которые *мало интересны*\n_Japan, Singapore, Cyprus, China_. Так как коммуникация с азиатами трудновата из-за плохого английского, рассматриваем каждый случай отдельно.\n\nСтраны, с которыми *не работаем*\nAndorra, Argentina, Bahamas, Belarus, Bolivia, Brazil, Brunei, Bulgaria, Chile, Colombia, Costa, Rica, Dominican Republic, Ecuador, Egypt, Fiji, Guyana, Indonesia, Kazakhstan, Macao, Malaysia, Mexico, Morocco, Nepal, Oman, Panama, Paraguay, Peru, Philippines, Puerto, Rico, Qatar, Republic of Korea (South), Romania, Russian Federation, Saudi Arabia, South, Africa, Thailand, Turkey, Ukraine, United Arab Emirates, Uruguay, Vanuatu, Albania, Algeria, Angola, Armenia, Azerbaijan, Bahrain, Bangladesh, Barbados, Belize, Benin, Botswana, Burkina, Faso, Burundi, Cambodia, Cameroon, Cape Verde, Chad, Comoros, Congo, El Salvador, Ethiopia, Gabon, Georgia, Guatemala, Guinea, Haiti, Honduras, India, Iraq, Jamaica, Jordan, Kenya, Kuwait, Kyrgyzstan, Laos, Lebanon, Lesotho, Macedonia, Madagascar, Mali, Mauritania, Mauritius, Moldova, Mongolia, Mozambique, Namibia, Nicaragua, Niger, Nigeria, Pakistan, Senegal, Sri Lanka, Suriname, Swaziland, Tajikistan, Tanzania, Togo, Trinidad and Tobago, Tunisia, Turkmenistan, Uganda, Uzbekistan, Vietnam, Zambia.\n\nСтраны СНГ – Украина, Россия, Беларусь, Молдова, Казахстан, Грузия, Азербайджан, Армения, Узбекистан, Таджикистан.\nПрактически все страны Африки и некоторые страны Азии – также являются неактуальными для нашего бизнеса.",
)
element_tree.add_element("branch", "_questions_countriues_working_with")
element_tree.add_element(
    "text",
    "Страны, с которыми мы работаем:\n_Australia, Austria, Belgium, Canada, Denmark, Finland, France, Germany, Ireland, Italy, Luxembourg, Netherlands, Norway, Spain, Sweden, Switzerland, United Kingdom, United States of America, Israel, Latvia, Lithuania, Estonia, Czech Republic_",
)

######################################################
##  Status questions menu
######################################################

element_tree.add_element("branch", "_questions_status")
# element_tree.add_element("text", "Выбери вопрос из списка:")
element_tree.add_element("keyboard", bm.QUESTIONS_STATUS)
element_tree.add_element("branch", "_questions_status_on_event")
element_tree.add_element(
    "text", "Статус лида в СРМ при назначении ивента - *Event*")
element_tree.add_element("branch", "_questions_status_update")
element_tree.add_element(
    "text",
    "Если ты ищешь лидов в СРМ для апдейта, то в Lead Status выбери все статусы, кроме Call.\n\nЕсли уже сделал апдейт, то в карте лида, в поле Lead Status поставь - *Sent Request*.",
)
element_tree.add_element("branch", "_questions_status_categories_in_CRM")
element_tree.add_element(
    "text",
    "*sent request* - отправлена заявка на коннект\n\n*connected* - лид принял твою заявку на коннект, и у тебя есть его контакты (почта и телефон)\n\n*interested* - лид ответил на твое сообщение и заинтересовался нашим предложением\n\n*not interested* - лид ответил, что наше предложение его не интересует\n\n*ignoring* - лид общался с тобой некоторое время, а потом перестал отвечать на сообщения\n\n*follow up* - лид ответил, что в данный момент не заинтересован в нашем предложении, но возможно рассмотрит его в будущем\n\n*event* - лид согласился на звонок и мы делаем ивент в календаре\n\n*call* - когда сейлз менеджер сообщил тебе, что звонок состоялся\n\n*not relevant for us* - когда случайно добавил в СРМ лида, который нам не подходит",
)

element_tree.add_element("branch", "_feedback")
element_tree.add_element("keyboard", bm.FEEDBACK_MENU)
element_tree.add_element("text", "Если есть проблемы/вопросы/предложения")
element_tree.add_element("text", "Отправляй их сюда:\n*Пиши прямо в чат*")
element_tree.add_element("input", "feedback")
element_tree.add_element("text", "Спасибо за отзыв!")

element_tree.add_element("branch", "_nn_question")
element_tree.add_element("text", "Задавай свой вопрос:")
element_tree.add_element("question", "question")
element_tree.add_element("keyboard", bm.NEW_USER_MENU)  # check it, it's a bug
element_tree.add_element("text", "Я не понял ваш вопрос")
element_tree.add_element("branch", "_end")

element_tree.add_element("branch", "_do_not_understand")
element_tree.add_element("text", "Я не понял ваш вопрос.")
element_tree.add_element("branch", "_end")


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bot.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)
# db.create_all()

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login_page.login"

@login.user_loader
def load_admin(id):
    return Admin.query.get(int(id))

if DEVELOPMENT == True:
    @app.after_request
    def add_header(response):
        response.headers["ngrok-skip-browser-warning"] = "true"
        return response

app.register_blueprint(stats_page, url_prefix="/stats")
app.register_blueprint(index_page, url_prefix="/index")
app.register_blueprint(register_page, url_prefix="/register")
app.register_blueprint(login_page, url_prefix="/login")
app.register_blueprint(logout_page, url_prefix="/logout")

# All bot request processing is done here


@app.route("/", methods=["POST"])
def incoming():

    rhandler.process_request(request)

    return Response(status=200)


def set_webhook(viber_bot):
    viber_bot.set_webhook(SERVER)


if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    app.run(host=HOST, port=PORT, debug=DEVELOPMENT, ssl_context=SSL_CONTEXT)
