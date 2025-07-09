def ask_licence_format_text(lang: str):
    match lang:
        case "ru":
            return "Какой формат вашего паспорта?"
        case "en":
            return "What format is your passport?"
        case "kz":
            return "Сіздің төлқұжатыңыз қандай форматта?"
        case "by":
            return "Які фармат вашага пашпарта?"
        case "az":
            return "Pasportunuz hansı formatdadır?"
        case "uz":
            return "Sizning pasportingiz qanday formatda?"
        case "tg":
            return "Шиносномаи шумо кадом формат аст?"
        case _:
            return "Unsupported language."


def failed_authorization_text(lang: str):
    match lang:
        case "ru":
            return "Не удалось авторизоваться, вернитесь в главное меню."
        case "en":
            return "Failed to log in, please return to main menu."
        case "kz":
            return "Жүйеге кіру сәтсіз аяқталды, негізгі мәзірге оралыңыз."
        case "by":
            return "Не атрымалася аўтарызавацца, вярніцеся ў галоўнае меню."
        case "az":
            return "Giriş uğursuz oldu, əsas menyuya qayıdın."
        case "uz":
            return "Kirish amalga oshmadi, asosiy menyuga qayting."
        case "tg":
            return "Ворид нашуд, ба менюи асосӣ баргардед."
        case _:
            return "Unsupported language."


def need_registration_text(lang: str):
    match lang:
        case "ru":
            return "Вас нет в моих записях. Вам нужно зарегистрироваться в системе."
        case "en":
            return "You are not in my records. You need to register in the system."
        case "kz":
            return "Сіз менің жазбамда жоқсыз. Жүйеге тіркелу керек."
        case "by":
            return "Аб вас няма ў маіх запісах. Вам трэба зарэгістравацца ў сістэме."
        case "az":
            return "Siz mənim qeydlərimdə deyilsiniz. Sistemdə qeydiyyatdan keçməlisiniz."
        case "uz":
            return "Siz mening yozuvlarimda yo'qsiz. Tizimda ro'yxatdan o'tishingiz kerak."
        case "tg":
            return "Шумо дар сабтҳои ман нестед. Шумо бояд дар система сабт шавед."
        case _:
            return "Unsupported language."


""" Keyboards texts """


def ru_format_kb_text(lang: str):
    match lang:
        case "ru":
            return "Российский"
        case "en":
            return "Russian"
        case "kz":
            return "Ресейлік"
        case "by":
            return "Расійскія"
        case "az":
            return "Rusiya"
        case "uz":
            return "Rossiya"
        case "tg":
            return "Русия"
        case _:
            return "Unsupported language."


def by_format_kb_text(lang: str):
    match lang:
        case "ru":
            return "Белорусский"
        case "en":
            return "Belarusian"
        case "kz":
            return "Беларусь"
        case "by":
            return "Беларуская"
        case "az":
            return "Belarus"
        case "uz":
            return "Belarus"
        case "tg":
            return "Белорус"
        case _:
            return "Unsupported language."


def en_format_kb_text(lang: str):
    match lang:
        case "ru":
            return "Европейский"
        case "en":
            return "European"
        case "kz":
            return "Еуропалық"
        case "by":
            return "Еўрапейская"
        case "az":
            return "Avropa"
        case "uz":
            return "Evropa"
        case "tg":
            return "Аврупоӣ"
        case _:
            return "Unsupported language."


def kz_format_kb_text(lang: str):
    match lang:
        case "ru":
            return "Казахский"
        case "en":
            return "Kazakh"
        case "kz":
            return "Қазақ"
        case "by":
            return "Казахская"
        case "az":
            return "Qazax"
        case "uz":
            return "Qozog'iston"
        case "tg":
            return "Қазоқ"
        case _:
            return "Unsupported language."


def az_format_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Азербайджанский"
        case "en":
            return "Azerbaijani"
        case "kz":
            return "Әзірбайжан"
        case "by":
            return "Азербайджана"
        case "az":
            return "Azərbaycan"
        case "uz":
            return "Ozarbayjon"
        case "tg":
            return "Озарбойҷон"
        case _:
            return "Unsupported language."


