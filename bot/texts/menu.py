def choose_lang_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Выберите язык.\nВаш язык <b>Русский</b>?"
        case "en":
            return "Choose language.\nYour language is <b>English</b>?"
        case "kz":
            return "Тілді таңдаңыз.\nСіздің тіліңіз <b>Қазақша</b>?"
        case "by":
            return "Выберыце мову.\nВаша мова <b>Беларуская</b>?"
        case "az":
            return "Dil seçin.\nSizin diliniz <b>Azərbaycan</b> dilidir?"
        case "uz":
            return "Tilni tanlang.\nSizning tilingiz <b>O'zbekmi</b>?"
        case "tg":
            return "Забонро интихоб кунед.\nЗабони Шумо <b>Тоҷикӣ</b> аст?"


def selected_lang_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Установлен язык <b>Русский</b>"
        case "en":
            return "Language set to <b>English</b>"
        case "kz":
            return "Тіліні қою <b>Қазақ тілі</b>"
        case "by":
            return "Выбрана мова <b>Беларуская</b>"
        case "az":
            return "Dil seçilmiş <b>Azərbaycan dili</b>"
        case "uz":
            return "Tilni tanlash <b>O'zbek tili</b>"
        case "tg":
            return "Забонро танланад <b>Тоҷикӣ</b>"


def lang_button_text(lang: str) -> str:
    match lang:
        case "ru":
            return "Русский"
        case "en":
            return "English"
        case "kz":
            return "Қазақша"
        case "by":
            return "Беларусь"
        case "az":
            return "Azərbaycan"
        case "uz":
            return "O'zbek tili"
        case "tg":
            return "Тоҷикӣ"


def stand_menu_text(lang: str) -> str:
    return greeting_text(lang) + "\n" + commands_text(lang)


def greeting_text(lang: str) -> str:
    match lang:
        case "ru":
            return ("Добрый день, пользователь!\n"
                    "Это программа по быстрой активации заявок.")
        case "en":
            return ("Hello, user!\n"
                    "This is a quick application activation program.")
        case "kz":
            return ("Сәлеметсіз бе, қолданушы!\n"
                    "Бұл қолданбаны жылдам белсендіру бағдарламасы.")
        case "by":
            return ("Добры дзень, карыстальнік!\n"
                    "Гэта праграма для хуткай актывацыі прыкладання.")
        case "az":
            return ("Salam İstifadəçi!\n"
                    "Bu proqramı tez aktivləşdirmək üçün bir proqramdır.")
        case "uz":
            return ("Salom, foydalanuvchi!\n"
                    "Bu tezkor dasturni faollashtirish dasturi.")
        case "tg":
            return ("Салом корбар!\n"
                    "Ин барнома барои зуд фаъол кардани барнома аст.")


def commands_text(lang: str) -> str:
    match lang:
        case "ru":
            return ("Для вывода инструкции по использованию чат-бота нажмите /help.\n"
                    "Для ознакомления с <b>пользовательским соглашением</b> нажмите /user_agree.\n"
                    "Для <b>смены языка</b> нажмите /change_lang\n\n"
                    "Пожалуйста, укажите, у вас уже есть <b>6-ти значный код</b> для активации заявки?")
        case "en":
            return ("For detailed information about possible commands press /help.\n"
                    "To read the <b>user agreement</b> press /user_agree.\n"
                    "To <b>change the language</b> press /change_lang.\n\n"
                    "Please indicate if you already have a <b>6-digit code</b> to activate your application?")
        case "kz":
            return ("Ықтимал пәрмендер туралы толық ақпарат алу үшін /help түймесін басыңыз.\n"
                    "Пайдаланушы келісімін оқу үшін /user_agree түймесін басыңыз.\n"
                    "Тілді өзгерту үшін /change_lang пернесін басыңыз\n\n"
                    "Қолданбаны белсендіру үшін сізде <b>6 санды код</b> бар-жоғын көрсетіңіз?")
        case "by":
            return ("Для атрымання падрабязнай інфармацыі аб магчымых камандах націсніце /help.\n"
                    "Для азнаямлення з карыстацкім пагадненнем націсніце /user_agree.\n"
                    "Для змены мовы Націсніце /change_lang\n\n"
                    "Калі ласка, укажыце, у вас ужо ёсць <b>6-ці значны код</b> для актывацыі заяўкі?")
        case "az":
            return ("Mümkün əmrlər haqqında ətraflı məlumat üçün /help düyməsini basın.\n"
                    "İstifadəçi müqaviləsi ilə tanış olmaq üçün /user_agree düyməsini basın.\n"
                    "Dili dəyişdirmək üçün /change_lang düyməsini basın\n\n"
                    "Tətbiqinizi aktivləşdirmək üçün artıq <b>6 rəqəmli kodun</b> olub olmadığını göstərin?")
        case "uz":
            return ("Iloji buyruqlar matbuot haqida batafsil ma'lumot olish uchun /help.\n"
                    "Foydalanuvchi shartnomasi bosing o'qish uchun /user_agree.\n"
                    "Tilni o'zgartirish uchun /change_lang tugmasini bosing\n\n"
                    "Iltimos, ilovangizni faollashtirish uchun sizda <b>6 xonali kod</b> bor-yo‘qligini ko‘rsating?")
        case "tg":
            return ("Барои тафсилот дар бораи фармонҳои имконпазир, клик кунед /help.\n"
                    "Барои шиносоӣ бо созишномаи корбар /user_agree пахш кунед.\n"
                    "Барои тағир додани забон, пахш кунед /change_lang\n\n"
                    "Лутфан нишон диҳед, ки оё шумо аллакай <b>рамзи 6-рақама</b> "
                    "доред, то барномаи худро фаъол созед?")


