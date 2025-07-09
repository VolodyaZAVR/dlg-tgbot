from src.utils.texts_utils import get_orders_with_sheets_statis, get_orders_with_status, \
    get_orders_with_green_icon, get_orders_in_list


def ask_point_text(lang: str) -> str:
    if lang == "ru":
        return "На какую площадку вы приедете?"
    elif lang == "en":
        return "Which venue will you arrive at?"
    elif lang == "kz":
        return "Сіз қай алаңға келесіз?"
    elif lang == "by":
        return "На якую пляцоўку вы прыедзеце?"
    elif lang == "az":
        return "Hansı meydana gələcəksiniz?"
    elif lang == "uz":
        return "Qaysi maydonga borasiz?"
    elif lang == "tg":
        return "Ба кадом майдон меоед?"


def get_first_point_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Московское шоссе 19"
    elif lang == "en":
        return "Moskovskoye Highway 19"
    elif lang == "kz":
        return "Мәскеу тас жолы 19"
    elif lang == "by":
        return "Маскоўскае шасэ 19"
    elif lang == "az":
        return "Moskva şossesi 19"
    elif lang == "uz":
        return "Moskva shossesi 19"
    elif lang == "tg":
        return "Шоссеи Москва 19"


def get_second_point_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Московское шоссе 70"
    elif lang == "en":
        return "Moskovskoye Highway 70"
    elif lang == "kz":
        return "Мәскеу тас жолы 70"
    elif lang == "by":
        return "Маскоўскае шасэ 70"
    elif lang == "az":
        return "Moskva şossesi 70"
    elif lang == "uz":
        return "Moskva shossesi 70"
    elif lang == "tg":
        return "Шоссеи Москва 70"


def get_third_point_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Уткина Заводь"
    elif lang == "en":
        return "Utkina Zavod"
    elif lang == "kz":
        return "Уткинаның Заводы"
    elif lang == "by":
        return "Уткіна Заводзь"
    elif lang == "az":
        return "Utkina Zavod"
    elif lang == "uz":
        return "Utkina Zavod"
    elif lang == "tg":
        return "Заводи Уткина"


def get_fourth_point_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Открытая площадка"
        case "en":
            return "Open Plaza"
        case "kz":
            return "Ашық алаң"
        case "by":
            return "Адкрытае плошча"
        case "az":
            return "Açık Sahə"
        case "uz":
            return "Ochiq Maydon"
        case "tg":
            return "Майдони отвора"


def get_fifth_point_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Курьерский проезд 8"
        case "en":
            return "Courier Passage 8"
        case "kz":
            return "Курьерлік жол 8"
        case "by":
            return "Кур'ерская вуліца 8"
        case "az":
            return "Kuryer Yol 8"
        case "uz":
            return "Kuryer Yo'li 8"
        case "tg":
            return "Раҳи курьерӣ 8"


def ask_job_type_text(lang: str) -> str:
    if lang == "ru":
        return "Цель вашего визита?"
    elif lang == "en":
        return "What is the purpose of your visit?"
    elif lang == "kz":
        return "Сіздің сапарыңыздың мақсаты?"
    elif lang == "by":
        return "Мэта вашага візіту?"
    elif lang == "az":
        return "Səfərinizin məqsədi nədir?"
    elif lang == "uz":
        return "Tashrifingiz maqsadi nima?"
    elif lang == "tg":
        return "Мақсади боздиди шумо чӣ аст?"


def get_job_first_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Я привез груз"
    elif lang == "en":
        return "I brought the cargo"
    elif lang == "kz":
        return "Мен жүк әкелдім"
    elif lang == "by":
        return "Я прывёз груз"
    elif lang == "az":
        return "Mən yük gətirdim"
    elif lang == "uz":
        return "Men yuk olib keldim"
    elif lang == "tg":
        return "Ман бор овардам"


