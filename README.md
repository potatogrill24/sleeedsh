# Интернет-магазин

Интернет магазин электроники с возможностью пополнения баланса, оставлением отзывов и системой рекомендаций пользователю

### Сборка проекта

```bash
make # создает контейнер в докере
make down # останавливает и удаляет контейнер в докере
```

### Запуск веб-приложения

```bash
python3 -m venv venv
source/venv/bin/activate
streamlit run web/main.py
```

### Если нет каких-то пакетов после запуска стримлита, то

```bash
pip install (some_packet) # например, streamlit, psycopg2 или surprise
deactivate 
source/venv/bin/activate
streamlit run web/main.py # перезапуск окружения и повторный запуск веб-приложения
```
