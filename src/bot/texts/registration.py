from src.services.settings import settings


def get_data_list_text(lang: str) -> str:
    if lang == "ru":
        return "Для того чтобы зарегистрироваться в системе нужно ввести свои данные:"
    elif lang == "en":
        return "In order to register in the system, you need to enter your data:>"
    elif lang == "kz":
        return "Жүйеге тіркелу үшін өз деректеріңізді енгізу қажет:"
    elif lang == "by":
        return "Для таго каб зарэгістравацца ў сістэме трэба ўвесці свае дадзеныя:"
    elif lang == "az":
        return "Sistemdə qeydiyyatdan keçmək üçün məlumatlarınızı daxil etməlisiniz:"
    elif lang == "uz":
        return "Tizimda ro'yxatdan o'tish uchun siz ma'lumotlaringizni kiritishingiz kerak:"
    elif lang == "tg":
        return "Барои дохил шудан ба система, шумо бояд маълумоти худро ворид кунед:"


def get_enter_name_text(lang: str) -> str:
    if lang == "ru":
        return " Введите ваше имя"
    elif lang == "en":
        return " Enter your name.\n\nInput format: Ivan (russian letters)"
    elif lang == "kz":
        return " Атыңызды енгізіңіз.\n\nЕнгізу форматы: Иван (орыс әріптерімен)."
    elif lang == "by":
        return " Увядзіце ваша імя\n\nФармат уводу: Иван (рускімі літарамі)."
    elif lang == "az":
        return " Adınızı daxil edin.\n\nGiriş formatı: Иван (rus hərfləri ilə)."
    elif lang == "uz":
        return "Ismingizni kiriting.\n\nKirish formati: Иван (ruscha harflar bilan)."
    elif lang == "tg":
        return "Номи худро ворид кунед.\n\nФормати вуруд: Иван (бо ҳарфҳои русӣ)."


def get_incorrect_name_text(lang: str) -> str:
    if lang == "ru":
        return "Вы ввели некорректное имя.\nПожалуйста, введите имя в формате: Иван."
    elif lang == "en":
        return "You entered an incorrect name.\nPlease enter the name in the format: Ivan."
    elif lang == "kz":
        return "Сіз қате атау енгіздіңіз.\nАтын форматта енгізіңіз: Иван."
    elif lang == "by":
        return "Вы ўвялі няправільнае імя.\nКалі ласка, увядзіце імя ў фармаце: Иван."
    elif lang == "az":
        return "Səhv bir ad daxil etdiniz.\nZəhmət olmasa adı formatda daxil edin: Иван."
    elif lang == "uz":
        return "Siz noto'g'ri ism kiritdingiz.\nIltimos, ismni formatga kiriting: Иван."
    elif lang == "tg":
        return "Шумо номи нодурустро ворид кардед.\nЛутфан номро дар формат ворид кунед: Иван."


def get_enter_surname_text(lang: str) -> str:
    if lang == "ru":
        return "Введите вашу фамилию"
    elif lang == "en":
        return "Enter your last name.\n\nInput format: Ivanov.\nFor a double surname: Ivanov-Smirnov."
    elif lang == "kz":
        return "Фамилияңызды енгізіңіз.\n\nЕнгізу форматы: Иванов.\nҚос Тегі үшін: Иванов-Смирнов."
    elif lang == "by":
        return "Увядзіце ваша прозвішча.\n\nФармат уводу: Иванов.\nДля двайны прозвішчы: Иванов-Смирнов"
    elif lang == "az":
        return "Soyadınızı daxil edin.\n\nGiriş formatı: Иванов.\nİkiqat soyad üçün: Иванов-Смирнов."
    elif lang == "uz":
        return "Familiyangizni kiriting.\n\nKirish formati: Иванов.\nIkkita familiya uchun: Иванов-Смирнов."
    elif lang == "tg":
        return "Насаби худро ворид кунед.\n\nФормати вуруд: Иванов.\nБарои насаби дугона: Иванов-Смирнов."


