from src.bot.translations.orders import show_contact_point, show_job_type, get_lang_no, get_lang_yes, get_lang_partner
from typing import Optional
from src.utils.texts_utils import get_orders_in_list
from src.bot.filters.manage_access import get_stand_chat_ids


def ask_vehicle_format(lang: str) -> str:
    if lang == "ru":
        return "Выберите формат номера вашего транспортного средства"
    elif lang == "en":
        return "Please enter your vehicle number format"
    elif lang == "kz":
        return "Көлік нөмірі пішімін енгізіңіз"
    elif lang == "by":
        return "Увядзіце фармат нумара вашага транспартнага сродку"
    elif lang == "az":
        return "Avtomobil nömrənizin formatını daxil edin"
    elif lang == "uz":
        return "Avtomobil raqamingiz formatini kiriting"
    elif lang == "tg":
        return "Формати рақами мошини худро ворид кунед"


def ask_format_ru(lang: str) -> str:
    if lang == "ru":
        return "Российские номера"
    elif lang == "en":
        return "Russian license plates"
    elif lang == "kz":
        return "Ресейлік нөмірлер"
    elif lang == "by":
        return "Расійскія нумары"
    elif lang == "az":
        return "Rusiyalıq nömrələr"
    elif lang == "uz":
        return "Rossiya nomerlari"
    elif lang == "tg":
        return "Нишонаҳои рӯсиягӣ"


def ask_format_by(lang: str) -> str:
    if lang == "ru":
        return "Белорусские номера"
    elif lang == "en":
        return "Belarusian license plates"
    elif lang == "kz":
        return "Беларустік нөмірлер"
    elif lang == "by":
        return "Беларускія нумары"
    elif lang == "az":
        return "Belarusluq nömrələr"
    elif lang == "uz":
        return "Belarus nomerlari"
    elif lang == "tg":
        return "Нишонаҳои белорусӣ"


def ask_format_eu(lang: str) -> str:
    if lang == "ru":
        return "Европейские номера"
    elif lang == "en":
        return "European license plates"
    elif lang == "kz":
        return "Еуропалық нөмірлер"
    elif lang == "by":
        return "Еўрапейскія нумары"
    elif lang == "az":
        return "Avropalıq nömrələr"
    elif lang == "uz":
        return "Yevropa nomerlari"
    elif lang == "tg":
        return "Нишонаҳои аврупоӣ"


def ask_format_kz(lang: str) -> str:
    if lang == "ru":
        return "Казахские номера"
    elif lang == "en":
        return "Kazakhstani license plates"
    elif lang == "kz":
        return "Қазақстандық нөмірлер"
    elif lang == "by":
        return "Казахскія нумары"
    elif lang == "az":
        return "Qazaxıstanlıq nömrələr"
    elif lang == "uz":
        return "Qozog'iston nomerlari"
    elif lang == "tg":
        return "Нишонаҳои қозоғистонӣ"


def get_vehicle_number_example(select_format: str) -> str:
    match select_format:
        case "ru":
            return "А000АА00"
        case "by":
            return "WR0000-0"
        case "en":
            return "000WRG"
        case "kz":
            return "000WRG00"
        case _:
            raise Exception("Unexpected vehicle number format")


def ask_vehicle_number(lang: str, select_format: str) -> str:
    match lang:
        case "ru":
            return f"Введите номер транспортного средства в формате {get_vehicle_number_example(select_format)}"
        case "en":
            return f"Enter the vehicle number in the format {get_vehicle_number_example(select_format)}"
        case "kz":
            return f"{get_vehicle_number_example(select_format)} пішімі бойынша көліктің нөмірін енгізіңіз"
        case "by":
            return f"Увядзіце нумар транспартнага сродка ў фармаце {get_vehicle_number_example(select_format)}"
        case "az":
            return f"{get_vehicle_number_example(select_format)} formatında nəqliyyat vasitəsinin nömrəsini daxil edin"
        case "uz":
            return f"{get_vehicle_number_example(select_format)} formatida transport vositasining raqamini kiriting"
        case "tg":
            return f"Нишонаи гардидашудаи васитаи нақлиётии худро дар шакли {get_vehicle_number_example(select_format)} ворид намоед"