def get_job_second_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Я забираю груз"
    elif lang == "en":
        return "I am picking up the cargo"
    elif lang == "kz":
        return "Мен жүкті алып жатырмын"
    elif lang == "by":
        return "Я забіраю груз"
    elif lang == "az":
        return "Mən yükü götürürəm"
    elif lang == "uz":
        return "Men yukni olib ketyapman"
    elif lang == "tg":
        return "Ман борро мегирам"


def ask_order_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Введите номера заявок через пробел:"
        case "en":
            return "Please enter the application numbers separated by spaces:"
        case "kz":
            return "Пробелмен бөлінген өтініш нөмірлерін енгізіңіз:"
        case "by":
            return "Увядзіце нумары заяўак праз праліц:"
        case "az":
            return "Zəhmət olmasa, müraciət nömrələrini boşluqla ayırıb daxil edin:"
        case "uz":
            return "Iltimos, ariza raqamlarini bo'sh joy bilan ajratib kiriting:"
        case "tg":
            return "Лутфан, рақамҳои дархостро бо жод вақтида ворид кунед:"


def ask_another_order_text(lang: str) -> str:
    if lang == "ru":
        return "Укажите, пожалуйста, есть у вас ещё заявки?"
    elif lang == "en":
        return "Please specify if you have any other applications?"
    elif lang == "kz":
        return "Сізде тағы өтініштер бар ма, көрсетіңізші?"
    elif lang == "by":
        return "Калі ласка, пакажыце, ці ёсць у вас яшчэ заяўкі?"
    elif lang == "az":
        return "Zəhmət olmasa, başqa müraciətləriniz varmı, göstərin?"
    elif lang == "uz":
        return "Iltimos, sizda yana arizalar bormi, ko'rsating?"
    elif lang == "tg":
        return "Лутфан, нишон диҳед, ки дархостҳои дигар доред?"


def get_orders_info_text(lang: str, data: dict) -> str:
    if lang == "ru":
        return (f"Проверьте введенные вами данные:\n\n"
                f"Площадка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Цель визита: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Ваши заявки:\n" +
                get_orders_in_list(data['orders']) +
                f"Для изменения данных нажмите кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для отправки заявок на проверку нажмите <b>{send_to_review_button_text(lang)}</b>.")
    elif lang == "en":
        return (f"Please check the information you have entered:\n\n"
                f"Site: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Purpose of visit: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Your applications:\n" +
                get_orders_in_list(data['orders']) +
                f"To modify the data, press the <b>{edit_data_button_text(lang)}</b> button.\n"
                f"To submit the applications for verification, press <b>{send_to_review_button_text(lang)}</b> for review.")
    elif lang == "kz":
        return (f"Кіргізген деректеріңізді тексеріңіз:\n\n"
                f"Алаң: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Келу мақсаты: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Сіздің өтініштеріңіз:\n" +
                get_orders_in_list(data['orders']) +
                f"Деректерді өзгерту үшін <b>{edit_data_button_text(lang)}</b> түймесін басыңыз.\n"
                f"Өтініштерді тексеруге жіберу үшін <b>{send_to_review_button_text(lang)}</b> түймесін басыңыз.")
    elif lang == "by":
        return (f"Праверце ўведзеныя вамі дадзеныя:\n\n"
                f"Пляцоўка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мэта візіту: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Вашы заяўкі:\n" +
                get_orders_in_list(data['orders']) +
                f"Для змянення дадзеных націсніце кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для адпраўкі заяў на праверку націсніце <b>{send_to_review_button_text(lang)}</b>")
    elif lang == "az":
        return (f"Daxil etdiyiniz məlumatları yoxlayın:\n\n"
                f"Meydança: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Ziyarət məqsədi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizin müraciətləriniz:\n" +
                get_orders_in_list(data['orders']) +
                f"Məlumatları dəyişdirmək üçün <b>{edit_data_button_text(lang)}</b> düyməsini basın.\n"
                f"Müraciətləri yoxlamağa göndərmək üçün <b>{send_to_review_button_text(lang)}</b> düyməsini basın.")
    elif lang == "uz":
        return (f"Kirittirgan ma'lumotlaringizni tekshiring:\n\n"
                f"Maydon: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Tashrif maqsadi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizning arizalaringiz:\n" +
                get_orders_in_list(data['orders']) +
                f"Ma'lumotlarni o'zgartirish uchun <b>{edit_data_button_text(lang)}</b> tugmasini bosing.\n"
                f"Arizalarni tekshiruvga yuborish uchun <b>{send_to_review_button_text(lang)}</b> tugmasini bosing.")
    elif lang == "tg":
        return (f"Маълумотҳои воридкардаи худро санҷед:\n\n"
                f"Майдон: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мақсади боздид: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Аризаҳои шумо:\n" +
                get_orders_in_list(data['orders']) +
                f"Барои тағйири маълумотҳо тугмаи <b>{edit_data_button_text(lang)}</b>-ро пахш кунед.\n"
                f"Барои ирсоли аризаҳо барои санҷиш тугмаи <b>{send_to_review_button_text(lang)}</b>-ро пахш кунед.")