def get_incorrect_surname_text(lang: str) -> str:
    if lang == "ru":
        return "Вы ввели некорректно фамилию.\nПожалуйста, введите фамилию в формате: Иванов.\nДля двойной фамилии: Иванов-Смирнов."
    elif lang == "en":
        return "You entered the last name incorrectly.\nPlease enter your last name in the format: Ivanov.\nFor a double surname: Ivanov-Smirnov."
    elif lang == "kz":
        return "Сіз фамилияны қате енгіздіңіз.\nФамилияңызды форматта енгізіңіз: Иванов.\nҚос фамилия үшін: Иванов-Смирнов."
    elif lang == "by":
        return "Вы няправільна ўвялі прозвішча.\nКалі ласка, увядзіце ваша прозвішча ў фармаце: Иванов.\nДля двайны прозвішчы: Иванов-Смирнов."
    elif lang == "az":
        return "Soyadınızı səhv daxil etdiniz.\nZəhmət olmasa soyadınızı formatda daxil edin: Иванов.\nİkiqat soyad üçün: Иванов-Смирнов."
    elif lang == "uz":
        return "Siz familiyani noto'g'ri kiritdingiz.\nIltimos, familiyangizni quyidagi formatda kiriting: Иванов.\nIkki familiya uchun: Иванов-Смирнов."
    elif lang == "tg":
        return "Шумо насабро нодуруст ворид кардед.\nЛутфан насаби худро дар формат ворид кунед: Иванов.\nБарои насаби дугона: Иванов-Смирнов."


def get_enter_middle_name_text(lang: str) -> str:
    if lang == "ru":
        return "Введите ваше отчество"
    elif lang == "en":
        return "Enter your patronymic.\n\nInput format: Ivanovich."
    elif lang == "kz":
        return "Әкеңіздің атын енгізіңіз.\n\nЕнгізу форматы: Иванович."
    elif lang == "by":
        return "Увядзіце ваша імя па бацьку.\n\nФармат уводу: Иванович."
    elif lang == "az":
        return "Orta adınızı daxil edin.\n\nGiriş formatı: Иванович."
    elif lang == "uz":
        return "Otangizning ismini kiriting.\n\nKirish formati: Иванович."
    elif lang == "tg":
        return "Номи падари худро ворид кунед.\n\nФормати вуруд: Иванович."


def get_incorrect_middle_name_text(lang: str) -> str:
    if lang == "ru":
        return "Вы ввели некорректно отчество.\n\nПожалуйста, введите отчество в формате: Иванович"
    elif lang == "en":
        return "You entered the patronymic incorrectly.\n\nPlease enter the patronymic in the format: Ivanovich"
    elif lang == "kz":
        return "Сіз әкесінің атын дұрыс енгізбедіңіз.\n\nӘкесінің атын келесі форматта енгізіңіз: Иванович"
    elif lang == "by":
        return "Вы ўвялі некарэктна імя па бацьку.\n\nКалі ласка, увядзіце імя па бацьку ў фармаце: Иванович"
    elif lang == "az":
        return "Siz yanlış orta adı daxil.\n\nXahiş edirəm orta adınızı formatda daxil edin: Иванович"
    elif lang == "uz":
        return "Siz otasining ismini noto'g'ri kiritdingiz.\n\nIltimos, otasining ismini quyidagi formatda kiriting: Иванович"
    elif lang == "tg":
        return "Шумо номи падари нодурустро ворид кардед.\n\nЛутфан номи падари худро дар формат ворид кунед: Иванович"


def skip_middle_name_kb_text(lang: str) -> str:
    if lang == "ru":
        return "У меня нет отчества"
    elif lang == "en":
        return "I don't have a Patronymic"
    elif lang == "kz":
        return "Менің әкем жоқ"
    elif lang == "by":
        return "У мяне няма імя па бацьку"
    elif lang == "az":
        return "Mənim ata adım yoxdur"
    elif lang == "uz":
        return "Mening otamning ismi yo'q"
    elif lang == "tg":
        return "Ман номи падар надорам"


