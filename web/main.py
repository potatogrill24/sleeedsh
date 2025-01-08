import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import requests
import base64
import logging
import re
import csv
import os
import time
import pandas as pd
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from ml.recommendation_system.model import RecommendationSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8080"
SEARCH_API_URL = "http://localhost:8009" # Add this line


# Параметры подключения к бд
DB_RECOMMEND_CONFIG = {
    "dbname": "internet_shop",  
    "user": "admin",            
    "password": "secretpassword",        
    "host": "localhost",        
    "port": 5433                
}


def self_profile(jwt):
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.get(f"{API_URL}/api/profile/self", headers=headers)
    if response.status_code == 200:
        return response.json()

    logger.error(f"Ошибка получения профиля: {response.status_code} - {response}")
    return {}


def validate_name(name):
    """
    Проверяет, что ФИО состоит из трёх слов, содержащих только буквы.
    """
    # Регулярное выражение для проверки ФИО
    pattern = r"^[А-Яа-яA-Za-z-]+\s[А-Яа-яA-Za-z-]+\s[А-Яа-яA-Za-z-]+$"
    return re.match(pattern, name) is not None

def validate_password(password):
    """
    Проверяет, что пароль содержит минимум 5 символов и хотя бы одну цифру.
    """
    # Проверка длины пароля
    if len(password) < 5:
        return False
    # Проверка наличия хотя бы одной цифры
    if not re.search(r"\d", password):
        return False
    return True

def login(username, password, role):
    auth_str = f"{role}:{username}:{password}"
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    headers = {"Authorization": f"Basic {auth_base64}"}
    response = requests.get(f"{API_URL}/api/login", headers=headers)
    if response.status_code == 200:
        logger.info("Успешная авторизация")
        return response.json().get('jwt')
    else:
        logger.error(f"Ошибка авторизации: {response.status_code} - {response.text}")
        st.error(f"Ошибка авторизации: {response.text}")
        return None

def logout(jwt):
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.post(f"{API_URL}/api/logout", headers=headers)
    if response.status_code == 200:
        logger.info("Успешный выход")
        st.session_state['jwt'] = None
        st.session_state['role'] = None
        st.session_state['logged_in'] = False
        return response.json()
    else:
        logger.error(f"Ошибка выхода: {response.status_code} - {response.text}")
        return None

def register(name, username, password):
    """
    Регистрирует нового пользователя с валидацией ФИО и пароля.
    """
    # Валидация ФИО
    if not validate_name(name):
        st.error("ФИО должно состоять из трёх слов, содержащих только буквы и дефисы.")
        return None

    # Валидация пароля
    if not validate_password(password):
        st.error("Пароль должен содержать минимум 5 символов и хотя бы одну цифру.")
        return None

    # Если валидация прошла успешно, продолжаем регистрацию
    reg = f"{name}:{username}:{password}"
    reg_bytes = reg.encode('utf-8')
    reg_base64 = base64.b64encode(reg_bytes).decode('utf-8')
    headers = {"Authorization": f"Basic {reg_base64}"}
    response = requests.post(f"{API_URL}/api/register", headers=headers)
    if response.status_code == 200:
        logger.info("Успешная регистрация.")
        role = "user"
        jwt = login(username, password, role)
        if jwt:
            st.session_state['jwt'] = jwt
            st.session_state['role'] = role
            st.session_state['logged_in'] = True
            st.rerun()
        return response.json()
    else:
        logger.error(f"Ошибка регистрации: {response.status_code} - {response.text}")
        st.error(f"Ошибка регистрации: {response.text}")
        return None

def login_page():
    st.title("Авторизуйтесь или зарегистрируйтесь")
    tab_login, tab_register = st.tabs(["Вход", "Регистрация"])
    with tab_login:
        # role = st.selectbox("Выберите роль", ["user", "shop"], key="login_role")
        role = "user"
        username = st.text_input("Логин", key="login")
        password = st.text_input("Пароль", type="password", key="login_password")
        if st.button("Войти"):
            jwt = login(username, password, role)
            if jwt:
                st.session_state['jwt'] = jwt
                st.session_state['role'] = role
                st.session_state['logged_in'] = True
                st.rerun()

    with tab_register:
        name = st.text_input("ФИО", key="fio")
        username = st.text_input("Логин", key="reg")
        password = st.text_input("Пароль", type="password", key="reg_pas")
        password2 = st.text_input("Повторите пароль", type="password", key="reg_pas2")
        if st.button("Зарегистрироваться"):
            if not name or not username or not password or not password2:
                st.error("Все поля должны быть заполнены.")
                return
            if password != password2:
                st.error("Ваши пароли не совпадают")
                return
            register(name, username, password)


