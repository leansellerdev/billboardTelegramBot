
# Billboard Managemet System Bot

Этот Telegram-бот позволяет бронировать билборды

Файлы проекта находятся в папке "core" и организованы в собственные папки категорий

- buttons - настройки кнопок, с помощью которых пользователь взаимодействует с ботом
- database - модели сущностей и ORM запросы к билборды
- filters - фильтры входящих сообщений для обработчиков запросов
- handlers - обработчики входящих обновлений(запросов) от пользователей
- middlewares - обработчики сообщений до того, как они попадут в хэндлеры.
    - в данной папке есть throttling middleware, что позволяет защитить бота от спама
- states - состояния бота, которые позволяют контролировать то, на каком шаге сейчас находится пользователь
- utils - различные утилиты для сущностей, такие как создание excel файлов для отправки пользователям, менеджерам или администраторам