def incorrect_vehicle_number(lang: str, select_format: str) -> str:
    match lang:
        case "ru":
            return f"Вы некорректно ввели номер транспортного средства. Формат ввода: {get_vehicle_number_example(select_format)}"
        case "en":
            return f"You entered the vehicle number incorrectly. Input format: {get_vehicle_number_example(select_format)}"
        case "kz":
            return f"Сіз көліктің нөмірін дұрыс енгізген жоқсыз. Енгізу пішімі: {get_vehicle_number_example(select_format)}"
        case "by":
            return f"Вы ўвялі нумар транспартнага сродка неправільна. Фармат увядзення: {get_vehicle_number_example(select_format)}"
        case "az":
            return f"Nəqliyyat vasitəsinin nömrəsini düzgün daxil etməmisiniz. Daxilolunma formatı: {get_vehicle_number_example(select_format)}"
        case "uz":
            return f"Siz transport vositasining raqamini to'g'ri kiritmadingiz. Kirish formati: {get_vehicle_number_example(select_format)}"
        case "tg":
            return f"Шумо нишонаи гардидашудаи васитаи нақлиётии худро дуруст ворид накардаед. Формати воридкунӣ: {get_vehicle_number_example(select_format)}"


def ask_trailer_format(lang: str) -> str:
    match lang:
        case "ru":
            return "Выберите формат номера прицепа"
        case "en":
            return "Select the trailer number format"
        case "kz":
            return "Прицептің нөмірінің пішімін таңдаңыз"
        case "by":
            return "Выберыце фармат нумара прычэпа"
        case "az":
            return "Rəqəm formatını seçin"
        case "uz":
            return "Prichip nomerining formatini tanlang"
        case "tg":
            return "Формати нишонаи трейлериро интихоб кунед"


def get_trailer_number_example(select_format: str) -> str:
    match select_format:
        case "ru":
            return "АА000078"
        case "by":
            return "W0000R-0"
        case "en":
            return "WRG0000WRG"
        case "kz":
            return "WRG0000"
        case default:
            raise Exception("Unexpected vehicle number format")


def ask_trailer_number(lang: str, select_format: str) -> str:
    match lang:
        case "ru":
            return f"Введите номер прицепа в формате {get_trailer_number_example(select_format)}"
        case "en":
            return f"Enter the trailer number in the format {get_trailer_number_example(select_format)}"
        case "kz":
            return f"{get_trailer_number_example(select_format)} пішімі бойынша прицептің нөмірін енгізіңіз"
        case "by":
            return f"Увядзіце нумар прычэпа ў фармаце {get_trailer_number_example(select_format)}"
        case "az":
            return f"{get_trailer_number_example(select_format)} formatında rəqəmi daxil edin"
        case "uz":
            return f"{get_trailer_number_example(select_format)} formatida prichipning raqamini kiriting"
        case "tg":
            return f"Нишонаи трейлериро дар шакли {get_trailer_number_example(select_format)} ворид намоед"


def incorrect_trailer_number(lang: str, select_format: str) -> str:
    match lang:
        case "ru":
            return f"Вы некорректно ввели номер прицепа. Формат ввода: {get_trailer_number_example(select_format)}"
        case "en":
            return f"You entered the trailer number incorrectly. Input format: {get_trailer_number_example(select_format)}"
        case "kz":
            return f"Сіз прицептің нөмірін дұрыс енгізген жоқсыз. Енгізу пішімі: {get_trailer_number_example(select_format)}"
        case "by":
            return f"Вы ўвялі нумар прычэпа неправільна. Фармат увядзення: {get_trailer_number_example(select_format)}"
        case "az":
            return f"Treylerin nömrəsini düzgün daxil etməmisiniz. Daxilolunma formatı: {get_trailer_number_example(select_format)}"
        case "uz":
            return f"Siz prichipning raqamini to'g'ri kiritmadingiz. Kirish formati: {get_trailer_number_example(select_format)}"
        case "tg":
            return f"Шумо нишонаи трейлериро дуруст ворид накардаед. Формати воридкунӣ: {get_trailer_number_example(select_format)}"


def get_lang_enter_vehicle_number(lang: str) -> str:
    if lang == "ru":
        return "Введите номер ТС (транспортного средства) в формате А000АА00."
    elif lang == "en":
        return "Enter the vehicle registration number in the format A000AA00."
    elif lang == "kz":
        return "ТС (транспорттық құрал) нөмірін А000АА00 форматы бойынша енгізіңіз."
    elif lang == "by":
        return "Увядзіце нумар ТС (транспартнага сродку) у фармаце А000АА00."
    elif lang == "az":
        return "TS (nəqliyyat vasitəsi) nömrəsini A000AA00 formatında daxil edin."
    elif lang == "uz":
        return "ТС (transport vositasi) raqamini A000AA00 formatida kiriting."
    elif lang == "tg":
        return "Рақами ТС (ваҳати нақлиёт) дар формати А000АА00 ворид кунед."