def show_full_info(lang: str, data: dict) -> str:
    edit_button_text = edit_reg_data_kb_text(lang)
    register_button_text = apply_registration_kb_text(lang)

    match lang:
        case "ru":
            return (f"Вот вся введенная вами информация:\n\n"
                    f"Фамилия: <b>{data['surname']}</b>\n"
                    f"Имя: <b>{data['name']}</b>\n"
                    f"Отчество: <b>{data['middle_name']}</b>\n"
                    f"Номер телефона: <b>{data['number']}</b>\n"
                    f"Серия паспорта: <b>{data['licence_series']}</b>\n"
                    f"Номер паспорта: <b>{data['licence_number']}</b>\n\n"
                    f"Для изменения данных нажмите на <b>{edit_button_text}</b>.\n"
                    f"Для завершения регистрации нажмите <b>{register_button_text}</b>.")
        case "en":
            return (f"Here is all the information you entered:\n\n"
                    f"Last name: <b>{data['surname']}</b>\n"
                    f"First name: <b>{data['name']}</b>\n"
                    f"Patronymic: <b>{data['middle_name']}</b>\n"
                    f"Phone number: <b>{data['number']}</b>\n"
                    f"Passport series: <b>{data['licence_series']}</b>\n"
                    f"Passport number: <b>{data['licence_number']}</b>\n\n"
                    f"To change the data, click on <b>{edit_button_text}</b>.\n"
                    f"To complete the registration, click <b>{register_button_text}</b>.")
        case "kz":
            return (f"Міне, сіз енгізген барлық ақпарат:\n\n"
                    f"Тегі: <b>{data['surname']}</b>\n"
                    f"Аты: <b>{data['name']}</b>\n"
                    f"Әкесінің аты: <b>{data['middle_name']}</b>\n"
                    f"Телефон нөмірі: <b>{data['number']}</b>\n"
                    f"Паспортың сериясы: <b>{data['licence_series']}</b>\n"
                    f"Паспортың нөмірі: <b>{data['licence_number']}</b>\n\n"
                    f"Деректерді өзгерту үшін басыңыз <b>{edit_button_text}</b>.\n"
                    f"Тіркеуді аяқтау үшін басыңыз <b>{register_button_text}</b>.")
        case "by":
            return (f"Вось уся інфармацыя, якую вы ўвялі:\n\n"
                    f"Прозвішча: <b>{data['surname']}</b>\n"
                    f"Імя: <b>{data['name']}</b>\n"
                    f"Імя па бацьку: <b>{data['middle_name']}</b>\n"
                    f"Нумар тэлефона: <b>{data['number']}</b>\n"
                    f"Серыя паспарту: <b>{data['licence_series']}</b>\n"
                    f"Нумар паспарту: <b>{data['licence_number']}</b>\n\n"
                    f"Каб змяніць дадзеныя, націсніце <b>{edit_button_text}</b>.\n"
                    f"Каб завяршыць рэгістрацыю, націсніце <b>{register_button_text}</b>.")
        case "az":
            return (f"Budur daxil etdiyiniz bütün məlumatlar:\n\n"
                    f"Soyad: <b>{data['surname']}</b>\n"
                    f"Ad: <b>{data['name']}</b>\n"
                    f"Ata adı: <b>{data['middle_name']}</b>\n"
                    f"Telefon nömrəsi: <b>{data['number']}</b>\n"
                    f"Pasport seriyası: <b>{data['licence_series']}</b>\n"
                    f"Pasport nömrəsi: <b>{data['licence_number']}</b>\n\n"
                    f"Veriləri dəyişdirmək üçün basın <b>{edit_button_text}</b>.\n"
                    f"Qeydiyyatı başa çatdırmaq üçün basın <b>{register_button_text}</b>.")
        case "uz":
            return (f"Siz kiritgan barcha ma'lumotlar:\n\n"
                    f"Familiya: <b>{data['surname']}</b>\n"
                    f"Ism: <b>{data['name']}</b>\n"
                    f"Otasining ismi: <b>{data['middle_name']}</b>\n"
                    f"Telefon raqami: <b>{data['number']}</b>\n"
                    f"Pasport seriyasi: <b>{data['licence_series']}</b>\n"
                    f"Pasport raqami: <b>{data['licence_number']}</b>\n\n"
                    f"Ma'lumotlarni o'zgartirish uchun bosing <b>{edit_button_text}</b>.\n"
                    f"Ro'yxatdan o'tishni yakunlash uchun bosing <b>{register_button_text}</b>.")
        case "tg":
            return (f"Ин аст тамоми маълумоте, ки шумо ворид кардед:\n\n"
                    f"Насаб: <b>{data['surname']}</b>\n"
                    f"Ном: <b>{data['name']}</b>\n"
                    f"Номи падар: <b>{data['middle_name']}</b>\n"
                    f"Рақами телефон: <b>{data['number']}</b>\n"
                    f"Силсилаи паспорт: <b>{data['licence_series']}</b>\n"
                    f"Рақами паспорт: <b>{data['licence_number']}</b>\n\n"
                    f"Барои тағир додани маълумот, клик кунед <b>{edit_button_text}</b>.\n"
                    f"Барои ба итмом расонидани бақайдгирӣ, клик кунед <b>{register_button_text}</b>.")
        case _:
            return "Unsupported language."

