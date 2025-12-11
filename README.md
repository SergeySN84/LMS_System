## Запуск проекта через Docker Compose

1. Склонируйте репозиторий:
   ```bash
   git clone <https://github.com/SergeySN84/LMS_System.git>
   cd LMS_System
2. Создайте .env из шаблона: cp .env.example .env
 Отредактируйте .env при необходимости
3. Соберите и запустите контейнеры: docker-compose up --build
4. Выполните миграции (в новом терминале): docker-compose exec backend python manage.py migrate
5. Создайте суперпользователя (опционально): docker-compose exec backend python manage.py createsuperuser