def get_lang_incorrect_vehicle_number(lang: str) -> str:
    if lang == "ru":
        return "Вы ввели некорректный номер ТС. Формат ввода А000АА00."
    elif lang == "en":
        return "You have entered an incorrect vehicle number. Input format A000AA00."
    elif lang == "kz":
        return "Сіз көлік нөмірін қате енгіздіңіз. Енгізу пішімі A000AA00."
    elif lang == "by":
        return "Вы ўвялі некарэктны нумар МС. Фармат уводу А000АА00."
    elif lang == "az":
        return "Yanlış avtomobil nömrəsi daxil etmisiniz. Daxiletmə formatı A000AA00."
    elif lang == "uz":
        return "Siz mashina raqamini noto‘g‘ri kiritdingiz. Kirish formati A000AA00."
    elif lang == "tg":
        return "Шумо рақами мошинро нодуруст ворид кардед. Формати вуруд A000AA00."


def get_lang_enter_trailer_number(lang: str) -> str:
    if lang == "ru":
        return "Введите номер вашего прицепа в формате AA0000."
    elif lang == "en":
        return "Please enter your trailer number in the format AA0000."
    elif lang == "kz":
        return "Трейлер нөміріңізді AA0000 пішімінде енгізіңіз."
    elif lang == "by":
        return "Увядзіце нумар вашага прычэпа ў фармаце AA0000."
    elif lang == "az":
        return "Treyler nömrənizi AA0000 formatında daxil edin."
    elif lang == "uz":
        return "Treyler raqamingizni AA0000 formatida kiriting."
    elif lang == "tg":
        return "Рақами трейлери худро дар формати AA0000 ворид кунед."


def get_lang_incorrect_trailer_number(lang: str) -> str:
    if lang == "ru":
        return "Вы некорректно ввели номер прицепа. Формат ввода: AA0000."
    elif lang == "en":
        return "You have entered the trailer number incorrectly. Input format: AA0000."
    elif lang == "kz":
        return "Сіз трейлер нөмірін қате енгіздіңіз. Енгізу пішімі: AA0000."
    elif lang == "by":
        return "Вы некарэктна ўвялі нумар прычэпа. Фармат уводу: AA0000."
    elif lang == "az":
        return "Treyler nömrəsini səhv daxil etmisiniz. Daxiletmə formatı: AA0000."
    elif lang == "uz":
        return "Treyler raqamini noto'g'ri kiritdingiz. Kirish formati: AA0000."
    elif lang == "tg":
        return "Шумо рақами трейлерро нодуруст ворид кардед. Формати вуруд: AA0000."


def get_lang_indicate_trailer(lang: str) -> str:
    if lang == "ru":
        return "Укажите, есть ли у вас прицеп?"
    elif lang == "en":
        return "Indicate if you have a trailer."
    elif lang == "kz":
        return "Сізде тіркеменің бар екенін көрсетіңіз."
    elif lang == "by":
        return "Укажыце, ці ёсць у вас прычэп."
    elif lang == "az":
        return "Sizdə qoşqunun olub-olmadığını göstərin."
    elif lang == "uz":
        return "Sizda prikup borligini ko'rsating."
    elif lang == "tg":
        return "Маълум кунед, ки оё шумо прицеп доред."


def get_lang_load_capacity_class(lang: str) -> str:
    if lang == "ru":
        return "Класс грузоподъемности вашего транспортного средства больше 1,5 тонн?"
    elif lang == "en":
        return "Is the load capacity class of your vehicle more than 1.5 tons?"
    elif lang == "kz":
        return "Сіздің көлігіңіздің жүк көтеру класы 1,5 тоннадан көп пе?"
    elif lang == "by":
        return "Клас грузападымнасці вашага транспартнага сродку больш за 1,5 тонны?"
    elif lang == "az":
        return "Nəqliyyat vasitənizin yük qaldırma sinfi 1,5 tondan çoxdurmu?"
    elif lang == "uz":
        return "Transport vositangizning yuk ko'tarish klassi 1,5 tonnadan ortiqmi?"
    elif lang == "tg":
        return "Класси боркашии воситаи нақлиётатон бештар аз 1,5 тонна аст?"


