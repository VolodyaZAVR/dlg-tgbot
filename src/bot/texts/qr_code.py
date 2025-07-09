def edit_lang_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Изменить язык"
        case "en":
            return "Change language"
        case "kz":
            return "Тілді өзгерту"
        case "by":
            return "Змяніць мову"
        case "az":
            return "Dili dəyişdirin"
        case "uz":
            return "Tilni o'zgartirish"
        case "tg":
            return "Тағир додани забон"


def has_code_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Есть код активации"
        case "en":
            return "Have an activation code"
        case "kz":
            return "Белсендіру коды бар"
        case "by":
            return "Ёсць код актывацыі"
        case "az":
            return "Aktivləşdirmə kodu var"
        case "uz":
            return "Faollashtirish kodi mavjud"
        case "tg":
            return "Рамзи фаъолсозӣ мавҷуд аст"


def no_code_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Зарегистрироваться на погрузку/разгрузку"
        case "en":
            return "Register for loading/unloading"
        case "kz":
            return "Жүктеу/түсіру үшін тіркелу"
        case "by":
            return "Зарэгістравацца на пагрузку/разгрузку"
        case "az":
            return "Yükləmə/boşaltma üçün qeydiyyatdan keçin"
        case "uz":
            return "Yuklash/tushirish uchun ro'yxatdan o'ting"
        case "tg":
            return "Барои боркунӣ/борфарорӣ сабти ном кунед"


def menu_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Вернуться в меню ↩️"
        case "en":
            return "Back to the menu ↩️"
        case "kz":
            return "Мәзірге оралу ↩️"
        case "by":
            return "Вярнуцца ў меню ↩️"
        case "az":
            return "Menyuya qayıdın ↩️"
        case "uz":
            return "Menyuga qaytish ↩️"
        case "tg":
            return "Бозгашт ба меню ↩️"


def cls_button_text(lang: str) -> str:
    if lang == "ru":
        return "Завершить работу"
    elif lang == "en":
        return "Finish the job"
    elif lang == "kz":
        return "Жұмысты аяқтаңыз"
    elif lang == "by":
        return "Скончы працу"
    elif lang == "az":
        return "İşi bitirin"
    elif lang == "uz":
        return "Ishni tugating"
    elif lang == "tg":
        return "Корро анҷом диҳед"


def activate_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Активировать код"
        case "en":
            return "Activate code"
        case "kz":
            return "Кодты іске қосыңыз"
        case "by":
            return "Актываваць код"
        case "az":
            return "Kodu aktivləşdirin"
        case "uz":
            return "Kodni faollashtirish"
        case "tg":
            return "Рамзро фаъол созед"


def request_key_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Введите, пожалуйста, ваш уникальный ключ."
        case "en":
            return "Please enter your unique number key."
        case "kz":
            return "Бірегей нөмір кілтін енгізіңіз."
        case "by":
            return "Калі ласка, увядзіце свой унікальны лічбавай ключ."
        case "az":
            return "Zəhmət olmasa unikal rəqəmsal açarınızı daxil edin."
        case "uz":
            return "Sizning noyob soni kalitini kiriting."
        case "tg":
            return "Лутфан калиди рақамии беназири худро ворид кунед."


def incorrect_key_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Вы ввели некорректный ключ. Попробуйте ещё раз."
        case "en":
            return "You entered an incorrect key. Try again."
        case "kz":
            return "Сіз қате кілт енгіздіңіз. Қайталап көріңіз."
        case "by":
            return "Вы ўвялі няправільны ключ. Спрабаваць зноў."
        case "az":
            return "Səhv açarı daxil etdiniz. Yenidən cəhd edin."
        case "uz":
            return "Siz noto'g'ri kalitni kiritdingiz. Qayta urinib ko'ring."
        case "tg":
            return "Шумо калиди нодурустро ворид кардед. Боз кӯшиш кунед."


