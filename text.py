start_registration = ("Здравствуйте, {name} !\n "
                      "Это телеграмм бот для ведения дневника для людей с диабетом.\n "
                      "Я вижу вас первый раз, вам будет нужно зарегестрироваться.\n "
                      "Укажите свой тип диабета с помощью кнопок. ")

greetings = ("Здравствуйте, {name} ! Я рад вас видить снова ! \n"
             "Информация об аккаунте: \n"
             "Id пользователя: {id}\n"
             "Имя пользователя: {name}\n"
             "Тип диабета: {diabetes_type}\n")

help = ("Я обладаю следующими командами:\n"
        "/start - команда позволяет зарегистрироваться или получить информацию об аккаунте.\n"
        "/help - команда выводит список команд.\n"
        "/report - команда позволит выбрать прием пищи в который вы внесете свои данные.\n")

registration = (f"Отлично! Вы успешно зарегестрированны.С следующими данными:\n"
                "Id пользователя: {id}\n"
                "Имя пользователя: {name}\n"
                "Тип диабета: {diabetes_type}\n")