def user_menu_text(lang: str) -> str:
    match lang:
        case "ru":
            return ("Добрый день, пользователь!\n"
                    "Это программа по быстрой активации заявок.\n"
                    "Для вывода инструкции по использованию чат-бота нажмите /help..\n"
                    "Для ознакомления с <b>пользовательским соглашением</b> нажмите /user_agree.\n"
                    "Для <b>смены языка</b> нажмите /change_lang.")
        case "en":
            return ("Hello, user!\n"
                    "This is a quick application activation program.\n"
                    "For detailed information about possible commands press /help.\n"
                    "To read the <b>user agreement</b> press /user_agree.\n"
                    "To <b>change the language</b> press /change_lang.")
        case "kz":
            return ("Сәлеметсіз бе, қолданушы!\n"
                    "Бұл қолданбаны жылдам белсендіру бағдарламасы.\n"
                    "Ықтимал пәрмендер туралы толық ақпарат алу үшін /help түймесін басыңыз.\n"
                    "Пайдаланушы келісімін оқу үшін /user_agree түймесін басыңыз.\n"
                    "Тілді өзгерту үшін /change_lang пернесін басыңыз.")
        case "by":
            return ("Добры дзень, карыстальнік!\n"
                    "Гэта праграма для хуткай актывацыі прыкладання.\n"
                    "Для атрымання падрабязнай інфармацыі аб магчымых камандах націсніце /help.\n"
                    "Для азнаямлення з карыстацкім пагадненнем націсніце /user_agree.\n"
                    "Для змены мовы Націсніце /change_lang.")
        case "az":
            return ("Salam İstifadəçi!\n"
                    "Bu proqramı tez aktivləşdirmək üçün bir proqramdır.\n"
                    "Mümkün əmrlər haqqında ətraflı məlumat üçün /help düyməsini basın.\n"
                    "İstifadəçi müqaviləsi ilə tanış olmaq üçün /user_agree düyməsini basın.\n"
                    "Dili dəyişdirmək üçün /change_lang düyməsini basın.")
        case "uz":
            return ("Salom, foydalanuvchi!\n"
                    "Bu tezkor dasturni faollashtirish dasturi.\n"
                    "Iloji buyruqlar matbuot haqida batafsil ma'lumot olish uchun /help.\n"
                    "Foydalanuvchi shartnomasi bosing o'qish uchun /user_agree.\n"
                    "Tilni o'zgartirish uchun /change_lang tugmasini bosing.")
        case "tg":
            return ("Салом корбар!\n"
                    "Ин барнома барои зуд фаъол кардани барнома аст.\n"
                    "Барои тафсилот дар бораи фармонҳои имконпазир, клик кунед /help.\n"
                    "Барои шиносоӣ бо созишномаи корбар /user_agree пахш кунед.\n"
                    "Барои тағир додани забон, пахш кунед /change_lang.")


