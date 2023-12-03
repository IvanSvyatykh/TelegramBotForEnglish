start_registration = ("Здравствуйте, {name} !\n"
                      "Я телеграмм бот для ведения дневника для людей с диабетом.\n"
                      "Я вижу вас первый раз, вам будет нужно зарегестрироваться.\n"
                      "Укажите свой тип диабета с помощью кнопок.")

information = ("Я телеграмм бот для ведения дневника для людей с диабетом.\n"
               "Если я вас знаю, вы сможете занести данные в выбранный месяц текущего года.\n"
               "Также вы сможете просмотреть уже заполненные данные и редактировать их.\n"
               "Вы сможете получить заполненный данными за месяц или неделю pdf файл.\n")

security = ("Почему мне можно доверять?\n"
            "Я не храню никакой важной информаии о вас.\n"
            "Отличаю пользователей друг от друга, только по id, который им присваивает Telegram\n"
            "Также я помню ваше имя, которое видят все пользователи.\n"
            "То есть я не знаю ни какой важной информации, по которой вас можно индефицировать в реальной жизни.")

greetings = ("Здравствуйте, {name} ! Я рад вас видить снова ! \n"
             "Информация об аккаунте: \n"
             "Id пользователя: {id}\n"
             "Имя пользователя: {name}\n"
             "Тип диабета: {diabetes_type}\n")

help = ("Я обладаю следующими командами:\n"
        "/help - команда выводит список команд.\n"
        "/information - команда позволит получить информацию об боте.\n"
        "/security - команда расскажет почему мне не страшно доверить данные.\n"
        "/report - команда позволит занести данные в дневник.\n"
        "/start - команда позволяет зарегистрироваться или получить информацию об аккаунте.\n")

choose_month = ("Выберите месяц.\n"
                "Внимание, месяц будет принадлежить текущему {year} году.\n")

choose_day = ("Выберите день. \n"
              "Внимание, день будет принадлежить месяцу({month}) текущего {year} года.\n")

registration = (f"Отлично! Вы успешно зарегестрированны.С следующими данными:\n"
                "Id пользователя: {id}\n"
                "Имя пользователя: {name}\n"
                "Тип диабета: {diabetes_type}\n")