def send_to_review_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Отправить на проверку"
        case "en":
            return "Submit for review"
        case "kz":
            return "Қарауға жіберу"
        case "by":
            return "Адправіць на праверку"
        case "az":
            return "Nəzərdən keçirilməsi üçün təqdim edin"
        case "uz":
            return "Tekshirish uchun yuboring"
        case "tg":
            return "Барои баррасӣ пешниҳод кунед"


def submit_orders_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Подтвердить"
        case "en":
            return "Confirm"
        case "kz":
            return "Растау"
        case "by":
            return "Пацвердзіць"
        case "az":
            return "Təsdiq edin"
        case "uz":
            return "Tasdiqlang"
        case "tg":
            return "Тасдиқ кунед"


def edit_data_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Изменить данные"
        case "en":
            return "Edit data"
        case "kz":
            return "Мәліметтерді өзгерту"
        case "by":
            return "Змяніць дадзеныя"
        case "az":
            return "Məlumatları dəyişdir"
        case "uz":
            return "Ma'lumotlarni o'zgartirish"
        case "tg":
            return "Маълумотҳоро тағйир додан"


def get_edit_site_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить площадку"
    elif lang == "en":
        return "Edit site"
    elif lang == "kz":
        return "Алаңды өзгерту"
    elif lang == "by":
        return "Змяніць пляцоўку"
    elif lang == "az":
        return "Meydançanı dəyişdir"
    elif lang == "uz":
        return "Maydonni o'zgartirish"
    elif lang == "tg":
        return "Майдонро тағйир додан"


def get_edit_purpose_of_visit_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить цель визита"
    elif lang == "en":
        return "Edit purpose of visit"
    elif lang == "kz":
        return "Келу мақсатын өзгерту"
    elif lang == "by":
        return "Змяніць мэту візіту"
    elif lang == "az":
        return "Ziyarət məqsədini dəyişdir"
    elif lang == "uz":
        return "Tashrif maqsadini o'zgartirish"
    elif lang == "tg":
        return "Мақсади бозидро тағйир додан"


def get_edit_applications_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить заявки"
    elif lang == "en":
        return "Edit applications"
    elif lang == "kz":
        return "Өтініштерді өзгерту"
    elif lang == "by":
        return "Змяніць заяўкі"
    elif lang == "az":
        return "Müraciətləri dəyişdir"
    elif lang == "uz":
        return "Arizalarni o'zgartirish"
    elif lang == "tg":
        return "Аризаҳоро тағйир додан"


def get_edit_application_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить заявку"
    elif lang == "en":
        return "Edit application"
    elif lang == "kz":
        return "Өтінішті өзгерту"
    elif lang == "by":
        return "Змяніць заяўку"
    elif lang == "az":
        return "Müraciəti dəyişdir"
    elif lang == "uz":
        return "Arizani o'zgartirish"
    elif lang == "tg":
        return "Аризаро тағйир додан"


def get_add_application_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Добавить заявку"
    elif lang == "en":
        return "Add application"
    elif lang == "kz":
        return "Өтініш қосу"
    elif lang == "by":
        return "Дадаць заяўку"
    elif lang == "az":
        return "Müraciət əlavə et"
    elif lang == "uz":
        return "Ariza qo'shish"
    elif lang == "tg":
        return "Ариза илова кардан"