def tj_format_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Таджикский"
        case "en":
            return "Tajik"
        case "kz":
            return "Тажикистан"
        case "by":
            return "Тацікская"
        case "az":
            return "Tacik"
        case "uz":
            return "Tojikiston"
        case "tg":
            return "Тожикистон"
        case _:
            return "Unsupported language."


def uz_format_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Узбекский"
        case "en":
            return "Uzbek"
        case "kz":
            return "Ўзбекистан"
        case "by":
            return "Узбекская"
        case "az":
            return "Özbək"
        case "uz":
            return "O'zbekiston"
        case "tg":
            return "Ўзбекистон"
        case _:
            return "Unsupported language."


def kg_format_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Киргизский"
        case "en":
            return "Kyrgyz"
        case "kz":
            return "Кыргызстан"
        case "by":
            return "Кіргізская"
        case "az":
            return "Kırğız"
        case "uz":
            return "Qirg'iziston"
        case "tg":
            return "Киргизстин"
        case _:
            return "Unsupported language."


def ua_format_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Украинский"
        case "en":
            return "Ukrainian"
        case "kz":
            return "Украина"
        case "by":
            return "Укаранская"
        case "az":
            return "Ükrayin"
        case "uz":
            return "Ukraina"
        case "tg":
            return "Украинӣ"
        case _:
            return "Unsupported language."


def go_back_kb_text(lang: str):
    match lang:
        case "ru":
            return "Вернуться назад"
        case "en":
            return "Go back"
        case "kz":
            return "Артқа қайту"
        case "by":
            return "Вярнуцца назад"
        case "az":
            return "Geri qayıt"
        case "uz":
            return "Orqaga qaytish"
        case "tg":
            return "Бозгашт"
        case _:
            return "Unsupported language."


def auth_kb_text(lang: str):
    match lang:
        case "ru":
            return "Авторизоваться"
        case "en":
            return "Log in"
        case "kz":
            return "Жүйеге кіру"
        case "by":
            return "Аўтарызавацца"
        case "az":
            return "Daxil ol"
        case "uz":
            return "Tizimga kirish"
        case "tg":
            return "Даромадан"
        case _:
            return "Unsupported language."


def edit_kb_text(lang: str):
    match lang:
        case "ru":
            return "Изменить"
        case "en":
            return "Edit"
        case "kz":
            return "Өзгерту"
        case "by":
            return "Змяніць"
        case "az":
            return "Dəyişmək"
        case "uz":
            return "O'zgartirish"
        case "tg":
            return "Тағйир"
        case _:
            return "Unsupported language."


def apply_authorization_kb_text(lang: str):
    match lang:
        case "ru":
            return "Да, это я"
        case "en":
            return "Yes, it's me"
        case "kz":
            return "Иә, бұл менмін"
        case "by":
            return "Так, гэта я"
        case "az":
            return "Bəli, mənəm"
        case "uz":
            return "Ha, bu menman"
        case "tg":
            return "Бале, ин манам"
        case _:
            return "Unsupported language."


def deny_authorization_kb_text(lang: str):
    match lang:
        case "ru":
            return "Нет, изменить серию и номер паспорта"
        case "en":
            return "No, change my passport"
        case "kz":
            return "Жоқ, паспортыңдың сериясын және нөмірін өзгерт"
        case "by":
            return "Не, памяняць паспарт"
        case "az":
            return "Xeyr, pasportimi dəyişin"
        case "uz":
            return "Yo'q, pasportimni almashtiring"
        case "tg":
            return "Не, паспорти маро иваз кунед"
        case _:
            return "Unsupported language."


def edit_licence_format_kb_text(lang: str):
    match lang:
        case "ru":
            return "Изменить формат паспорта"
        case "en":
            return "Edit passport format"
        case "kz":
            return "Паспортың пішімін өңдеу"
        case "by":
            return "Рэдагаваць фармат паспарту"
        case "az":
            return "Pasport formatını redaktə edin"
        case "uz":
            return "Pasport formatini tahrirlash"
        case "tg":
            return "Таҳрири формати паспорт"
        case _:
            return "Unsupported language."


def edit_licence_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Изменить серию и номер паспорта"
        case "en":
            return "Edit passport series and number"
        case "kz":
            return "Паспортың сериясын және нөмірін өзгерту"
        case "by":
            return "Змяніць серыю і нумар паспарту"
        case "az":
            return "Pasport seriyasını və nömrəsini dəyişmək"
        case "uz":
            return "Pasport seriyasini va raqamini o'zgartirish"
        case "tg":
            return "Серия ва рақами паспортро тағйир додан"
        case _:
            return "Unsupported language."