def apply_registration_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Зарегистрироваться"
        case "en":
            return "Register"
        case "kz":
            return "Тіркелу"
        case "by":
            return "Зарэгістравацца"
        case "az":
            return "Qeydiyyatdan keçin"
        case "uz":
            return "Ro'yxatdan o'tish"
        case "tg":
            return "Ба қайд гирифтан"
        case _:
            return "Register"


def edit_reg_data_kb_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Изменить"
        case "en":
            return "Edit"
        case "kz":
            return "Өңдеу"
        case "by":
            return "Рэдагаваць"
        case "az":
            return "Redaktə edin"
        case "uz":
            return "Tahrirlash"
        case "tg":
            return "Таҳрир"
        case _:
            return "Edit"


def get_user_agree_text(lang: str) -> str:
    if lang == "ru":
        return (f"Перед тем, как зарегистрироваться в системе, прочитайте, пожалуйста, пользовательское сообщение.\n\n"
                f"{settings.bot['user_agree']}\n\n"
                f"Нажимая кнопку \"Ознакомлен\" вы соглашаетесь с пользовательским соглашением.")
    elif lang == "en":
        return (f"Before registering in the system, please read the user message.\n\n"
                f"{settings.bot['user_agree']}\n\n"
                f"By clicking the \"Accept\" button, you agree to the user agreement.")
    elif lang == "kz":
        return (f"Жүйеге тіркелмес бұрын, пайдаланушы хабарламасын оқыңыз.\n\n"
                f"{settings.bot['user_agree']}\n\n"
                f"\"Қабылданды\" түймесін басу арқылы сіз пайдаланушы келісімімен келісесіз.")
    elif lang == "by":
        return (f"Перад тым, як зарэгістравацца ў сістэме, прачытайце, калі ласка, карыстальніцкае паведамленне.\n\n"
                f"{settings.bot['user_agree']}\n\n"
                f"Націскаючы кнопку \"Азнаёмлены\" вы згаджаецеся з карыстацкай дамовай.")
    elif lang == "az":
        return (f"Sistemdə qeydiyyatdan keçməzdən əvvəl istifadəçi mesajını oxuyun.\n\n"
                f"{settings.bot['user_agree']}\n\n"
                f"\"Qəbul edildi\" düyməsini klikləməklə siz istifadəçi müqaviləsi ilə razılaşırsınız.")
    elif lang == "uz":
        return (f"Tizimda ro'yxatdan o'tishdan oldin foydalanuvchi xabarini o'qing.\n\n"
                f"{settings.bot['user_agree']}\n\n"
                f"\"Qabul qilingan\" tugmasini bosish orqali siz foydalanuvchi shartnomasiga rozilik bildirasiz.")
    elif lang == "tg":
        return (f"Пеш аз сабти ном дар система, лутфан паёми корбарро хонед.\n\n"
                f"{settings.bot['user_agree']}\n\n"
                f"Бо пахш кардани тугмаи \"Қабулшуда\" шумо ба шартномаи корбар розӣ мешавед.")


def get_incorrect_user_agree_text(lang: str) -> str:
    if lang == "ru":
        return "Пожалуйста, примите соглашение, нажав на кнопку выше ⬆️."
    elif lang == "en":
        return "Please accept the agreement by clicking the button above ⬆️."
    elif lang == "kz":
        return "Жоғарыдағы ⬆️ түймешігін басу арқылы келісімді қабылдаңыз."
    elif lang == "by":
        return "Калі ласка, прыміце пагадненне, націснуўшы на кнопку вышэй ⬆️."
    elif lang == "az":
        return "Zəhmət olmasa yuxarıdakı ⬆️ düyməsinə klikləməklə müqaviləni qəbul edin."
    elif lang == "uz":
        return "Iltimos, yuqoridagi tugmani bosish orqali shartnomani qabul qiling ⬆️."
    elif lang == "tg":
        return "Лутфан, бо пахш кардани тугмаи боло ⬆️ шартномаро қабул кунед."