def get_delete_application_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Удалить заявку"
    elif lang == "en":
        return "Delete application"
    elif lang == "kz":
        return "Өтінішті жою"
    elif lang == "by":
        return "Выдаліць заяўку"
    elif lang == "az":
        return "Müraciəti sil"
    elif lang == "uz":
        return "Arizani o'chirish"
    elif lang == "tg":
        return "Аризаро нест кардан"


def get_enter_application_number_text(lang: str) -> str:
    if lang == "ru":
        return "Введите, пожалуйста, номер заявки, которую вы хотите изменить:"
    elif lang == "en":
        return "Please enter the application number you want to edit:"
    elif lang == "kz":
        return "Өзгерту үшін қажетті өтініштің нөмірін енгізіңіз:"
    elif lang == "by":
        return "Калі ласка, увядзіце нумар заяўкі, якую вы хочаце змяніць:"
    elif lang == "az":
        return "Dəyişdirmək istədiyiniz müraciətin nömrəsini daxil edin:"
    elif lang == "uz":
        return "O'zgartirmoqchi bo'lgan ariza raqamini kiriting:"
    elif lang == "tg":
        return "Лутфан рақами аризаро, ки шумо мехоҳед тағйир диҳед, ворид кунед:"


def get_enter_application_number_to_delete_text(lang: str) -> str:
    if lang == "ru":
        return "Введите, пожалуйста, номер заявки, которую вы хотите удалить:"
    elif lang == "en":
        return "Please enter the application number you want to delete:"
    elif lang == "kz":
        return "Жою үшін қажетті өтініштің нөмірін енгізіңіз:"
    elif lang == "by":
        return "Калі ласка, увядзіце нумар заяўкі, якую вы хочаце выдаліць:"
    elif lang == "az":
        return "Silmək istədiyiniz müraciətin nömrəsini:"


def get_enter_application_number_to_add_text(lang: str) -> str:
    if lang == "ru":
        return "Введите, пожалуйста, номер заявки, которую вы хотите добавить."
    elif lang == "en":
        return "Please enter the application number you want to add."
    elif lang == "kz":
        return "Қосқыңыз келетін өтініштің нөмірін енгізіңіз."
    elif lang == "by":
        return "Калі ласка, увядзіце нумар заяўкі, якую вы хочаце дадаць."
    elif lang == "az":
        return "Əlavə etmək istədiyiniz müraciətin nömrəsini daxil edin."
    elif lang == "uz":
        return "Qo'shmoqchi bo'lgan ariza raqamini kiriting."
    elif lang == "tg":
        return "Лутфан рақами аризаро, ки шумо мехоҳед илова кунед, ворид кунед."


def get_incorrect_order_text(lang: str) -> str:
    if lang == "ru":
        return "Вы ввели некорректный номер заявки. Введите еще раз."
    elif lang == "en":
        return "You have entered an incorrect application number. Please enter it again."
    elif lang == "kz":
        return "Сіз қате қолданба нөмірін енгіздіңіз. Қайтадан енгізіңіз."
    elif lang == "by":
        return "Вы ўвялі некарэктны нумар заяўкі. Увядзіце яшчэ раз."
    elif lang == "az":
        return "Siz səhv ərizə nömrəsi daxil etdiniz. Yenidən daxil olun."
    elif lang == "uz":
        return "Siz ariza raqamini noto‘g‘ri kiritdingiz. Yana kiriting."
    elif lang == "tg":
        return "Шумо рақами аризаро нодуруст ворид кардед. Боз ворид кунед."