""" Ask licence texts """


def get_format_messages(lang: str, country_code: str) -> str:
    format_messages = {
        "ru": ask_licence_text(lang),
        "by": ask_licence_text(lang),
        "en": ask_licence_text(lang),
        "kz": ask_licence_text(lang),
        "az": ask_licence_text(lang),
        "tj": ask_only_licence_number_text(lang),
        "uz": ask_only_licence_number_text(lang),
        "kg": ask_licence_text(lang),
        "ua": ask_licence_text(lang),
    }
    return format_messages.get(country_code)


def ask_licence_text(lang: str) -> str:
    match lang:
        case "ru":
            return ("Введите серию и номер паспорта через пробел:\n"
                    "При наличии только номера паспорта, вводите без пробела.")
        case "en":
            return "Enter passport series and number separated by a space:"
        case "kz":
            return "Паспортың сериясын және нөмірін бос орынмен ажыратып енгізіңіз:"
        case "by":
            return "Увядзіце серыю і нумар паспарту праз прабел:"
        case "az":
            return "Seriya və pasport nömrəsini boşluqla ayırıb daxil edin:"
        case "uz":
            return "Pasportning seriyasini va raqamini probel bilan ajratib kiriting:"
        case "tg":
            return "Серия ва рақами паспортро бо фосила якка шуда ворид кунед:"
        case _:
            return "Unsupported language."


def ask_only_licence_number_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Введите номер паспорта:"
        case "en":
            return "Enter passport number:"
        case "kz":
            return "Жолаушыңыздың нөмірін енгізіңіз:"
        case "by":
            return "Увядзіце нумар паспарту:"
        case "az":
            return "Pasport nömrəsini daxil edin:"
        case "uz":
            return "Pasportning raqamini kiriting:"
        case "tg":
            return "Рақами паспорт ро баъд гирок зедо:"
        case _:
            return "Unsupported language."


""" Incorrect input texts """


def get_error_messages(lang: str, country_code: str) -> str:
    return incorrect_licence_number(lang) + format_input_licence_number(lang, country_code)


def incorrect_licence_number(lang: str) -> str:
    match lang:
        case "ru":
            return "Вы ввели некорректно серию и/или номер паспорта.\n"
        case "en":
            return "You entered the passport series and/or number incorrectly.\n"
        case "kz":
            return "Сіз паспортың сериясын және/ немесе нөмірін дұрыс енгізбегеніз.\n"
        case "by":
            return "Вы ўвялі некарэктна серыю і/або нумар паспарту.\n"
        case "az":
            return "Sizi pasportun seriya və ya nömrəsini səhv daxil etdiniz.\n"
        case "uz":
            return "Siz pasportning seriyasini yoki raqamini noto'g'ri kiritdingiz.\n"
        case "tg":
            return "Шумо серия ва/ёки рақами паспортро нодуруст ворид кардед.\n"
        case _:
            return "Unsupported language."


