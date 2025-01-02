import streamlit as st
import requests
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8080"


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
        st.error("Ошибка авторизации")
        return None


def logout(jwt):
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.post(f"{API_URL}/api/logout", headers=headers)
    if response.status_code == 200:
        logger.info("Успешный выход")
        return response.json()
    else:
        logger.error(f"Ошибка выхода: {response.status_code} - {response.text}")
        return None


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
        return response.json()
    else:
        logger.error(f"Ошибка покупки: {response.status_code} - {response.text}")
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


def create_review(jwt, product_id, rate, text):
    headers = {"Authorization": f"Bearer {jwt}"}
    data = {"product_id": product_id, "rate": rate, "text": text}
    response = requests.post(f"{API_URL}/api/review/create", headers=headers, json=data)
    if response.status_code == 200:
        logger.info("Отзыв успешно создан")
        return response.json()
    else:
        logger.error(f"Ошибка создания отзыва: {response.status_code} - {response.text}")
        return None


def delete_review(jwt, product_id):
    headers = {"Authorization": f"Bearer {jwt}"}
    data = {"product_id": product_id}
    response = requests.delete(f"{API_URL}/api/review/delete", headers=headers, json=data)
    if response.status_code == 200:
        logger.info("Отзыв успешно удален")
        return response.json()
    else:
        logger.error(f"Ошибка удаления отзыва: {response.status_code} - {response.text}")
        return None


def recommendations(jwt, count):
    headers = {"Authorization": f"Bearer {jwt}"}

    response = requests.get(f"{API_URL}/api/recommendations/{count}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Ошибка получения рекомендаций: {response.status_code} - {response.text}")
        return []

def self_profile(jwt):
    headers = {"Authorization": f"Bearer {jwt}"}
    response = requests.get(f"{API_URL}/api/profile/self", headers=headers)
    if response.status_code == 200:
        return response.json()

    logger.error(f"Ошибка получения профиля: {response.status_code} - {response}")
    return {}


def main(jwt):
    st.title("Рекомендованные товары")
    recommended_products = recommendations(jwt, 10)  # Параметр count
    for product in recommended_products:
        st.write(f"Название: {product['name']}, Цена: {product['price']}")
        if st.button("Добавить в корзину", key=product['id']):
            add_to_cart(jwt, product['id'])
            st.success("Товар добавлен в корзину")


def deposit_page(jwt):
    st.title("Пополнение баланса")
    amount = st.number_input("Сумма", min_value=1)
    if st.button("Пополнить"):
        deposit(jwt, amount)
        st.success("Баланс пополнен")


def buy_page(jwt):
    st.title("Покупка товаров")
    if st.button("Купить"):
        buy(jwt)
        st.success("Покупка завершена")


def review_page(jwt, product_id):
    st.title("Управление отзывами")
    rate = st.slider("Оценка", 0.0, 5.0)
    text = st.text_area("Текст отзыва")
    if st.button("Создать отзыв"):
        create_review(jwt, product_id, rate, text)
        st.success("Отзыв создан")
    if st.button("Удалить отзыв"):
        delete_review(jwt, product_id)
        st.success("Отзыв удален")


def login_page():
    st.title("Авторизация")
    role = st.selectbox("Выберите роль", ["user", "shop"])
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        jwt = login(username, password, role)
        if jwt:
            st.session_state['jwt'] = jwt
            st.session_state['role'] = role
            st.session_state['logged_in'] = True

def profile_page_user_self(jwt):
    profile = self_profile(jwt)
    st.title(profile['data']['name'])

    st.write(f"Баланс: {profile['data']['balance']}")

    st.subheader(f"Корзина - {profile['total_cart_price']}")
    cart = profile['cart']
    for product in cart:
        st.write(f"{product['name'] - product['price']}")

    st.subheader(f"Чеки")
    checks = profile['paychecks']
    for check in checks:
        common = check['common']
        st.write(f"{common['total_price']} - {common['creation_time']}")

        products = check['products']
        for product in products:
            st.write(f"{product['name']} - {product['price']}")
            if st.button("Оставить отзыв", key=f"{product['id']}_{profile['data']['id']}_review"):
                review_page(jwt, product['id'])


    st.subheader(f"Отзывы")
    st.write(f"Количество - {profile['review_count']}")
    st.write(f"Средняя оценка - {profile['review_avg']}")

    reviews = profile['reviews']
    for review in reviews:
        st.write(f"{review['product_id']} - {review['rate']}")
        st.write(f"{review['text']}")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page()
else:
    jwt = st.session_state['jwt']
    role = st.session_state['role']

    st.sidebar.title("Меню")
    page = st.sidebar.selectbox("Выберите страницу", ["Главная", "Пополнение баланса", "Покупка", "Профиль"])

    if page == "Главная":
        main(jwt)
    elif page == "Пополнение баланса":
        deposit_page(jwt)
    elif page == "Покупка":
        buy_page(jwt)
    elif page == "Профиль":
        profile_page_user_self(jwt)