def successful_activation_text(lang: str) -> str:
    match lang:
        case "ru":
            return '''Ваша регистрация прошла успешна. 

ПОЖАЛУЙСТА, ПОДОЙДИТЕ К ДИСПЕТЧЕРУ ДЛЯ ОФОРМЛЕНИЯ ДОКУМЕНТОВ. 

После ожидайте звонка диспетчера для постановки на ворота.'''
        case "en":
            return '''Your registration was successful.

PLEASE APPROACH THE DISPATCHER TO COMPLETE THE DOCUMENTS.

Then wait for the dispatcher to call you to set up the gate.'''
        case "kz":
            return '''Тіркелу сәтті аяқталды.

ҚҰЖАТТЫ ТОЛЫҚТАУ ҮШІН ДИСПЕТЧЕРГЕ ҚАРАҢЫЗ.

Содан кейін диспетчердің қақпаны орнату үшін қоңырау шалуын күтіңіз.'''
        case "by":
            return '''Ваша рэгістрацыя прайшла паспяховая.

Калі ласка, падыдзіце да дыспетчар для афармлення дакументаў.

Пасля чакайце званка дыспетчара для пастаноўкі на вароты.'''
        case "az":
            return '''Qeydiyyatınız uğurla keçdi.

SƏNƏDLƏRİ TAMAMLAMAQ ÜÇÜN DISPATÇERƏ BAXIN.

Sonra darvaza qurmaq üçün dispetçerin zəng etməsini gözləyin.'''
        case "uz":
            return '''Roʻyxatdan oʻtish muvaffaqiyatli oʻtdi.

HUJJATLARNI TO‘LDIRISH UCHUN DISPATCHERGA KO‘RING.

Keyin dispetcherning eshikni o'rnatish uchun qo'ng'iroq qilishini kuting.'''
        case "tg":
            return '''Бақайдгирии шумо муваффақ шуд.

БАРОИ ПУР НАМУДАНИ ХУЧЧАТХО БА ДИСПЕТЧЕР НАМОЕД.

Пас интизор шавед, ки диспетчер занг занад, то дарвозаро насб кунад.'''


def failed_activation_text(lang: str) -> str:
    match lang:
        case "ru":
            return "\nНе удалось активировать код."
        case "en":
            return "\nFailed to activate code."
        case "kz":
            return "\nКод іске қосылмады."
        case "by":
            return "\nНе ўдалося актываваць код."
        case "az":
            return "\nKodu aktivləşdirmək alınmadı."
        case "uz":
            return "\nKodni faollashtirib bo‘lmadi."
        case "tg":
            return "\nКодро фаъол карда натавонист."


def activate_key_text(lang: str, key) -> str:
    match lang:
        case "ru":
            return (f"Вот ваш код активации:"
                    f"\n\n<b>{str(key)}</b>\n\n"
                    f"Для его активации нажмите на <b>\"{activate_button_text(lang)}\"</b>.")
        case "en":
            return ("Here is your activation code:"
                    f"\n\n<b>{str(key)}</b>\n\n"
                    f"To activate it, click on <b>\"{activate_button_text(lang)}\"</b>.")
        case "kz":
            return ("Міне, сіздің белсендіру кодыңыз:"
                    f"\n\n<b>{str(key)}</b>\n\n"
                    f"Оны белсендіру үшін түймесін басыңыз <b>\"{activate_button_text(lang)}\"</b>.")
        case "by":
            return ("Вось ваш код актывацыі:"
                    f"\n\n<b>{str(key)}</b>\n\n"
                    f"Для яго актывацыі націсніце на <b>\"{activate_button_text(lang)}\"</b>.")
        case "az":
            return ("Budur aktivləşdirmə kodunuz:"
                    f"\n\n<b>{str(key)}</b>\n\n"
                    f"Aktivləşdirmək üçün üzərinə klikləyin <b>\"{activate_button_text(lang)}\"</b>.")
        case "uz":
            return ("Mana sizning faollashtirish kodingiz:"
                    f"\n\n<b>{str(key)}</b>\n\n"
                    f"Uni faollashtirish uchun ustiga bosing <b>\"{activate_button_text(lang)}\"</b>.")
        case "tg":
            return ("Ин аст рамзи фаъолсозии шумо:"
                    f"\n\n<b>{str(key)}</b>\n\n"
                    f"Барои фаъол кардани он, клик кунед <b>\"{activate_button_text(lang)}\"</b>.")