def get_order_error_text(lang: str) -> str:
    if lang == "ru":
        return "Не удалось пройти проверку заявок. Повторите попытку ещё раз."
    elif lang == "en":
        return "Failed to verify the applications. Please try again."
    elif lang == "kz":
        return "Қолданбаларды тексеру мүмкін болмады. Қайталап көріңіз."
    elif lang == "by":
        return "Не атрымалася праверыць заяўкі. Паўтарыце спробу."
    elif lang == "az":
        return "Tətbiqləri yoxlamaq mümkün olmadı. Bir daha cəhd edin."
    elif lang == "uz":
        return "Arizalarni tekshirib bo'lmadi. Yana urinib ko'ring."
    elif lang == "tg":
        return "Санҷиши барномаҳо анҷом нашуд. Лутфан дубора кӯшиш кунед."


def get_all_orders_deleted_text(lang: str) -> str:
    if lang == "ru":
        return "Вы удалили все заявки. Нужно ввести хотя бы одну.\nВведите, пожалуйста, номер заявки:"
    elif lang == "en":
        return "You have deleted all applications. You must enter at least one.\nPlease enter the application number:"
    elif lang == "kz":
        return "Сіз барлық қолданбаларды жойдыңыз. Сіз кем дегенде біреуін енгізуіңіз керек.\nӨтінім нөмірін енгізіңіз:"
    elif lang == "by":
        return "Вы выдалілі ўсе заяўкі. Трэба ўвесці хаця б адну.\nУвядзіце, калі ласка, нумар заяўкі:"
    elif lang == "az":
        return "Siz bütün proqramları sildiniz. Ən azı birini daxil etməlisiniz.\nLütfən, ərizə nömrənizi daxil edin:"
    elif lang == "uz":
        return "Siz barcha ilovalarni o'chirib tashladingiz. Kamida bittasini kiritishingiz kerak.\nIltimos, ariza raqamingizni kiriting:"
    elif lang == "tg":
        return "Шумо ҳамаи барномаҳоро нест кардед. Шумо бояд ақаллан якто ворид кунед.\nЛутфан рақами дархости худро ворид кунед:"


def get_no_match_text(lang: str) -> str:
    if lang == "ru":
        return "Введенной вами заявки нет в моих записях! Возвращаюсь назад."
    elif lang == "en":
        return "The request you entered is not in my records! Going back."
    elif lang == "kz":
        return "Сіз енгізген қолданба менің жазбамда жоқ! Мен қайтамын."
    elif lang == "by":
        return "Уведзенай вамі заяўкі няма ў маіх запісах! Вяртаюся назад."
    elif lang == "az":
        return "Daxil etdiyiniz proqram mənim qeydlərimdə yoxdur! Mən qayıdıram."
    elif lang == "uz":
        return "Siz kiritgan ilova mening yozuvlarimda yo'q! Men qaytib ketyapman."
    elif lang == "tg":
        return "Аризае, ки шумо ворид кардед, дар сабтҳои ман нест! Ман бармегардам."


def get_enter_new_order_number_text(lang: str) -> str:
    if lang == "ru":
        return "Введите, пожалуйста, новый номер заявки:"
    elif lang == "en":
        return "Please enter the new application number:"
    elif lang == "kz":
        return "Жаңа өтінім нөмірін енгізіңіз:"
    elif lang == "by":
        return "Калі ласка, увядзіце новы нумар заяўкі:"
    elif lang == "az":
        return "Zəhmət olmasa yeni ərizə nömrəsi daxil edin:"
    elif lang == "uz":
        return "Iltimos, yangi ariza raqamini kiriting:"
    elif lang == "tg":
        return "Лутфан рақами нави аризаро ворид кунед:"


def show_contact_point(text: str, lang: str) -> str:
    if text == "М19":
        return get_first_point_kb_text(lang)
    elif text == "М70":
        return get_second_point_kb_text(lang)
    elif text == "Уткина Заводь":
        return get_third_point_kb_text(lang)
    elif text == "Открытая площадка":
        return get_fourth_point_kb_text(lang)
    elif text == "К8":
        return get_fifth_point_kb_text(lang)
    else:
        return "Error"


def show_job_type(text: str, lang: str) -> str:
    if text == "Прием":
        return get_job_first_kb_text(lang)
    elif text == "Отгрузка":
        return get_job_second_kb_text(lang)
    else:
        return "Error"