def get_successful_registration_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Я записал ваши данные!\nВ дальнейшем вы можете быстро авторизоваться по вашему паспорту."
        case "en":
            return "I have written down your details!\nIn the future, you can quickly log in using your passport."
        case "kz":
            return "Мен сіздің мәліметтеріңізді жазып алдым!\nБолашақта паспорттың нөмірі арқылы жүйеге жылдам кіруге болады."
        case "by":
            return "Я запісаў вашы дадзеныя!\nУ далейшым вы можаце хутка аўтарызавацца па нумары вашага паспарту."
        case "az":
            return "Mən sizin təfərrüatlarınızı qeyd etmişəm!\nGələcəkdə siz pasportunuzun nömrəsi ilə tez daxil ola bilərsiniz."
        case "uz":
            return "Men sizning ma'lumotlaringizni yozib oldim!\nKelajakda siz pasportingiz raqamidan foydalanib tezda tizimga kirishingiz mumkin."
        case "tg":
            return "Ман тафсилоти шуморо сабт кардам!\nДар оянда шумо метавонед бо рақами паспорт худ зуд ворид шавед."
        case _:
            return "Unsupported language."


def get_unable_to_registration_text(lang: str) -> str:
    if lang == "ru":
        return "Не удалось зарегистрироваться, вернитесь в главное меню."
    elif lang == "en":
        return "Failed to register, return to main menu."
    elif lang == "kz":
        return "Тіркеу сәтсіз аяқталды, негізгі мәзірге оралыңыз."
    elif lang == "by":
        return "Немагчыма зарэгістравацца, вярніцеся ў галоўнае меню."
    elif lang == "az":
        return "Qeydiyyat uğursuz oldu, lütfən əsas menyuya qayıdın."
    elif lang == "uz":
        return "Ro'yxatdan o'tish amalga oshmadi, iltimos, asosiy menyuga qayting."
    elif lang == "tg":
        return "Бақайдгирӣ ноком шуд, лутфан ба менюи асосӣ баргардед."


def number_formats_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Формат ввода телефона: +7xxxxxxxxxx  (10 цифр)"
        case "en":
            return "Phone entry format: +7xxxxxxxxxx  (10 digits)"
        case "kz":
            return "Телефон енгізу пішімдері: +7xxxxxxxxxx  (10 сан)"
        case "by":
            return "Фармат ўводу тэлефона: +7xxxxxxxxxx  (10 лічбаў)"
        case "az":
            return "Telefon daxiletmə formatları: +7xxxxxxxxxx  (10 rəqəm)"
        case "uz":
            return "Telefon kiritish formatlari: +7xxxxxxxxxx  (10 ta raqam)"
        case "tg":
            return "Форматҳои вуруди телефон: +7xxxxxxxxxx  (10 рақам)"


def user_number_text(lang: str) -> str:
    if lang == "ru":
        return "Введите ваш номер телефона"
    elif lang == "en":
        return "Enter your phone number"
    elif lang == "kz":
        return "Телефон нөміріңізді енгізіңіз"
    elif lang == "by":
        return "Увядзіце ваш нумар тэлефона"
    elif lang == "az":
        return "Telefon nömrənizi daxil edin"
    elif lang == "uz":
        return "Telefon raqamingizni kiriting"
    elif lang == "tg":
        return "Рақами телефони худро ворид кунед"


def incorrect_user_number_text(lang: str) -> str:
    if lang == "ru":
        return "Вы ввели некорректный номер телефона.\n\n"
    elif lang == "en":
        return "You have entered an incorrect phone number.\n\n"
    elif lang == "kz":
        return "Сіз қате телефон нөмірін енгіздіңіз.\n\n"
    elif lang == "by":
        return "Вы ўвялі некарэктны нумар тэлефона.\n\n"
    elif lang == "az":
        return "Yanlış telefon nömrəsi daxil etmisiniz.\n\n"
    elif lang == "uz":
        return "Siz telefon raqamini notoʻgʻri kiritdingiz.\n\n"
    elif lang == "tg":
        return "Шумо рақами телефонро нодуруст ворид кардед.\n\n"


