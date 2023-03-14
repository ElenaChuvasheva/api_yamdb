# Проект YaMDb

## Описание
Проект **YaMDb** собирает **отзывы** пользователей на **произведения**. Произведения делятся на **категории**: «Книги», «Фильмы», «Музыка». Список **категорий** может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство», «Ювелирное искусство» или «Скульптура»).

Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Богатый папа, бедный папа» и «Думай медленно, решай быстро», а в категории «Музыка» — песня «На заре» группы «Альянс» и «Перемен» группы «Кино».

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Роман-эпопея», «Рок-н-ролл» или «Фэнтези»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Технологии
![Python](https://www.python.org/static/community_logos/python-logo-generic.svg)
![Django](https://static.djangoproject.com/img/logos/django-logo-positive.svg)

## Запуск проекта в dev режиме.

Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone <адрес репозитория>
```
```
cd api_yamdb/
```

Cоздайте и активируйте виртуальное окружение:
```
python -m venv venv
```
```
source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Перейдите в папку api_yamdb с файлом manage.py:
```
cd .\api_yamdb\
```
Зайдите в shell:
```
python manage.py shell
```
и выполните там команду для получения SECRET_KEY:
```
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
Запишите SECRET_KEY в соответствующее место в файле settings.py.
Выполните миграции:
```
python manage.py migrate
```
Добавьте в базу тестовые данные в случае необходимости:
```
python manage.py filldatabase
```
Запустите проект:
```
python manage.py runserver
```

## Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт ```/api/v1/auth/signup/```.
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт ```/api/v1/auth/token/```, в ответе на запрос ему приходит token (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт ```/api/v1/users/me/``` и заполняет поля в своём профайле (описание полей — в документации).

## Пользовательские роли
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.

**Модератор** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.

**Администратор** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Суперюзер Django** — обладает правами администратора (admin). Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## Ресурсы API YaMDb

**AUTH** - Регистрация пользователей и выдача токенов.

**CATEGORIES** - Категории (типы) произведений.

**GENRES** - Категории жанров.

**TITLES** - Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

**REVIEWS** - Отзывы.

**COMMENTS** - Комментарии к отзывам.

**USERS** - Пользователи.

## Документация к API доступна после запуска
```
http://127.0.0.1:8000/redoc/
```


## Авторы проекта

- [Елена Чувашева](https://github.com/ElenaChuvasheva) - руководство; модели, view и эндпойнты для отзывов, комментариев, рейтинга произведений
- [Алексей Воеводин](https://github.com/voevoda173) - модели, view и эндпойнты для произведений, категорий, жанров
- [Александр Макунин](https://github.com/madmas11) - система регистрации и аутентификации пользователей, права доступа