def get_lang_yes(lang: str) -> str:
    if lang == "ru":
        return "Да"
    elif lang == "en":
        return "Yes"
    elif lang == "kz":
        return "Иә"
    elif lang == "by":
        return "Так"
    elif lang == "az":
        return "Bəli"
    elif lang == "uz":
        return "Ha"
    elif lang == "tg":
        return "Ҳа"


def get_lang_no(lang: str) -> str:
    if lang == "ru":
        return "Нет"
    elif lang == "en":
        return "No"
    elif lang == "kz":
        return "Жоқ"
    elif lang == "by":
        return "Не"
    elif lang == "az":
        return "Xeyr"
    elif lang == "uz":
        return "Yo'q"
    elif lang == "tg":
        return "Не"


def get_lang_partner(lang: str) -> str:
    if lang == "ru":
        return "Контрагент"
    elif lang == "en":
        return "Partner"
    elif lang == "kz":
        return "Серіктес"
    elif lang == "by":
        return "Партнёр"
    elif lang == "az":
        return "Tərəfdaş"
    elif lang == "uz":
        return "Hamkor"
    elif lang == "tg":
        return "Шарик"


def get_reset_partner_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Сбросить контрагента"
    elif lang == "en":
        return "Reset partner"
    elif lang == "kz":
        return "Серіктесті қалпына келтіру"
    elif lang == "by":
        return "Перазагрузіць партнёра"
    elif lang == "az":
        return "Tərəfdaşınızı yenidən başladın"
    elif lang == "uz":
        return "Hamkorni tiklash"
    elif lang == "tg":
        return "Шарики худро бозоғоз намоед"


def get_orders_with_status_text(lang: str, data: dict) -> str:
    if lang == "ru":
        return (f"Проверьте свои данные чтобы пройти проверку:\n\n"
                f"Площадка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Цель визита: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Ваши заявки:\n" +
                get_orders_with_status(data['orders']) +
                f"Для изменения данных нажмите кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для отправки заявок на проверку нажмите <b>{send_to_review_button_text(lang)}</b>.")
    elif lang == "en":
        return (f"Please check the information you have entered:\n\n"
                f"Site: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Purpose of visit: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Your applications:\n" +
                get_orders_with_status(data['orders']) +
                f"To modify the data, press the <b>{edit_data_button_text(lang)}</b> button.\n"
                f"To submit the applications for verification, press <b>{send_to_review_button_text(lang)}</b>")
    elif lang == "kz":
        return (f"Кіргізген деректеріңізді тексеріңіз:\n\n"
                f"Алаң: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Келу мақсаты: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Сіздің өтініштеріңіз:\n" +
                get_orders_with_status(data['orders']) +
                f"Деректерді өзгерту үшін <b>{edit_data_button_text(lang)}</b> түймесін басыңыз.\n"
                f"Өтініштерді тексеруге жіберу үшін <b>{send_to_review_button_text(lang)}</b> түймесін басыңыз.")
    elif lang == "by":
        return (f"Праверце ўведзеныя вамі дадзеныя:\n\n"
                f"Пляцоўка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мэта візіту: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Вашы заяўкі:\n" +
                get_orders_with_status(data['orders']) +
                f"Для змянення дадзеных націсніце кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для адпраўкі заяў на праверку націсніце <b>{send_to_review_button_text(lang)}</b>")
    elif lang == "az":
        return (f"Daxil etdiyiniz məlumatları yoxlayın:\n\n"
                f"Meydança: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Ziyarət məqsədi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizin müraciətləriniz:\n" +
                get_orders_with_status(data['orders']) +
                f"Məlumatları dəyişdirmək üçün <b>{edit_data_button_text(lang)}</b> düyməsini basın.\n"
                f"Müraciətləri yoxlamağa göndərmək üçün <b>{send_to_review_button_text(lang)}</b> düyməsini basın.")
    elif lang == "uz":
        return (f"Kirittirgan ma'lumotlaringizni tekshiring:\n\n"
                f"Maydon: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Tashrif maqsadi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizning arizalaringiz:\n" +
                get_orders_with_status(data['orders']) +
                f"Ma'lumotlarni o'zgartirish uchun <b>{edit_data_button_text(lang)}</b> tugmasini bosing.\n"
                f"Arizalarni tekshiruvga yuborish uchun <b>{send_to_review_button_text(lang)}</b> tugmasini bosing.")
    elif lang == "tg":
        return (f"Маълумотҳои воридкардаи худро санҷед:\n\n"
                f"Майдон: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мақсади боздид: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Аризаҳои шумо:\n" +
                get_orders_with_status(data['orders']) +
                f"Барои тағйири маълумотҳо тугмаи <b>{edit_data_button_text(lang)}</b>-ро пахш кунед.\n"
                f"Барои ирсоли аризаҳо барои санҷиш тугмаи <b>{send_to_review_button_text(lang)}</b>-ро пахш кунед.")