def get_user_number_text(lang: str) -> str:
    return user_number_text(lang)


def get_incorrect_user_number_text(lang: str) -> str:
    return incorrect_user_number_text(lang) + number_formats_text(lang)


def edit_name_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить имя"
    elif lang == "en":
        return "Edit name"
    elif lang == "kz":
        return "Тағир додани ном"
    elif lang == "by":
        return "Змяніць імя"
    elif lang == "az":
        return "Adı dəyişdirin"
    elif lang == "uz":
        return "Ismni o'zgartirish"
    elif lang == "tg":
        return "Тағир додани ном"


def edit_surname_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить фамилию"
    elif lang == "en":
        return "Edit last name"
    elif lang == "kz":
        return "Тегін өзгерту"
    elif lang == "by":
        return "Змяніць прозвішча"
    elif lang == "az":
        return "Soyadı dəyişdirin"
    elif lang == "uz":
        return "Familiyani tahrirlash"
    elif lang == "tg":
        return "Иваз кардани насаб"


def edit_middle_name_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить отчество"
    elif lang == "en":
        return "Edit patronymic"
    elif lang == "kz":
        return "Әкесінің атын өзгерту"
    elif lang == "by":
        return "Змяніць імя па бацьку"
    elif lang == "az":
        return "Orta adı dəyişdirin"
    elif lang == "uz":
        return "Otasining ismini tahrirlash"
    elif lang == "tg":
        return "Тағйири номи падар"


def edit_number_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить номер телефона"
    elif lang == "en":
        return "Edit phone number"
    elif lang == "kz":
        return "Телефон нөмірін өңдеу"
    elif lang == "by":
        return "Змяніць нумар тэлефона"
    elif lang == "az":
        return "Telefon nömrəsini dəyişdirin"
    elif lang == "uz":
        return "Telefon raqamini tahrirlash"
    elif lang == "tg":
        return "Рақами телефонро иваз кунед"


def get_edit_licence_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Изменить удостоверение личности"
    elif lang == "en":
        return "Edit driver licence"
    elif lang == "kz":
        return "Жүргізуші куәлігін өңдеу"
    elif lang == "by":
        return "Рэдагаваць правы кіроўцы"
    elif lang == "az":
        return "Sürücü lisenziyasını redaktə edin"
    elif lang == "uz":
        return "Haydovchilik guvohnomasini tahrirlash"
    elif lang == "tg":
        return "Таҳрири шаҳодатномаи ронандагӣ"


def accept_user_agree_kb_text(lang: str) -> str:
    if lang == "ru":
        return "Ознакомлен"
    elif lang == "en":
        return "Accept"
    elif lang == "kz":
        return "Танысқан"
    elif lang == "by":
        return "Азнаёмлены"
    elif lang == "az":
        return "Tanış"
    elif lang == "uz":
        return "Tanishgan"
    elif lang == "tg":
        return "Шинос шуд"


def get_user_already_reg_text(lang: str) -> str:
    if lang == "ru":
        return "Такой пользователь уже зарегистрирован! Пожалуйста, обратитесь к диспетчеру."
    elif lang == "en":
        return "Such a user is already registered! Please contact the dispatcher."
    elif lang == "kz":
        return "Мұндай пайдаланушы тіркелген! Диспетчерге хабарласыңыз."
    elif lang == "by":
        return "Такі карыстальнік ужо зарэгістраваны! Калі ласка, звярніцеся да дыспетчару."
    elif lang == "az":
        return "Belə bir istifadəçi artıq qeydiyyatdan keçib! Zəhmət olmasa dispetçerə müraciət edin."
    elif lang == "uz":
        return "Bunday foydalanuvchi allaqachon ro'yxatdan o'tgan! Iltimos, dispetcherga murojaat qiling."
    elif lang == "tg":
        return "Чунин корбар аллакай ба қайд гирифта шудааст! Лутфан ба диспетчер муроҷиат кунед."