def format_input_licence_number(lang: str, country_code: str) -> str:
    match country_code:
        case "ru":
            match lang:
                case "ru": return "Формат ввода для Российский паспорт: xxxx yyyy (4 цифры для серии, 6 цифр для номера через пробел)."
                case "en": return "Input format for Russian passport: xxxx yyyy (4 digits for series, 6 digits for number separated by a space)."
                case "kz": return "Енгізу форматы үшін Ресей паспорты: xxxx yyyy (серия 4 сан, нөмір 6 сан аралас бос орынмен)."
                case "by": return "Фармат уводу для Расійская паспарт: xxxx yyyy (4 лічбы для серыі, 6 лічбаў для нумара з прабелам)."
                case "az": return "Daxil formatı Rusiya pasportu üçün: xxxx yyyy (seriya üçün 4 rəqəm, nömrə üçün 6 rəqəm boşluqla ayrılmış şəkildə)."
                case "uz": return "Kirish formati Rossiya pasport uchun: xxxx yyyy (seriya uchun 4 ta raqam, raqam uchun 6 ta raqam probel bilan ajratilgan holatda)."
                case "tg": return "формати вуруд барои паспорт русия: xxxx yyyy (4 рақам барои серия, 6 рақам барои рақам бо фосила якка шуда)."
        case "by":
            match lang:
                case "ru": return "Формат ввода для Белорусский паспорт: XX yyyy (2 буквы для серии, 7 цифр для номера через пробел)."
                case "en": return "Input format for Belarusian passport: XX yyyy (2 letters for series, 7 digits for number separated by a space)."
                case "kz": return "Енгізу форматы үшін Беларусь паспорты: XX yyyy (серия 2 әрп, нөмір 7 сан аралас бос орынмен)."
                case "by": return "Фармат уводу для Беларуская паспарт: XX yyyy (2 літары для серыі, 7 лічбаў для нумара з прабелам)."
                case "az": return "Daxil formatı Belorussiya pasportu üçün: XX yyyy (seriya üçün 2 hərf, nömrə üçün 7 rəqəm boşluqla ayrılmış şəkildə)."
                case "uz": return "Kirish formati Belorussiya pasport uchun: XX yyyy (seriya uchun 2 ta harf, raqam uchun 7 ta raqam probel bilan ajratilgan holatda)."
                case "tg": return "формати вуруд барои паспорт белорусӣ: XX yyyy (2 хурӯф барои серия, 7 рақам барои рақам бо фосила якка шуда)."
        case "en":
            match lang:
                case "ru": return "Формат ввода для Европейский паспорт: XX yyyy (2 буквы для серии, 7 цифр для номера через пробел)."
                case "en": return "Input format for European passport: XX yyyy (2 letters for series, 7 digits for number separated by a space)."
                case "kz": return "Енгізу форматы үшін Еуропа паспорты: XX yyyy (серия 2 әрп, нөмір 7 сан аралас бос орынмен)."
                case "by": return "Фармат уводу для Еўрапейская паспарт: XX yyyy (2 літары для серыі, 7 лічбаў для нумара з прабелам)."
                case "az": return "Daxil formatı Avropa pasportu üçün: XX yyyy (seriya üçün 2 hərf, nömrə üçün 7 rəqəm boşluqla ayrılmış şəkildə)."
                case "uz": return "Kirish formati Evropa pasport uchun: XX yyyy (seriya uchun 2 ta harf, raqam uchun 7 ta raqam probel bilan ajratilgan holatda)."
                case "tg": return "формати вуруд барои паспорт аврупоӣ: XX yyyy (2 хурӯф барои серия, 7 рақам барои рақам бо фосила якка шуда)."
        case "kz":
            match lang:
                case "ru": return "Формат ввода для Казахстанский паспорт: X yyyy (1 буква для серии, 8 цифр для номера через пробел)."
                case "en": return "Input format for Kazakh passport: X yyyy (1 letter for series, 8 digits for number separated by a space)."
                case "kz": return "Енгізу форматы үшін Қазақстан паспорты: X yyyy (серия 1 әрп, нөмір 8 сан аралас бос орынмен)."
                case "by": return "Фармат уводу для Казахская паспарт: X yyyy (1 літара для серыі, 8 лічбаў для нумара з прабелам)."
                case "az": return "Daxil formatı Qazaxstan pasportu üçün: X yyyy (seriya üçün 1 hərf, nömrə üçün 8 rəqəm boşluqla ayrılmış şəkildə)."
                case "uz": return "Kirish formati Qozog'iston pasport uchun: X yyyy (seriya uchun 1 ta harf, raqam uchun 8 ta raqam probel bilan ajratilgan holatda)."
                case "tg": return "формати вуруд барои паспорт қазоқистон: X yyyy (1 хурӯф барои серия, 8 рақам барои рақам бо фосила якка шуда)."
        case "az":
            match lang:
                case "ru": return "Формат ввода для Азербайджанский паспорт: X yyyy (1 буква для серии, 8 цифр для номера через пробел)."
                case "en": return "Input format for Azerbaijani passport: X yyyy (1 letter for series, 8 digits for number separated by a space)."
                case "kz": return "Енгізу форматы үшін Әзірбайжан паспорты: X yyyy (серия 1 әрп, нөмір 8 сан аралас бос орынмен)."
                case "by": return "Фармат уводу для Азербайджанская паспарт: X yyyy (1 літара для серыі, 8 лічбаў для нумара з прабелам)."
                case "az": return "Daxil formatı Azərbaycan pasportu üçün: X yyyy (seriya üçün 1 hərf, nömrə üçün 8 rəqəm boşluqla ayrılmış şəkildə)."
                case "uz": return "Kirish formati Ozarbayjon pasport uchun: X yyyy (seriya uchun 1 ta harf, raqam uchun 8 ta raqam probel bilan ajratilgan holatda)."
                case "tg": return "формати вуруд барои паспорт озарбойҷон: X yyyy (1 хурӯф барои серия, 8 рақам барои рақам бо фосила якка шуда)."
        case "tj":
            match lang:
                case "ru": return "Формат ввода для Таджикский паспорт: xxxxxxxxx (9 цифр без пробелов)."
                case "en": return "Input format for Tajik passport: xxxxxxxxx (9 digits without spaces)."
                case "kz": return "Енгізу форматы үшін Тоҷикистон паспорты: xxxxxxxxx (9 сан бос орынсыз)."
                case "by": return "Фармат уводу для Таджикская паспарт: xxxxxxxxx (9 лічбаў без прабелаў)."
                case "az": return "Daxil formatı Tacikistan pasportu üçün: xxxxxxxxx (9 rəqəm boşluqsuz)."
                case "uz": return "Kirish formati Tojikiston pasport uchun: xxxxxxxxx (9 ta raqam bo'sh joysiz)."
                case "tg": return "формати вуруд барои паспорт тоҷикистон: xxxxxxxxx (9 рақам бе фосила)."
        case "uz":
            match lang:
                case "ru": return "Формат ввода для Узбекский паспорт: xxxxxxx (7 цифр без пробелов)."
                case "en": return "Input format for Uzbek passport: xxxxxxx (7 digits without spaces)."
                case "kz": return "Енгізу форматы үшін Озбекистан паспорты: xxxxxxx (7 сан бос орынсыз)."
                case "by": return "Фармат уводу для Узбекская паспарт: xxxxxxx (7 лічбаў без прабелаў)."
                case "az": return "Daxil formatı Özbəkistan pasportu üçün: xxxxxxx (7 rəqəm boşluqsuz)."
                case "uz": return "Kirish formati O'zbekiston pasport uchun: xxxxxxx (7 ta raqam bo'sh joysiz)."
                case "tg": return "формати вуруд барои паспорт озбекистон: xxxxxxx (7 рақам бе фосила)."
        case "kg":
            match lang:
                case "ru": return "Формат ввода для Киргизский паспорт: XXX yyyy или xx xxxxxxxx (2-3 буквы для серии, 6-9 цифр для номера через пробел)."
                case "en": return "Input format for Kyrgyz passport: XXX yyyy or xx xxxxxxxx (2-3 letters for series, 6-9 digits for number separated by a space)."
                case "kz": return "Енгізу форматы үшін Кыргызстан паспорты: XXX yyyy немесе xx xxxxxxxx (серия 2-3 әрп, нөмір 6-9 сан аралас бос орынмен)."
                case "by": return "Фармат уводу для Кіргізская паспарт: XXX yyyy ці xx xxxxxxxx (2-3 літары для серыі, 6-9 лічбаў для нумара з прабелам)."
                case "az": return "Daxil formatı Kırğızstan pasportu üçün: XXX yyyy və ya xx xxxxxxxx (seriya üçün 2-3 hərf, nömrə üçün 6-9 rəqəm boşluqla ayrılmış şəkildə)."
                case "uz": return "Kirish formati Qirg'iziston pasport uchun: XXX yyyy yoki xx xxxxxxxx (seriya uchun 2-3 ta harf, raqam uchun 6-9 ta raqam probel bilan ajratilgan holatda)."
                case "tg": return "формати вуруд барои паспорт кирғизистон: XXX yyyy ёки xx xxxxxxxx (2-3 хурӯф барои серия, 6-9 рақам барои рақам бо фосила якка шуда)."
        case "ua":
            match lang:
                case "ru": return "Формат ввода для Украинский паспорт: XX yyyy или xx xxxxxxxx (2 буквы для серии, 6-9 цифр для номера через пробел)."
                case "en": return "Input format for Ukrainian passport: XX yyyy or xx xxxxxxxx (2 letters for series, 6-9 digits for number separated by a space)."
                case "kz": return "Енгізу форматы үшін Украина паспорты: XX yyyy немесе xx xxxxxxxx (серия 2 әрп, нөмір 6-9 сан аралас бос орынмен)."
                case "by": return "Фармат уводу для Украінская паспарт: XX yyyy ці xx xxxxxxxx (2 літары для серыі, 6-9 лічбаў для нумара з прабелам)."
                case "az": return "Daxil formatı Ukrayna pasportu üçün: XX yyyy və ya xx xxxxxxxx (seriya üçün 2 hərf, nömrə üçün 6-9 rəqəm boşluqla ayrılmış şəkildə)."
                case "uz": return "Kirish formati Ukraina pasport uchun: XX yyyy yoki xx xxxxxxxx (seriya uchun 2 ta harf, raqam uchun 6-9 ta raqam probel bilan ajratilgan holatda)."
                case "tg": return "формати вуруд барои паспорт odioн: XX yyyy ёки xx xxxxxxxx (2 хурӯф барои серия, 6-9 рақам барои рақам бо фосила якка шуда)."
        case _:
            return "Unknown passport format."