def cart_page(jwt):
    profile = self_profile(jwt)
    st.title(f"Корзина")

    st.subheader(f"Сумма товаров {profile['total_cart_price']} рублей")

    st.write("")
    st.subheader("Список товаров в корзине:")
    st.write("")
    cart = profile['cart']
    i = 0
    for product in cart:
        i += 1
        st.write(f"{product['name']} - {product['price']}")
        if st.button("Удалить", key=f"{product['id']} - {i}"):
            remove_from_cart(jwt, product['id'])
            st.rerun()

    st.write("")
    if st.button("Купить все"):
        buy(jwt)

def deposit(jwt, amount):
    headers = {"Authorization": f"Bearer {jwt}"}
    data = {"money": amount}
    response = requests.post(f"{API_URL}/api/deposit", headers=headers, json=data)
    if response.status_code == 200:
        logger.info("Баланс успешно пополнен")
        return response.json()
    else:
        logger.error(f"Ошибка пополнения баланса: {response.status_code} - {response.text}")
        return None

def buy(jwt):
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.post(f"{API_URL}/api/buy", headers=headers)
    if response.status_code == 200:
        logger.info("Успешная покупка")
        st.success("Покупка завершена")
        return response.json()
    else:
        logger.error(f"Ошибка покупки: {response.status_code} - {response.text}")
        st.error("Не удалось совершить покупку! Проверьте баланс!")
        return None

def add_to_cart(jwt, product_id):
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.post(f"{API_URL}/api/cart/add/{product_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Ошибка добавления товара в корзину: {response.status_code} - {response.text}")
        return None

def remove_from_cart(jwt, product_id):
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.delete(f"{API_URL}/api/cart/delete/{product_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Ошибка удаления товара из корзины: {response.status_code} - {response.text}")
        return None


def get_category_id_for_product(product_id):
    """
    Получает category_id для продукта.
    """
    # Пример: запрос к базе данных
    query = "SELECT category_id FROM products WHERE id = %s;"
    try:
        with psycopg2.connect(**DB_RECOMMEND_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (product_id,))
                result = cur.fetchone()
                if result:
                    return result[0]  # Возвращаем category_id
                else:
                    logger.error(f"Продукт с id={product_id} не найден.")
                    return None
    except Exception as e:
        logger.error(f"Ошибка при получении category_id: {e}")
        return None