def help_text(lang: str) -> str:
    match lang:
        case "ru":
            return """Чат-бот предназначен для удобной регистрации водителей при приемке/отгрузке груза. Использование возможно как с личного смартфона, так и на стойке в диспетчерской.

Шаги использования:
1. Запуск бота
Отправьте команду /start в Telegram.
Выберите язык общения.

2. Регистрация. Если вы впервые пользуетесь ботом:
На стойке выберите опцию "Нет QR-кода".
Введите номер ВУ, затем Авторизоваться. После введите личные данные: ФИО, номер телефона.
Проверьте введенные данные и подтвердите их.

3. Авторизация. Если вы уже регистрировались:
Введите номер водительского удостоверения.
Проверьте актуальность данных, измените при необходимости.

4.Создание заявки
Укажите:
Место приемки/отгрузки (например, Московское шоссе, 19).
Тип операции: "Я привез груз" или "Я забираю груз".
Клиентский номер заявки.
Добавьте номер транспортного средства и прицепа (если есть).

5. Получение QR-кода
После завершения регистрации бот отправит QR-код (или 6-значный код), который нужно отсканировать на стойке регистрации.

6. Использование кода
Отсканируйте QR-код на стойке регистрации. Ваши данные будут переданы в систему для обработки.

Важно! Следите за правильностью ввода данных и при необходимости редактируйте их перед подтверждением."""
        case "en":
            return """This chat-bot is designed for convenient driver registration during cargo acceptance/dispatch. It can be used from a personal smartphone or at a dispatcher's desk.
    
Usage steps:
1. Starting the bot
Send the /start command in Telegram.
Select the communication language.

2. Registration. If you are using the bot for the first time:
At the desk, select the "No QR-code" option.
Enter the driver's license number, then Authorize. Then enter your personal data: Full Name, phone number.
Check the entered data and confirm it.

3. Authorization. If you have already registered:
Enter your driver's license number.
Check the relevance of the data, change if necessary.

4.Creating an application
Specify:
Pickup/delivery location (e.g., Moskovskoe Highway, 19).
Operation type: "I brought the cargo" or "I am picking up the cargo".
Client's application number.
Add the vehicle and trailer number (if any).

5. Obtaining a QR-code
After completing the registration, the bot will send a QR-code (or a 6-digit code) that needs to be scanned at the registration desk.

6. Using the code
Scan the QR-code at the registration desk. Your data will be transmitted to the system for processing.

Important! Make sure that you enter the data correctly and edit it if necessary before confirmation."""
        case "kz":
            return """Бұл чат-бот жүк қабылдау/ жіберу кезінде жүргізушілерді ыңғайлы тіркеу үшін арналған. Оны жеке смартфоннан да, диспетчерлік пункттегі стендтен де пайдалануға болады.
       
Пайдалану кезеңдері:
1. Ботты іске қосу
Telegram-ға /start командасын жіберіңіз.
Сөйлесу тілін таңдаңыз.

2. Тіркеу. Егер сіз бұл ботты бірінші рет пайдаланатын болсаңыз:
Стендтен "QR-код жоқ" опциясын таңдаңыз.
Көлік куәлігінің нөмірін, содан кейін Авторизацияны енгізіңіз. Содан кейін жеке деректеріңізді енгізіңіз: Тегі, аты, әкесінің аты, телефон нөмірі.
Енгізілген деректерді тексеріп, растаңыз.

3. Авторизация. Егер сіз бұрын тіркелген болсаңыз:
Жүргізуші куәлігінің нөмірін енгізіңіз.
Деректердің өзектілігін тексеріп, қажет болса өзгертіңіз.

4. Өтінім жасау
Көрсетіңіз:
Жүкті қабылдау/ жіберу орны (мысалы, Мәскеу тас жолы, 19).
Операция түрі: "Мен жүкті әкелдім" немесе "Мен жүкті алып кетемін".
Клиенттің өтінім нөмірі.
Көлік құралы мен тіркеменің нөмірін қосыңыз (егер бар болса).

5. QR-код алу
Тіркеу аяқталғаннан кейін бот тіркеу стендінде сканерлеу керек QR-кодты (немесе 6 таңбалы кодты) жібереді.

6. Кодты пайдалану
Тіркеу стендінде QR-кодты сканерлеңіз. Сіздің деректеріңіз өңдеу үшін жүйеге жіберіледі.

Маңызды! Деректерді дұрыс енгізуді қадағалап, қажет болса растау алдында өңдеңіз."""
        case "by":
            return """Чат-бот прызначаны для зручнай рэгістрацыі вадзіцеляў пры прыёмцы/адгрузцы грузу. Выкарыстанне магчыма як з асабістага смартфона, так і на стойцы ў дыспетчарскай.
 
Крокі выкарыстання:
1. Запуск бота
Адпраўце каманду /start у Telegram.
Выберыце мову зносін.

2. Рэгістрацыя. Калі вы ўпершыню карыстаецеся ботам:
На стойцы выберыце опцыю "Няма QR-кода".
Увядзіце нумар ВУ, затым Аўтарызавацца. Пасля ўвядзіце асабістыя дадзеныя: ПІБ, нумар тэлефона.
Праверце ўведзеныя дадзеныя і пацвердзіце іх.

3. Аўтарызацыя. Калі вы ўжо рэгістраваліся:
Увядзіце нумар вадзіцельскага пасведчання.
Праверце актуальнасць дадзеных, змяніце пры неабходнасці.

4.Ствараэнне заяўкі
Укажыце:
Месца прыёмкі/адгрузкі (напрыклад, Маскоўскае шасэ, 19).
Тып аперацыі: "Я прывёз груз" або "Я забіраю груз".
Кліенцкі нумар заяўкі.
Дадайце нумар транспартнага сродку і прычэпа (калі ёсць).

5. Атрыманне QR-кода
Пасля завяршэння рэгістрацыі бот адправіць QR-код (ці 6-значны код), які трэба адсканаваць на стойцы рэгістрацыі.

6. Выкарыстанне кода
Адскануйце QR-код на стойцы рэгістрацыі. Вашы дадзеныя будуць перададзеныя ў сістэму для апрацоўкі.

Важна! Сачыце за правільнасцю ўводу дадзеных і пры неабходнасці рэдагуйце іх перад пацвярджэннем."""
        case "az":
            return """Çat-bot, yükün qəbulu/göndərilməsi zamanı sürücülərin rahat qeydiyyatı üçün nəzərdə tutulub. Həm şəxsi smartfondan, həm də dispetçer məntəqəsindəki stenddən istifadə etmək olar.
    
İstifadə addımları:
1. Botun işə salınması
Telegram-a /start əmrini göndərin.
Rabitə dilini seçin.

2. Qeydiyyat. Əgər botdan ilk dəfə istifadə edirsinizsə:
Stenddə "QR-kod yoxdur" seçimini seçin.
VÖ nömrəsini, sonra Avtorizasiya düyməsini daxil edin. Sonra şəxsi məlumatlarınızı daxil edin: Ad, Soyad, Ata adı, telefon nömrəsi.
Daxil edilmiş məlumatları yoxlayın və təsdiqləyin.

3. Avtorizasiya. Əgər artıq qeydiyyatdan keçmisinizsə:
Sürücü vəsiqəsinin nömrəsini daxil edin.
Məlumatların aktuallığını yoxlayın, zəruri hallarda dəyişdirin.

4.Ərizənin yaradılması
Göstərin:
Yükün qəbulu/göndərilmə yeri (məsələn, Moskva şose, 19).
Əməliyyat növü: "Yükü gətirdim" və ya "Yükü götürürəm".
Müəssisənin sifariş nömrəsi.
Nəqliyyat vasitəsinin və qoşqu nömrəsini əlavə edin (əgər varsa).

5. QR-kodun alınması
Qeydiyyat başa çatdıqdan sonra bot qeydiyyat stendində skaner edilməli olan QR-kodu (və ya 6 rəqəmli kodu) göndərəcək.

6. Kodun istifadəsi
Qeydiyyat stendində QR-kodu skaner edin. Məlumatlarınız emal üçün sistemə ötürüləcək.

Vacibdir! Məlumatların düzgün daxil edilməsinə nəzarət edin və zəruri hallarda təsdiq etməzdən əvvəl düzəldin."""
        case "uz":
            return """Ushbu chat-bot yukni qabul qilish/jo'natishda haydovchilarni qulay ro'yxatdan o'tkazish uchun mo'ljallangan. Undan shaxsi smartfondan hamda dispetcher stolida joylashgan stend orqali foydalanish mumkin.

Foydalanish bosqichlari:
1. Botni ishga tushirish
Telegramga /start buyrug'ini yuboring.
Aloqa tilini tanlang.

2. Ro'yxatdan o'tish. Agar siz botdan birinchi marta foydalanayotgan bo'lsangiz:
Stendda "QR-kod yo'q" opsiyasini tanlang.
Haydovchilik guvohnomasining raqamini, so'ngra Avtorizatsiya tugmasini kiriting. Shundan so'ng shaxsiy ma'lumotlaringizni kiriting: F.I.O., telefon raqami.
Kiritilgan ma'lumotlarni tekshirib, tasdiqlang.

3. Avtorizatsiya. Agar siz avval ro'yxatdan o'tgan bo'lsangiz:
Haydovchilik guvohnomasining raqamini kiriting.
Ma'lumotlarning dolzarbligini tekshirib, zarurat bo'lsa o'zgartiring.

4. Ariza yaratish
Ko'rsating:
Yukni qabul qilish/jo'natish joyi (masalan, Moskva shossesI, 19).
Operatsiya turi: "Yukni olib keldim" yoki "Yukni olib ketayapman".
Mijozning ariza raqami.
Transport vositasi va prisep raqamini qo'shing (agar mavjud bo'lsa).

5. QR-kodni olish
Ro'yxatdan o'tish tugagach, bot ro'yxatdan o'tish stendida skaner qilinishi kerak bo'lgan QR-kodni (yoki 6 xonali kodni) yuboradi.

6. Koddan foydalanish
Ro'yxatdan o'tish stendida QR-kodni skaner qiling. Sizning ma'lumotlaringiz qayta ishlash uchun tizimga yuboriladi.

Muhim! Ma'lumotlarni to'g'ri kiritishni kuzatib boring va zarurat bo'lsa tasdiqlashdan oldin ularni tahrirlang."""
        case "tg":
            return """Чат-бот барои бақайдгирии осони ронандагон ҳангоми қабул/бор кардани бордориш пешбинӣ шудааст. Истифода ҳам аз смартфони шахсӣ ва ҳам дар мизи корӣ дар диспетчер имконпазир аст.
    
Марҳилаҳои истифода:
1. Оғоз кардани бот
Фармони /start-ро ба Telegram фиристед.
Забони муоширатро интихоб кунед.

2. Бақайдгирӣ. Агар шумо барои аввалин бор аз бот истифода мебаред:
Дар мизи корӣ имконоти "QR-код надорад"-ро интихоб кунед.
Рақами шаҳодатномаи ронандагиро ворид кунед, баъд Авторизатсия. Баъд маълумоти шахсиро ворид кунед: Ном, насаб, рақами телефон.
Маълумоти воридшударо санҷед ва онҳоро тасдиқ кунед.

3. Авторизатсия. Агар шумо аллакай ба қайд гирифта бошед:
Рақами шаҳодатномаи ронандагиро ворид кунед.
Актуалнокии маълумотро санҷед, дар сурати зарурат ислоҳ кунед.

4.Эҷоди дархост
Нишон диҳед:
Ҷойи қабул/бор кардан (масалан, Шоҳроҳи Москва, 19).
Навъи амалиёт: "Ман бор овардам" ё "Ман бор мегирам".
Рақами дархости мизоҷ.
Рақами воситаи нақлиёт ва прицепро (агар бошад) илова кунед.

5. Гирифтани QR-код
Пас аз анҷоми бақайдгирӣ бот QR-кодро (ё коди 6-рақамӣ) мефиристад, ки бояд дар мизи корӣ сканер карда шавад.

6. Истифодаи код
QR-кодро дар мизи корӣ сканер кунед. Маълумоти шумо барои коркард ба система интиқол дода мешавад.

Муҳим! Ба дурустии воридкунии маълумот диққат диҳед ва дар сурати зарурат пеш аз тасдиқ онҳоро таҳрир кунед."""