""" Driver info texts """


def show_authorization_info_text(lang: str, data: dict) -> str:
    match lang:
        case "ru":
            return (f"Проверьте введённые вами данные.\n\n"
                    f"Серия паспорта: <b>{data['licence_series']}</b>\n"
                    f"Номер паспорта: <b>{data['licence_number']}</b>\n\n"
                    f"Для изменения данных нажмите кнопку <b>\"{edit_kb_text(lang)}\"</b>.\n"
                    f"Для авторизации нажмите <b>\"{auth_kb_text(lang)}\"</b>.")
        case "en":
            return (f"Check the data you entered.\n\n"
                    f"Passport series: <b>{data['licence_series']}</b>\n"
                    f"Passport number: <b>{data['licence_number']}</b>\n\n"
                    f"To change the data, click <b>\"{edit_kb_text(lang)}\"</b>.\n"
                    f"To log in, click <b>\"{auth_kb_text(lang)}\"</b>.")
        case "kz":
            return (f"Сіз енгізген деректерді тексеріңіз.\n\n"
                    f"Паспортың сериясы: <b>{data['licence_series']}</b>\n"
                    f"Паспортың нөмірі: <b>{data['licence_number']}</b>\n\n"
                    f"Деректерді өзгерту үшін <b>\"{edit_kb_text(lang)}\"</b> түймесін басыңыз.\n"
                    f"Авторизация үшін <b>\"{auth_kb_text(lang)}\"</b> түймесін басыңыз.")
        case "by":
            return (f"Праверце уведзеныя вамі дадзеныя.\n\n"
                    f"Серыя паспарту: <b>{data['licence_series']}</b>\n"
                    f"Нумар паспарту: <b>{data['licence_number']}</b>\n\n"
                    f"Для змены дадзеных націсніце кнопку <b>\"{edit_kb_text(lang)}\"</b>.\n"
                    f"Для аўтарызацыі націсніце <b>\"{auth_kb_text(lang)}\"</b>.")
        case "az":
            return (f"Daxil etdiyiniz məlumatları yoxlayın.\n\n"
                    f"Pasport seriyası: <b>{data['licence_series']}</b>\n"
                    f"Pasport nömrəsi: <b>{data['licence_number']}</b>\n\n"
                    f"Məlumatı dəyişdirmək üçün <b>\"{edit_kb_text(lang)}\"</b> düyməsini basın.\n"
                    f"Daxil olmaq üçün <b>\"{auth_kb_text(lang)} ol\"</b> klikləyin.")
        case "uz":
            return (f"Kiritilgan ma'lumotlarni tekshiring.\n\n"
                    f"Pasport seriyasi: <b>{data['licence_series']}</b>\n"
                    f"Pasport raqami: <b>{data['licence_number']}</b>\n\n"
                    f"Ma'lumotlarni o'zgartirish uchun <b>\"{edit_kb_text(lang)}\"</b> tugmasini bosing.\n"
                    f"Kirish uchun <b>\"{auth_kb_text(lang)}\"</b> tugmasini bosing.")
        case "tg":
            return (f"Маълумоти воридкардаатонро санҷед.\n\n"
                    f"Силсилаи паспорт: <b>{data['licence_series']}</b>\n"
                    f"Рақами паспорт: <b>{data['licence_number']}</b>\n\n"
                    f"Барои тағир додани маълумот, <b>\"{edit_kb_text(lang)}\"</b>-ро клик кунед.\n"
                    f"Барои ворид шудан, <b>\"{auth_kb_text(lang)}\"</b>-ро клик кунед.")
        case _:
            return "Unsupported language."