def get_lang_more(lang: str) -> str:
    if lang == "ru":
        return "Больше"
    elif lang == "en":
        return "More"
    elif lang == "kz":
        return "Көп"
    elif lang == "by":
        return "Больш"
    elif lang == "az":
        return "Daha çox"
    elif lang == "uz":
        return "Ko'proq"
    elif lang == "tg":
        return "Бештар"


def get_lang_less(lang: str) -> str:
    if lang == "ru":
        return "Меньше"
    elif lang == "en":
        return "Less"
    elif lang == "kz":
        return "Аз"
    elif lang == "by":
        return "Менш"
    elif lang == "az":
        return "Az"
    elif lang == "uz":
        return "Kam"
    elif lang == "tg":
        return "Камтар"


def get_generate_qr_text(lang: str) -> str:
    if lang == "ru":
        return "Сгенерировать QR код"
    elif lang == "en":
        return "Generate QR code"
    elif lang == "kz":
        return "QR кодын жасаңыз"
    elif lang == "by":
        return "Згенераваць QR код"
    elif lang == "az":
        return "QR kodu yaradın"
    elif lang == "uz":
        return "QR kodini yarating"
    elif lang == "tg":
        return "Эҷоди рамзи QR"


def get_generate_code_text(lang: str) -> str:
    if lang == "ru":
        return "Сгенерировать код активации"
    elif lang == "en":
        return "Generate activation code"
    elif lang == "kz":
        return "Белсендіру кодын жасаңыз"
    elif lang == "by":
        return "Згенераваць код актывацыі"
    elif lang == "az":
        return "Aktivləşdirmə kodu yaradın"
    elif lang == "uz":
        return "Faollashtirish kodini yarating"
    elif lang == "tg":
        return "Эҷоди рамзи фаъолсозӣ"


def activate_code_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Отправить данные"
        case "en":
            return "Submit data"
        case "kz":
            return "Деректерді жіберу"
        case "by":
            return "Адправіць дадзеныя"
        case "az":
            return "Məlumat göndərin"
        case "uz":
            return "Ma'lumotlarni yuborish"
        case "tg":
            return "Маълумотро пешниҳод кунед"


def ask_edit_tc(lang: str) -> str:
    if lang == "ru":
        return "Изменить номер ТС"
    elif lang == "en":
        return "Edit vehicle number"
    elif lang == "kz":
        return "Көлік нөмірін өзгерту"
    elif lang == "by":
        return "Змяніць нумар МС"
    elif lang == "az":
        return "Avtomobil nömrəsini dəyişdirin"
    elif lang == "uz":
        return "Avtomobil raqamini o'zgartirish"
    elif lang == "tg":
        return "Рақами мошинро тағир диҳед"


def ask_edit_trailer(lang: str) -> str:
    if lang == "ru":
        return "Изменить данные о прицепе"
    elif lang == "en":
        return "Edit trailer details"
    elif lang == "kz":
        return "Трейлер мәліметтерін өзгерту"
    elif lang == "by":
        return "Змяніць дадзеныя аб прычэпе"
    elif lang == "az":
        return "Treyler təfərrüatlarını dəyişdirin"
    elif lang == "uz":
        return "Treyler tafsilotlarini o'zgartirish"
    elif lang == "tg":
        return "Тағйир додани тафсилоти трейлер"


def get_lang_edit_tc_weight(lang: str) -> str:
    if lang == "ru":
        return "Изменить вес ТС"
    elif lang == "en":
        return "Edit vehicle weight"
    elif lang == "kz":
        return "Көліктің салмағын өзгерту"
    elif lang == "by":
        return "Змяніць вагу МС"
    elif lang == "az":
        return "Avtomobilin çəkisini dəyişdirin"
    elif lang == "uz":
        return "Avtomobil og'irligini o'zgartiring"
    elif lang == "tg":
        return "Вазни мошинро тағир диҳед"


def ask_edit_has_trailer(lang: str) -> str:
    if lang == "ru":
        return "Изменить наличие прицепа"
    elif lang == "en":
        return "Edit trailer availability"
    elif lang == "kz":
        return "Трейлердің қолжетімділігін өзгерту"
    elif lang == "by":
        return "Змяніць наяўнасць прычэпа"
    elif lang == "az":
        return "Treylerin mövcudluğunu dəyişdirin"
    elif lang == "uz":
        return "Treyler mavjudligini o'zgartirish"
    elif lang == "tg":
        return "Тағйир додани дастрасии трейлер"