def create_review(jwt, product_id, rate, text):
    profile = self_profile(jwt)

    user_id = profile['data']['id']

    category_id = get_category_id_for_product(product_id)  # Нужно реализовать эту функцию

    if not category_id:
        logger.error(f"Не удалось получить category_id для product_id={product_id}")
        return None

    # Отправляем запрос на создание отзыва
    headers = {"Authorization": f"Bearer {jwt}"}
    data = {"product_id": product_id, "rate": rate, "text": text}
    response = requests.post(f"{API_URL}/api/review/create", headers=headers, json=data)

    if response.status_code == 200:
        logger.info("Отзыв успешно создан")

        # Записываем данные в ratings.csv
        try:
            ratings_file_path = os.path.join(".", "ml", "recommendation_system", "data", "ratings.csv")
            file_exists = os.path.isfile(ratings_file_path)

            with open(ratings_file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Если файл пустой, добавляем заголовки
                if not file_exists:
                    writer.writerow(["rating", "user_id", "item_id", "category_id"])

                # Записываем данные
                writer.writerow([rate, user_id, product_id, category_id])

            logger.info(f"Данные успешно записаны в {ratings_file_path}")
        except Exception as e:
            logger.error(f"Ошибка записи в файл ratings.csv: {e}")

        return response.json()
    else:
        logger.error(f"Ошибка создания отзыва: {response.status_code} - {response.text}")
        return None

def review_page(jwt, product_id):
    st.title("Управление отзывами")

    # Проверяем, есть ли состояние для оценки и текста
    if f"rate_{product_id}" not in st.session_state:
        st.session_state[f"rate_{product_id}"] = 0.0
    if f"text_{product_id}" not in st.session_state:
        st.session_state[f"text_{product_id}"] = ""

    # Слайдер для оценки
    rate = st.slider(
        "Оценка",
        min_value=1,
        max_value=5,
        step=1,
        key=f"rate_slider_{product_id}"
    )

    # Текстовое поле для отзыва
    text = st.text_area(
        "Текст отзыва",
        st.session_state[f"text_{product_id}"],
        key=f"text_area_{product_id}"
    )

    # Кнопка для создания отзыва
    if st.button("Создать отзыв", key=f"create_review_{product_id}"):
        response = create_review(jwt, product_id, rate, text)
        if response:
            st.session_state[f"rate_{product_id}"] = 0.0
            st.session_state[f"text_{product_id}"] = ""
            if 'review_product_id' in st.session_state:
                del st.session_state['review_product_id']
        st.rerun()  # Перезагрузка страницы, чтобы закрыть текущую панель

    # Кнопка для закрытия панели
    if st.button("Закрыть", key=f"close_review_{product_id}"):
        # Очищаем состояние для текущего продукта
        st.session_state[f"rate_{product_id}"] = 0.0
        st.session_state[f"text_{product_id}"] = ""
        if 'review_product_id' in st.session_state:
            del st.session_state['review_product_id']
        st.rerun()  # Перезагрузка страницы, чтобы закрыть текущую панель


def is_file_modified(file_path, last_modified_time):
    """
    Проверяет, изменился ли файл.
    """
    if not os.path.exists(file_path):
        return False
    current_modified_time = os.path.getmtime(file_path)
    return current_modified_time > last_modified_time


def retrain_model_if_needed(recommendation_system, ratings_file_path, last_modified_time):
    """
    Переобучает модель, если файл ratings.csv изменился.
    """
    if is_file_modified(ratings_file_path, last_modified_time):
        print("Файл ratings.csv изменен. Переобучение модели...")
        try:
            # Проверяем, что файл не пуст
            if os.path.getsize(ratings_file_path) == 0:
                print("Файл ratings.csv пуст. Переобучение не требуется.")
                return recommendation_system, last_modified_time

            reviews = pd.read_csv(ratings_file_path, sep=',')
            required_columns = ['user_id', 'item_id', 'rating', 'category_id']
            if not all(column in reviews.columns for column in required_columns):
                raise ValueError(f"Файл ratings.csv должен содержать столбцы: {required_columns}")
            
            # Переобучение модели
            recommendation_system = RecommendationSystem(reviews).load_data().train_model()
            print("Модель успешно переобучена.")
            return recommendation_system, time.time()  # Возвращаем обновленное время изменения файла
        except Exception as e:
            print(f"Ошибка при переобучении модели: {e}")
            return None, last_modified_time  # Возвращаем None, если произошла ошибка
    else:
        return recommendation_system, last_modified_time


def get_recommendations_from_db(user_id):
    """
    Получает рекомендации для пользователя из таблицы user_recs.
    """
    query = """
        SELECT p.id, p.name, p.price
        FROM user_recs ur
        JOIN products p ON ur.product_id = p.id
        WHERE ur.user_id = %s
        ORDER BY ur.id
        LIMIT 10;
    """
    try:
        # Подключаемся к базе данных
        with psycopg2.connect(**DB_RECOMMEND_CONFIG) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (user_id,))
                recommendations = cur.fetchall()
                return recommendations
    except Exception as e:
        logger.error(f"Ошибка при получении рекомендаций из базы данных: {e}")
        return []


def rec_page(jwt):
    """
    Страница с рекомендациями для пользователя.
    """
    st.title("Возможно вам понравится:")

    # Получаем профиль пользователя, чтобы узнать его ID
    profile = self_profile(jwt)
    if not profile:
        st.error("Не удалось загрузить профиль пользователя.")
        return

    user_id = profile['data']['id']  # Предполагаем, что ID пользователя хранится в профиле

    # Путь к файлу ratings.csv
    ratings_file_path = os.path.join(".", "ml", "recommendation_system", "data", "ratings.csv")

    # Инициализация времени последнего изменения файла
    if 'last_modified_time' not in st.session_state:
        st.session_state['last_modified_time'] = 0

    # Переобучение модели, если файл изменился
    recommendation_system, st.session_state['last_modified_time'] = retrain_model_if_needed(
        st.session_state.get('recommendation_system'),
        ratings_file_path,
        st.session_state['last_modified_time']
    )

    # Если модель не была переобучена, используем существующую
    if recommendation_system is None:
        recommendation_system = st.session_state.get('recommendation_system')
        if recommendation_system is None:
            st.error("Модель не была инициализирована. Невозможно получить рекомендации.")
            return

    # Сохраняем модель в session_state
    st.session_state['recommendation_system'] = recommendation_system

    # Генерация рекомендаций
    recommendations = recommendation_system.recommend_items(user_id, top_n=7)
    if not recommendations:
        print("Реков нет:(")

    # Сохранение рекомендаций в базу данных
    recommendation_system.save_recommendations_to_db(user_id, recommendations)

    # Получаем рекомендации из базы данных
    recommended_products = get_recommendations_from_db(user_id)

    if not recommended_products:
        st.warning("Рекомендации не найдены.")
        return

    # Отображаем рекомендации
    for product in recommended_products:
        st.write(f"Название: {product['name']}, Цена: {product['price']}")
        if st.button("Добавить в корзину", key=product['id']):
            add_to_cart(jwt, product['id'])
            st.success("Товар добавлен в корзину")