def show_driver_info_text(lang: str, data) -> str:
    match lang:
        case "ru":
            return (f"Вот что я нашел в своих записях:\n"
                    f"Фамилия: <b>{data.surname}</b>\n"
                    f"Имя: <b>{data.name}</b>\n"
                    f"Отчество: <b>{data.middle_name}</b>\n"
                    f"Номер телефона: <b>{data.number}</b>\n"
                    f"Серия паспорта: <b>{data.licence_series}</b>\n"
                    f"Номер паспорта: <b>{data.licence_number}</b>")
        case "en":
            return (f"Here's what I found about you in my notes:\n"
                    f"Last name: <b>{data.surname}</b>\n"
                    f"First name: <b>{data.name}</b>\n"
                    f"Middle name: <b>{data.middle_name}</b>\n"
                    f"Phone number: <b>{data.number}</b>\n"
                    f"Passport series: <b>{data.licence_series}</b>\n"
                    f"Passport number: <b>{data.licence_number}</b>")
        case "kz":
            return (f"Мен жазбамда сіз туралы мынаны таптым:\n"
                    f"Тегі: <b>{data.surname}</b>\n"
                    f"Аты: <b>{data.name}</b>\n"
                    f"Әке/Ана аты: <b>{data.middle_name}</b>\n"
                    f"Телефон нөмірі: <b>{data.number}</b>\n"
                    f"Паспортың сериясы: <b>{data.licence_series}</b>\n"
                    f"Паспортың нөмірі: <b>{data.licence_number}</b>")
        case "by":
            return (f"Вось што я знайшоў пра вас у маіх запісах:\n"
                    f"Прозвішча: <b>{data.surname}</b>\n"
                    f"Імя: <b>{data.name}</b>\n"
                    f"По бацьку: <b>{data.middle_name}</b>\n"
                    f"Нумар тэлефона: <b>{data.number}</b>\n"
                    f"Серыя паспарту: <b>{data.licence_series}</b>\n"
                    f"Нумар паспарту: <b>{data.licence_number}</b>")
        case "az":
            return (f"Qeydlərimdə siz haqqında tapdığım məlumatlar budur:\n"
                    f"Soyadı: <b>{data.surname}</b>\n"
                    f"Ad: <b>{data.name}</b>\n"
                    f"Orta ad: <b>{data.middle_name}</b>\n"
                    f"Telefon nömrəsi: <b>{data.number}</b>\n"
                    f"Pasport seriyası: <b>{data.licence_series}</b>\n"
                    f"Pasport nömrəsi: <b>{data.licence_number}</b>")
        case "uz":
            return (f"Yozuvlarimda siz haqingizda shunday topdim:\n"
                    f"Familiya: <b>{data.surname}</b>\n"
                    f"Ism: <b>{data.name}</b>\n"
                    f"O'rta ism: <b>{data.middle_name}</b>\n"
                    f"Telefon raqami: <b>{data.number}</b>\n"
                    f"Pasport seriyasi: <b>{data.licence_series}</b>\n"
                    f"Pasport raqami: <b>{data.licence_number}</b>")
        case "tg":
            return (f"Ин аст он чизе ки ман дар ёддоштҳои худ дар бораи шумо ёфтам:\n"
                    f"Насаб: <b>{data.surname}</b>\n"
                    f"Ном: <b>{data.name}</b>\n"
                    f"Номи миёна: <b>{data.middle_name}</b>\n"
                    f"Рақами телефон: <b>{data.number}</b>\n"
                    f"Силсилаи паспорт: <b>{data.licence_series}</b>\n"
                    f"Рақами паспорт: <b>{data.licence_number}</b>")
        case _:
            return "Unsupported language."