def ask_edit_trailer_number(lang: str) -> str:
    if lang == "ru":
        return "Изменить номер прицепа"
    elif lang == "en":
        return "Edit trailer number"
    elif lang == "kz":
        return "Трейлер нөмірін өзгерту"
    elif lang == "by":
        return "Змяніць нумар прычэпа"
    elif lang == "az":
        return "Treyler nömrəsini dəyişdirin"
    elif lang == "uz":
        return "Treyler raqamini o'zgartiring"
    elif lang == "tg":
        return "Рақами трейлерро иваз кунед"


def ask_edit_vehicle(lang: str) -> str:
    if lang == "ru":
        return "Изменить данные о ТС"
    elif lang == "en":
        return "Edit vehicle information"
    elif lang == "kz":
        return "Көліктің деректерін өзгерту"
    elif lang == "by":
        return "Змяніць дадзеныя аб транспартным сродку"
    elif lang == "az":
        return "Nəqliyyat vasitəsinin məlumatlarını redaktə edin"
    elif lang == "uz":
        return "Transport vositali ma'lumotlarini tahrirlash"
    elif lang == "tg":
        return "Вироиш кардан намуди маълумоти воситаи нақлиёт"


def ask_edit_format(lang: str) -> str:
    if lang == "ru":
        return "Изменить формат номера"
    elif lang == "en":
        return "Edit number format"
    elif lang == "kz":
        return "Нөмірдің пішімін өзгерту"
    elif lang == "by":
        return "Змяніць фармат нумара"
    elif lang == "az":
        return "Nömrənin formatını dəyişmək"
    elif lang == "uz":
        return "Raqam formatini o'zgartirish"
    elif lang == "tg":
        return "Вироиш кардани шакли рақам"