def failed_generate_key_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Не удалось сгенерировать код. Вернитесь, пожалуйста, в главное меню."
        case "en":
            return "Failed to generate code. Please return to the main menu."
        case "kz":
            return "Кодын жасау сәтсіз аяқталды. Негізгі мәзірге оралыңыз."
        case "by":
            return "Не атрымалася згенераваць код. Калі ласка, вярніцеся ў галоўнае меню."
        case "az":
            return "Kodu yaratmaq alınmadı. Lütfən, əsas menyuya qayıdın."
        case "uz":
            return "Kodni yaratib bo‘lmadi. Iltimos, asosiy menyuga qayting."
        case "tg":
            return "Ташкили рамзи ноком шуд. Лутфан ба менюи асосӣ баргардед."


def contact_dispatcher_text(lang) -> str:
    match lang:
        case "ru":
            return "Произошла ошибка. Обратитесь к диспетчеру и предоставьте ему номера заявок, на которые вы пытаетесь зарегестрироваться."
        case "en":
            return "An error occurred. Please contact the dispatcher and provide them with the application numbers you are trying to register."
        case "kz":
            return "Жоқтыру жасалды. Диспетчермен танышып, сіз регистрация жасаған заявшылардың нөмірлерін көрсетіңіз."
        case "by":
            return "Памылка адбыўся. Адваката зязрубяйце і падаеце яму заявак нумары, якім вы спрабуеце запісацца."
        case "az":
            return "Səhifədə bir xəta baş verdi. Təyinatçıya müraciət edin və səsdəki təqdimatlar nömrələrinə göstərin ki, qeydiyyata daxil olmağa cəhd edirsiniz."
        case "uz":
            return "Xato yuz berdi. Dispatcher bilan bog'laning va siz royxatdan o'tayotgan arizalar sonlarini ko'rsatingiz."
        case "tg":
            return "Парокад тӯда шуд. Адвакатро пайваста, ва умумиҳои заявкадорӣ намудон номураҳоро омехта."


def write_code_text(lang: str, key) -> str:
    match lang:
        case "ru":
            return (f"Пожалуйста, запишите ваш уникальный ключ, необходимый для активации вашей заявки на следующем этапе:"
                    f"\n\n<b>{str(key)}</b>")
        case "en":
            return ("Please write down your unique key required to activate your application at the next stage:"
                    f"\n\n<b>{str(key)}</b>")
        case "kz":
            return ("Өтінімді келесі кезеңде белсендіру үшін қажет бірегей кілтті жазып алыңыз:"
                    f"\n\n<b>{str(key)}</b>")
        case "by":
            return ("Калі ласка, запішыце ваш унікальны ключ, неабходны для актывацыі Вашай заяўкі на наступным этапе:"
                    f"\n\n<b>{str(key)}</b>")
        case "az":
            return ("Zəhmət olmasa ərizənizi növbəti addımda aktivləşdirmək üçün tələb olunan unikal açarınızı yazın:"
                    f"\n\n<b>{str(key)}</b>")
        case "uz":
            return ("Iltimos, keyingi bosqichda arizangizni faollashtirish uchun zarur bo'lgan noyob kalitingizni yozing:"
                    f"\n\n<b>{str(key)}</b>")
        case "tg":
            return ("Лутфан калиди беназири худро нависед, ки барои фаъол кардани дархости шумо дар қадами оянда лозим аст:"
                    f"\n\n<b>{str(key)}</b>")
