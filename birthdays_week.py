from datetime import datetime, timedelta

def get_birthdays_per_week(users):
    # Определяем текущую дату
    today = datetime.now().date()
    current_year = today.year

    # Определяем дату начала недели (понедельник)
    start_of_week = today - timedelta(days=today.weekday())

    # Определяем дату конца недели (воскресенье)
    end_of_week = start_of_week + timedelta(days=6)

    # Создаем словарь, в котором ключами будут дни недели, а значениями - список именинников
    birthdays_per_day = {}

    # Итерируемся по пользователям
    for user in users:
        name = user['name']
        birthday = user['birthday'].replace(year=current_year).date()

        # Проверяем, что день рождения пользователя находится в текущей неделе
        if start_of_week <= birthday <= end_of_week:
            # Определяем день недели дня рождения пользователя
            weekday = birthday.strftime('%A')

            # Добавляем пользователя в список именинников для соответствующего дня недели
            birthdays_per_day.setdefault(weekday, []).append(name)

    # Выводим список именинников по дням недели
    for weekday, names in birthdays_per_day.items():
        print(f'{weekday}: {", ".join(names)}')