def get_all_user_data(lang: str, data: dict, user, order_data, orders) -> str:
    match lang:
        case "ru":
            return (f"Проверьте введенные вами данные:\n\n"
                    f"Фамилия: <b>{user.surname}</b>\n"
                    f"Имя: <b>{user.name}</b>\n"
                    f"Отчество: <b>{user.middle_name}</b>\n"
                    f"Номер: <b>{user.number}</b>\n"
                    f"Серия паспорта: <b>{user.licence_series}</b>\n"
                    f"Номер паспорта:<b> {user.licence_number}</b>\n"
                    f"Площадка: <b>{show_contact_point(order_data.contact_point, lang)}</b>\n"
                    f"Цель визита: <b>{show_job_type(order_data.job_type, lang)}</b>\n"
                    + get_orders_in_list(orders) +
                    f"{get_lang_partner(lang)}: <b>{order_data.partner}</b>\n"
                    f"Номер ТС: <b>{data['vehicle_number']}</b>\n"
                    + show_trailer_number(lang, bool(data["trailer"]), data["trailer_number"]) +
                    f"Класс грузоподъемности в 1,5 тонны: <b>{show_trailer_weight(lang, data['trailer_weight'])}</b>\n\n")
        case "en":
            return (f"Check the data you entered:\n\n"
                    f"Last name: <b>{user.surname}</b>\n"
                    f"First name: <b>{user.name}</b>\n"
                    f"Patronymic: <b>{user.middle_name}</b>\n"
                    f"Number: <b>{user.number}</b>\n"
                    f"Passport series: <b>{user.licence_series}</b>\n"
                    f"Passport number:<b> {user.licence_number}</b>\n"
                    f"Site: <b>{show_contact_point(order_data.contact_point, lang)}</b>\n"
                    f"Purpose of visit: <b>{show_job_type(order_data.job_type, lang)}</b>\n"
                    + get_orders_in_list(orders) +
                    f"{get_lang_partner(lang)}: <b>{order_data.partner}</b>\n"
                    f"Vehicle number: <b>{data['vehicle_number']}</b>\n"
                    + show_trailer_number(lang, bool(data["trailer"]), data["trailer_number"]) +
                    f"1.5 ton load class: <b>{show_trailer_weight(lang, data['trailer_weight'])}</b>\n\n")
        case "kz":
            return (f"Енгізген ақпаратты тексеріңіз:\n\n"
                    f"Тегі: <b>{user.surname}</b>\n"
                    f"Аты: <b>{user.name}</b>\n"
                    f"Әкесінің аты: <b>{user.middle_name}</b>\n"
                    f"Нөмір: <b>{user.number}</b>\n"
                    f"Паспортың сериясы: <b>{user.licence_series}</b>\n"
                    f"Паспортың нөмірі:<b> {user.licence_number}</b>\n"
                    f"Сайт: <b>{show_contact_point(order_data.contact_point, lang)}</b>\n"
                    f"Бару мақсаты: <b>{show_job_type(order_data.job_type, lang)}</b>\n"
                    + get_orders_in_list(orders) +
                    f"{get_lang_partner(lang)}: <b>{order_data.partner}</b>\n"
                    f"Көлік нөмірі: <b>{data['vehicle_number']}</b>\n"
                    + show_trailer_number(lang, bool(data["trailer"]), data["trailer_number"]) +
                    f"1,5 тонна сыйымдылық класы: <b>{show_trailer_weight(lang, data['trailer_weight'])}</b>\n\n")
        case "by":
            return (f"Праверце ўведзеныя вамі дадзеныя:\n\n"
                    f"Прозвішча: <b>{user.surname}</b>\n"
                    f"Імя: <b>{user.name}</b>\n"
                    f"Імя па бацьку: <b>{user.middle_name}</b>\n"
                    f"Нумар: <b>{user.number}</b>\n"
                    f"Серыя паспарту: <b>{user.licence_series}</b>\n"
                    f"Нумар паспарту:<b> {user.licence_number}</b>\n"
                    f"Пляцоўка: <b>{show_contact_point(order_data.contact_point, lang)}</b>\n"
                    f"Мэта візіту: <b>{show_job_type(order_data.job_type, lang)}</b>\n"
                    + get_orders_in_list(orders) +
                    f"{get_lang_partner(lang)}: <b>{order_data.partner}</b>\n"
                    f"Нумар МС: <b>{data['vehicle_number']}</b>\n"
                    + show_trailer_number(lang, bool(data["trailer"]), data["trailer_number"]) +
                    f"Клас грузападымальнасці ў 1,5 тоны: <b>{show_trailer_weight(lang, data['trailer_weight'])}</b>\n\n")
        case "az":
            return (f"Daxil etdiyiniz məlumatı yoxlayın:\n\n"
                    f"Soyadı: <b>{user.surname}</b>\n"
                    f"Ad: <b>{user.name}</b>\n"
                    f"Orta ad: <b>{user.middle_name}</b>\n"
                    f"Nömrə: <b>{user.number}</b>\n"
                    f"Pasport seriyası: <b>{user.licence_series}</b>\n"
                    f"Pasport nömrəsi:<b> {user.licence_number}</b>\n"
                    f"Sayt: <b>{show_contact_point(order_data.contact_point, lang)}</b>\n"
                    f"Səfər məqsədi: <b>{show_job_type(order_data.job_type, lang)}</b>\n"
                    + get_orders_in_list(orders) +
                    f"{get_lang_partner(lang)}: <b>{order_data.partner}</b>\n"
                    f"Maşın nömrəsi: <b>{data['vehicle_number']}</b>\n"
                    + show_trailer_number(lang, bool(data["trailer"]), data["trailer_number"]) +
                    f"1,5 ton tutum sinfi: <b>{show_trailer_weight(lang, data['trailer_weight'])}</b>\n\n")
        case "uz":
            return (f"Kiritilgan ma'lumotlarni tekshiring:\n\n"
                    f"Familiya: <b>{user.surname}</b>\n"
                    f"Ism: <b>{user.name}</b>\n"
                    f"O'rta ism: <b>{user.middle_name}</b>\n"
                    f"Raqam: <b>{user.number}</b>\n"
                    f"Pasport seriyasi: <b>{user.licence_series}</b>\n"
                    f"Pasport raqami:<b> {user.licence_number}</b>\n"
                    f"Sayt: <b>{show_contact_point(order_data.contact_point, lang)}</b>\n"
                    f"Tashrifdan maqsad: <b>{show_job_type(order_data.job_type, lang)}</b>\n"
                    + get_orders_in_list(orders) +
                    f"{get_lang_partner(lang)}: <b>{order_data.partner}</b>\n"
                    f"Avtomobil raqami: <b>{data['vehicle_number']}</b>\n"
                    + show_trailer_number(lang, bool(data["trailer"]), data["trailer_number"]) +
                    f"1,5 tonna sig'im klassi: <b>{show_trailer_weight(lang, data['trailer_weight'])}</b>\n\n")
        case "tg":
            return (f"Маълумоти воридкардаатонро санҷед:\n\n"
                    f"Насаб: <b>{user.surname}</b>\n"
                    f"Номи аввал: <b>{user.name}</b>\n"
                    f"Номи падар: <b>{user.middle_name}</b>\n"
                    f"Рақам: <b>{user.number}</b>\n"
                    f"Силсилаи паспорт: <b>{user.licence_series}</b>\n"
                    f"Рақами паспорт:<b> {user.licence_number}</b>\n"
                    f"Сомона: <b>{show_contact_point(order_data.contact_point, lang)}</b>\n"
                    f"Мақсади боздид: <b>{show_job_type(order_data.job_type, lang)}</b>\n"
                    + get_orders_in_list(orders) +
                    f"{get_lang_partner(lang)}: <b>{order_data.partner}</b>\n"
                    f"Рақами мошин: <b>{data['vehicle_number']}</b>\n"
                    + show_trailer_number(lang, bool(data["trailer"]), data["trailer_number"]) +
                    f"Кинфи бори 1,5 тонна: <b>{show_trailer_weight(lang, data['trailer_weight'])}</b>\n\n")
        case _:
            return "Unsupported language."