def user_agreement_text(lang: str, link: str) -> str:
    match lang:
        case "ru":
            return (f"Пользовательское соглашение доступно по ссылке:"
                    f"\n\n{link}\n\n"
                    f"Для ознакомления перейдите по ней на сайт компании.")
        case "en":
            return (f"The user agreement is available at the link:"
                    f"\n\n{link}\n\n"
                    f"Please follow the link to the company's website to review it.")
        case "kz":
            return (f"Пайдаланушы келісімі сілтеме бойынша қолжетімді:"
                    f"\n\n{link}\n\n"
                    f"Онымен танысу үшін компания сайтына өтіңіз.")
        case "by":
            return (f"Карыстальніцкае пагадненне даступна па спасылцы:"
                    f"\n\n{link}\n\n"
                    f"Для азнаямлення перайдзіце па ёй на сайт кампаніі.")
        case "az":
            return (f"İstifadəçi müqaviləsi linkdə mövcuddur:"
                    f"\n\n{link}\n\n"
                    f"Tanış olmaq üçün şirkətin veb saytına keçin.")
        case "uz":
            return (f"Foydalanuvchi shartnomasi quyidagi havola orqali mavjud:"
                    f"\n\n{link}\n\n"
                    f"U bilan tanishish uchun kompaniya veb-saytiga o'ting.")
        case "tg":
            return (f"Созишномаи истифодабаранда дар ин суроғ дастрас аст:"
                    f"\n\n{link}\n\n"
                    f"Барои шинос шудан ба вебсайти ширкат гузаред.")