def get_partners_text(lang: str, data: dict) -> str:
    if lang == "ru":
        return (f"Проверьте свои данные чтобы пройти проверку:\n\n"
                f"Площадка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Цель визита: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Ваши заявки:\n" +
                get_orders_in_list(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Для изменения данных нажмите кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для отправки заявок на подтверждение нажмите <b>{send_to_review_button_text(lang)}</b>.")
    elif lang == "en":
        return (f"Please check the information you have entered:\n\n"
                f"Site: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Purpose of visit: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Your applications:\n" +
                get_orders_in_list(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"To modify the data, press the <b>{edit_data_button_text(lang)}</b> button.\n"
                f"To submit the applications for verification, press <b>{send_to_review_button_text(lang)}</b>.")
    elif lang == "kz":
        return (f"Кіргізген деректеріңізді тексеріңіз:\n\n"
                f"Алаң: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Келу мақсаты: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Сіздің өтініштеріңіз:\n" +
                get_orders_in_list(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Деректерді өзгерту үшін <b>{edit_data_button_text(lang)}</b> түймесін басыңыз.\n"
                f"Өтініштерді тексеруге жіберу үшін <b>{send_to_review_button_text(lang)}</b> түймесін басыңыз.")
    elif lang == "by":
        return (f"Праверце ўведзеныя вамі дадзеныя:\n\n"
                f"Пляцоўка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мэта візіту: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Вашы заяўкі:\n" +
                get_orders_in_list(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Для змянення дадзеных націсніце кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для адпраўкі заяў на праверку націсніце <b>{send_to_review_button_text(lang)}</b>")
    elif lang == "az":
        return (f"Daxil etdiyiniz məlumatları yoxlayın:\n\n"
                f"Meydança: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Ziyarət məqsədi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizin müraciətləriniz:\n" +
                get_orders_in_list(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Məlumatları dəyişdirmək üçün <b>{edit_data_button_text(lang)}</b> düyməsini basın.\n"
                f"Müraciətləri yoxlamağa göndərmək üçün <b>{send_to_review_button_text(lang)}</b> düyməsini basın.")
    elif lang == "uz":
        return (f"Kirittirgan ma'lumotlaringizni tekshiring:\n\n"
                f"Maydon: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Tashrif maqsadi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizning arizalaringiz:\n" +
                get_orders_in_list(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Ma'lumotlarni o'zgartirish uchun <b>{edit_data_button_text(lang)}</b> tugmasini bosing.\n"
                f"Arizalarni tekshiruvga yuborish uchun <b>{send_to_review_button_text(lang)}</b> tugmasini bosing.")
    elif lang == "tg":
        return (f"Маълумотҳои воридкардаи худро санҷед:\n\n"
                f"Майдон: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мақсади боздид: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Аризаҳои шумо:\n" +
                get_orders_with_green_icon(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Барои тағйири маълумотҳо тугмаи <b>{edit_data_button_text(lang)}</b>-ро пахш кунед.\n"
                f"Барои ирсоли аризаҳо барои санҷиш тугмаи <b>{send_to_review_button_text(lang)}</b>-ро пахш кунед.")


def get_full_info_text(lang: str, data: dict) -> str:
    if lang == "ru":
        return (f"Проверьте свои данные чтобы пройти проверку:\n\n"
                f"Площадка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Цель визита: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Ваши заявки:\n" +
                get_orders_with_status(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Для изменения данных нажмите кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для отправки заявок на подтверждение нажмите <b>{submit_orders_button_text(lang)}</b>.")
    elif lang == "en":
        return (f"Please check the information you have entered:\n\n"
                f"Site: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Purpose of visit: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Your applications:\n" +
                get_orders_with_status(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"To modify the data, press the <b>{edit_data_button_text(lang)}</b> button.\n"
                f"To submit the applications for verification, press <b>{submit_orders_button_text(lang)}</b>.")
    elif lang == "kz":
        return (f"Кіргізген деректеріңізді тексеріңіз:\n\n"
                f"Алаң: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Келу мақсаты: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Сіздің өтініштеріңіз:\n" +
                get_orders_with_status(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Деректерді өзгерту үшін <b>{edit_data_button_text(lang)}</b> түймесін басыңыз.\n"
                f"Өтініштерді тексеруге жіберу үшін <b>{submit_orders_button_text(lang)}</b> түймесін басыңыз.")
    elif lang == "by":
        return (f"Праверце ўведзеныя вамі дадзеныя:\n\n"
                f"Пляцоўка: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мэта візіту: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Вашы заяўкі:\n" +
                get_orders_with_status(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Для змянення дадзеных націсніце кнопку <b>{edit_data_button_text(lang)}</b>.\n"
                f"Для адпраўкі заяў на праверку націсніце <b>{submit_orders_button_text(lang)}</b>")
    elif lang == "az":
        return (f"Daxil etdiyiniz məlumatları yoxlayın:\n\n"
                f"Meydança: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Ziyarət məqsədi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizin müraciətləriniz:\n" +
                get_orders_with_status(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Məlumatları dəyişdirmək üçün <b>{edit_data_button_text(lang)}</b> düyməsini basın.\n"
                f"Müraciətləri yoxlamağa göndərmək üçün <b>{submit_orders_button_text(lang)}</b> düyməsini basın.")
    elif lang == "uz":
        return (f"Kirittirgan ma'lumotlaringizni tekshiring:\n\n"
                f"Maydon: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Tashrif maqsadi: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Sizning arizalaringiz:\n" +
                get_orders_with_status(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Ma'lumotlarni o'zgartirish uchun <b>{edit_data_button_text(lang)}</b> tugmasini bosing.\n"
                f"Arizalarni tekshiruvga yuborish uchun <b>{submit_orders_button_text(lang)}</b> tugmasini bosing.")
    elif lang == "tg":
        return (f"Маълумотҳои воридкардаи худро санҷед:\n\n"
                f"Майдон: <b>{show_contact_point(data['contact_point'], lang)}</b>\n"
                f"Мақсади боздид: <b>{show_job_type(data['job_type'], lang)}</b>\n"
                f"Аризаҳои шумо:\n" +
                get_orders_with_status(data['orders']) +
                f"{get_lang_partner(lang)}: <b>{data['partner']}</b>\n"
                f"Барои тағйири маълумотҳо тугмаи <b>{edit_data_button_text(lang)}</b>-ро пахш кунед.\n"
                f"Барои ирсоли аризаҳо барои санҷиш тугмаи <b>{submit_orders_button_text(lang)}</b>-ро пахш кунед.")


def ask_partner_text(lang: str) -> str:
    if lang == "ru":
        return "Выберите вашего контрагента"
    elif lang == "en":
        return "Select your business partner"
    elif lang == "kz":
        return "Контрагентті таңдаңыз"
    elif lang == "by":
        return "Выберыце ваш контрагент"
    elif lang == "az":
        return "İş ortağınızı seçin"
    elif lang == "uz":
        return "Biznes sherigingizni tanlang"
    elif lang == "tg":
        return "Шарики тиҷорати худро интихоб кунед"