def get_comment_text_for_user(lang: str) -> str:
    if lang == "ru":
        return (f"Для изменения данных нажмите кнопку <b>\"Изменить\"</b>.\n"
                f"Для генерации 6-ти значного кода, необходимого для активации вашей заявки на следующем этапе, "
                f"нажмите <b>\"{get_generate_code_text(lang)}\"</b>.")
    elif lang == "en":
        return (f"To change the data, click the <b>\"Edit\"</b> button.\n"
                f"To generate the 6-digit code required to activate your application at the next stage, "
                f"press <b>\"{get_generate_code_text(lang)}\"</b>.")
    elif lang == "kz":
        return (f"Деректерді өзгерту үшін <b>\"Өзгерту\"</b> түймесін басыңыз.\n"
                f"Келесі қадамда қолданбаны белсендіру үшін қажетті 6 таңбалы кодты жасау үшін, "
                f"түймесін басыңыз <b>\"{get_generate_code_text(lang)}\"</b>.")
    elif lang == "by":
        return (f"Для змены дадзеных націсніце кнопку <b>\"Змяніць\"</b>.\n"
                f"Каб згенераваць 6-значны код, неабходны для актывацыі вашага прыкладання на наступным этапе, "
                f"націсніце <b>\"{get_generate_code_text(lang)}\"</b>.")
    elif lang == "az":
        return (f"Məlumatı dəyişmək üçün <b>\"Dəyişdir\"</b> düyməsini klikləyin.\n"
                f"Növbəti mərhələdə tətbiqinizi aktivləşdirmək üçün lazım olan 6 rəqəmli kodu yaratmaq üçün "
                f"<b>\"{get_generate_code_text(lang)}\"</b> düyməsini basın.")
    elif lang == "uz":
        return (f"Ma'lumotlarni o'zgartirish uchun <b>\"O'zgartirish\"</b> tugmasini bosing.\n"
                f"Keyingi bosqichda ilovangizni faollashtirish uchun zarur bo'lgan 6 xonali kodni yaratish uchun "
                f"<b>\"{get_generate_code_text(lang)}\"</b>tugmasini bosing.")
    elif lang == "tg":
        return (f"Барои тағир додани маълумот, тугмаи <b>\"Таҳрир\"</b> -ро клик кунед.\n"
                f"Барои тавлиди рамзи 6-рақама, ки барои фаъол кардани барномаи шумо дар қадами оянда лозим аст, "
                f"<b>\"{get_generate_code_text(lang)}\"</b>-ро пахш кунед.")


def get_comment_text_for_stand(lang: str) -> str:
    if lang == "ru":
        return (f"Для изменения данных нажмите кнопку <b>\"Изменить\"</b>.\n"
                f"Для завершения регистрации, "
                f"нажмите <b>\"{activate_code_button_text(lang)}\"</b>.")
    elif lang == "en":
        return (f"To change the data, click the <b>\"Edit\"</b> button.\n"
                f"To complete registration, "
                f"press <b>\"{activate_code_button_text(lang)}\"</b>.")
    elif lang == "kz":
        return (f"Деректерді өзгерту үшін <b>\"Өзгерту\"</b> түймесін басыңыз.\n"
                f"Тіркеуді аяқтау үшін, "
                f"түймесін басыңыз <b>\"{activate_code_button_text(lang)}\"</b>.")
    elif lang == "by":
        return (f"Для змены дадзеных націсніце кнопку <b>\"Змяніць\"</b>.\n"
                f"Для завяршэння рэгістрацыі, "
                f"націсніце <b>\"{activate_code_button_text(lang)}\"</b>.")
    elif lang == "az":
        return (f"Məlumatı dəyişmək üçün <b>\"Dəyişdir\"</b> düyməsini klikləyin.\n"
                f"Qeydiyyatı tamamlamaq üçün "
                f"<b>\"{activate_code_button_text(lang)}\"</b> düyməsini basın.")
    elif lang == "uz":
        return (f"Ma'lumotlarni o'zgartirish uchun <b>\"O'zgartirish\"</b> tugmasini bosing.\n"
                f"Ro'yxatdan o'tishni yakunlash uchun "
                f"<b>\"{activate_code_button_text(lang)}\"</b>tugmasini bosing.")
    elif lang == "tg":
        return (f"Барои тағир додани маълумот, тугмаи <b>\"Таҳрир\"</b> -ро клик кунед.\n"
                f"Барои анҷом додани сабти ном, "
                f"<b>\"{activate_code_button_text(lang)}\"</b>-ро пахш кунед.")