def get_all_products():
    response = requests.get(f"{SEARCH_API_URL}/products")
    if response.status_code == 200:
        return response.json().get("products", [])
    else:
        logger.error(f"Ошибка получения товаров: {response.status_code} - {response.text}")
        return []

def search_products(query):
    response = requests.post(f"{SEARCH_API_URL}/search", json={"query": query})
    if response.status_code == 200:
        return response.json().get("products", [])
    else:
        logger.error(f"Ошибка поиска товаров: {response.status_code} - {response.text}")
        return []

def cat_page(jwt):
    st.title("Каталог")
    search_query = st.text_input("Поиск товара")
    
    if search_query:
        products = search_products(search_query)
    else:
        products = get_all_products()
    
    for product in products:
        st.write(f"Название: {product['name']}, Цена: {product['price']}")
        if st.button("Добавить в корзину", key=product['id']):
            add_to_cart(jwt, product['id'])
            st.success("Товар добавлен в корзину")

def profile_page_user(jwt):
    profile = self_profile(jwt)
   
    # Создаем две колонки: одна для заголовка, другая для кнопки
    col1, col2 = st.columns([3, 1])  # Первая колонка шире, вторая уже
    
    with col1:
        st.subheader(profile['data']['name'])
        # st.subheader(f"Роль: пользователь")
    
    with col2: # Кнопка "Выйти из аккаунта" в правом верхнем углу
        if st.button("Выйти из аккаунта"):
            logout(jwt)
            st.rerun()

    st.write("")
    st.write("")
    st.subheader(f"Баланс: {profile['data']['balance']} рублей")
    st.write("Пополнение баланса")
    amount = st.number_input("Сумма, рублей", min_value=1)
    if st.button("Пополнить"):
        deposit(jwt, amount)
        st.rerun()

    st.write("")
    st.write("")
    st.subheader(f"Чеки")
    checks = profile['paychecks']
    for check in checks:
        # common = check['common']
        # st.write(f"{common['total_price']} - {common['creation_time']}")

        products = check['products']
        i = 0
        for product in products:
            i += 1
            st.write(f"{product['name']} - {product['price']}")
            if st.button("Оставить отзыв", key=f"{product['id']}_{profile['data']['id']}_review - {i}"):
                # Устанавливаем состояние для отзыва
                st.session_state['review_product_id'] = product['id']
                st.rerun()  # Перезагружаем страницу, чтобы отобразить панель отзыва

            # Если текущий товар выбран для отзыва, отображаем панель отзыва
            if 'review_product_id' in st.session_state and st.session_state['review_product_id'] == product['id']:
                review_page(jwt, product['id'])

    st.write("")
    st.write("")
    st.subheader(f"Отзывы")
    st.write(f"Количество - {profile['review_count']}")
    st.write(f"Средняя оценка - {profile['review_avg']}")
    reviews = profile['reviews']
    j = 0
    for review in reviews:
        j += 1
        st.write(f"{review['product_name']} - {review['rate']}")
        st.write(f"{review['text']}")

# def profile_page_shop(jwt):
#     profile = self_profile(jwt)
#     st.title(profile['data']['name'])
#     st.subheader(f"Роль: магазин")
#     st.subheader(f"Продукты")
#     if st.button("Добавить продукт"):
#         st.rerun()
#     products=profile['products']
#     i = 0
#     for product in products:
#         st.write(f"Название - {product['product_name']}")
#         # st.write(f"Категория - {product['cat_name']}")
#         st.write(f"Цена - {product['product_price']}")
#         # st.write(f"Продажи - {product['sales']}")
#         # st.write(f"Количество оценок - {product['review_count']}")
#         # st.write(f"Средняя оценка - {product['review_avg']}")
#         i+=1
#         if st.button("Удалить продукт", key=f"{product['product_name']} - {i}"):
#             st.rerun()
#     if st.button("Выйти из аккаунта"):
#         logout(jwt)
#         st.rerun()


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if not st.session_state['logged_in']:
    login_page()
else:
    jwt = st.session_state['jwt']
    role = st.session_state['role']
    st.sidebar.title("Меню")
    if role == "user":
        page = st.sidebar.selectbox("Выберите страницу", ["Рекомендованное", "Каталог", "Корзина", "Профиль"])
    elif role == "shop":
        page = st.sidebar.selectbox("Выберите страницу", ["Каталог", "Профиль"])
    if page == "Рекомендованное":
        rec_page(jwt)
    elif page == "Каталог":
        cat_page(jwt)
    elif page == "Корзина":
        cart_page(jwt)
    elif page == "Профиль" and role == "user":
        profile_page_user(jwt)
    elif page == "Профиль" and role == "shop":
        profile_page_shop(jwt)