def show_full_info_vehicle(lang: str, data: dict, user, order_data, orders, user_id) -> str:
    if user_id in get_stand_chat_ids():
        return get_all_user_data(lang, data, user, order_data, orders) + get_comment_text_for_stand(lang)
    else:
        return get_all_user_data(lang, data, user, order_data, orders) + get_comment_text_for_user(lang)


def show_trailer_number(lang: str, has_trailer: bool, trailer_number: Optional[str]):
    if has_trailer:
        return show_has_trailer_info(lang, trailer_number)
    else:
        return show_no_trailer(lang)


def show_has_trailer_info(lang: str, trailer_number: Optional[str]) -> str:
    if lang == "ru":
        return f"Наличие прицепа: <b>{get_lang_yes(lang)}</b>.\nНомер прицепа: <b>{trailer_number}</b>.\n"
    elif lang == "en":
        return f"Trailer availability: <b>{get_lang_yes(lang)}</b>.\nTrailer number: <b>{trailer_number}</b>.\n"
    elif lang == "kz":
        return f"Трейлердің қолжетімділігі: <b>{get_lang_yes(lang)}</b>.\nТрейлер нөмірі: <b>{trailer_number}</b>.\n"
    elif lang == "by":
        return f"Наяўнасць прычэпа: <b>{get_lang_yes(lang)}</b>.\nНумар прычэпа: <b>{trailer_number}</b>.\n"
    elif lang == "az":
        return f"Treylerin mövcudluğu: <b>{get_lang_yes(lang)}</b>.\nTreyler nömrəsi: <b>{trailer_number}</b>.\n"
    elif lang == "uz":
        return f"Treyler mavjudligi: <b>{get_lang_yes(lang)}</b>.\nTreyler raqami: <b>{trailer_number}</b>.\n"
    elif lang == "tg":
        return f"Мавҷудияти трейлер: <b>{get_lang_yes(lang)}</b>.\nРақами трейлер: <b>{trailer_number}</b>.\n"


def show_no_trailer(lang: str) -> str:
    if lang == "ru":
        return f"Наличие прицепа: <b>{get_lang_no(lang)}</b>.\n"
    elif lang == "en":
        return f"Trailer availability: <b>{get_lang_no(lang)}</b>.\n"
    elif lang == "kz":
        return f"Трейлердің қолжетімділігі: <b>{get_lang_no(lang)}</b>.\n"
    elif lang == "by":
        return f"Наяўнасць прычэпа: <b>{get_lang_no(lang)}</b>.\n"
    elif lang == "az":
        return f"Treylerin mövcudluğu: <b>{get_lang_no(lang)}</b>.\n"
    elif lang == "uz":
        return f"Treyler mavjudligi: <b>{get_lang_no(lang)}</b>.\n"
    elif lang == "tg":
        return f"Мавҷудияти трейлер: <b>{get_lang_no(lang)}</b>.\n"


def show_trailer_weight(lang: str, trailer_weight) -> str:
    if trailer_weight == "Да":
        return get_lang_yes(lang)
    elif trailer_weight == "Нет":
        return get_lang_no(lang)
    else:
        return "Error"


def ask_edit_personal_data(lang: str) -> str:
    match lang:
        case "ru":
            return "Изменить персональные данные"
        case "en":
            return "Edit personal data"
        case "kz":
            return "Өзгерту жасаған өзінің атауындағы мәліметтері"
        case "by":
            return "Змяніць асабістую інфармацыю"
        case "az":
            return "Şəxsi məlumatları dəyişmək"
        case "uz":
            return "Shaxsiy ma'lumotlarini o'zgartirish"
        case "tg":
            return "Вироиш кардани меъёши шахси"
