from internal.infrastructure.postgres import *
from internal.domain.model import *


class UserRepository:
    __AUTHORIZATION_SQL = """
        SELECT u.id, c.password_hash
        FROM public.users AS u
        JOIN public.user_credentials AS c ON c.user_id = u.id 
        WHERE u.login = :login;
        """

    __CHANGE_BALANCE_SQL = """
        UPDATE public.users
        SET balance = balance + :diff
        WHERE id = :user_id;
        """

    __GET_PROFILE_BY_ID_SQL = """
        SELECT
            id,
            name,
            login,
            balance
        FROM public.users
        WHERE id = :id;
        """

    __REGISTER_USER_PART1_SQL = """
        INSERT INTO public.users (name, login)
        VALUES (:name, :login)
        RETURNING id;
        """

    __REGISTER_USER_PART2_SQL = """
        INSERT INTO public.user_credentials (user_id, password_hash)
        VALUES (:user_id, :password_hash);
        """

    __MAX_USER_ID_SQL = """
        SELECT MAX(id) AS id
        FROM users;
        """

    __CHECK_IF_USER_REGISTERED_SQL = """
        SELECT id
        FROM public.users
        WHERE login = :login;
        """

    def __init__(self, db: Database):
        self.__db = db

    @staticmethod
    def __map_to_user(query_result) -> User:
        return User(user_id=query_result['id'], name=query_result['name'], login=query_result['login'], balance=query_result['balance'])

    def authorize_user(self, login: str) -> tuple[int, str]:
        result = self.__db.query_row(
            self.__AUTHORIZATION_SQL,
            {"login": login}
        )
        return result['id'], result['password_hash']

    def change_balance(self, user_id: int, diff: int):
        self.__db.transaction(
            [(self.__CHANGE_BALANCE_SQL,
              {"diff": diff, "user_id": user_id})], level="SERIALIZABLE")

    def get_profile_by_id(self, user_id: int) -> User:
        result = self.__db.query_row(
            self.__GET_PROFILE_BY_ID_SQL,
            {"id": user_id})
        return self.__map_to_user(result)

    def register(self, name, login, password_hash):
        row = self.__db.query_row(self.__MAX_USER_ID_SQL)
        self.__db.execute(self.__REGISTER_USER_PART1_SQL,
                          {'name': name, 'login': login})
        self.__db.execute(self.__REGISTER_USER_PART2_SQL, {
                          'user_id': row['id']+1, 'password_hash': password_hash})

    def check_registered(self, login) -> bool:
        return len(self.__db.query(self.__CHECK_IF_USER_REGISTERED_SQL, {'login': login})) > 0


class ShopRepository:
    __AUTHORIZATION_SQL = """
        SELECT s.id, c.password_hash
        FROM public.shops AS s
        JOIN public.shop_credentials AS c ON c.shop_id = s.id
        WHERE s.login = :login;
        """

    __GET_PROFILE_BY_ID_SQL = """
        SELECT
            id,
            name,
            login
        FROM public.shops
        WHERE id = :id;
        """

    __SEARCH_SHOPS_SQL = """
        SELECT id, name, login
        FROM public.shops
        WHERE name ILIKE :query;
        """

    def __init__(self, db: Database):
        self.__db = db

    @staticmethod
    def __map_to_shop(query_result) -> Shop:
        return Shop(shop_id=query_result['id'], name=query_result['name'], login=query_result['login'])

    def authorize_shop(self, login: str) -> tuple[int, str]:
        result = self.__db.query_row(
            self.__AUTHORIZATION_SQL,
            {"login": login}
        )
        return result['id'], result['password_hash']

    def get_profile_by_id(self, shop_id: int) -> Shop:
        result = self.__db.query_row(
            self.__GET_PROFILE_BY_ID_SQL,
            {'id': shop_id})
        return self.__map_to_shop(result)

    def search_shops(self, query: str):
        rows = self.__db.query(self.__SEARCH_SHOPS_SQL,
                               {"query": f"%{query}%"})
        return [self.__map_to_shop(row) for row in rows]

# seems useless ...
# class CategoryRepository:
#     def __init__(self, db: Database):
#         self.__db = db
#         self.__GET_BY_ID_SQL = """
#             SELECT id, name
#             FROM public.categories
#             WHERE id = :id;
#             """
#
#     @staticmethod
#     def __map_to_category(query_result) -> Category:
#         return Category(category_id=query_result['id'], name=query_result['name'])
#
#     def get_category_by_id(self, category_id: int) -> Category:
#         return self.__map_to_category(self.__db.query_row(
#             self.__GET_BY_ID_SQL, {"id": category_id}
#         ))


class ProductRepository:
    __GET_BY_ID_SQL = """
        SELECT
            p.id AS product_id,
            p.category_id AS category_id,
            p.shop_id AS shop_id,
            p.name AS product_name,
            p.price AS product_price,
            c.name AS category_name,
            s.name AS shop_name
        FROM public.products AS p
        JOIN public.categories AS c ON c.id = p.category_id
        JOIN public.shops AS s ON s.id = p.shop_id
        WHERE p.id = :id;
        """

    __GET_SHOP_PRODUCTS_SQL = """
        SELECT
            p.id AS product_id,
            p.category_id AS category_id,
            p.shop_id AS shop_id,
            p.name AS product_name,
            p.price AS product_price
        FROM public.products AS p
        WHERE p.shop_id = :id;
        """

    __SEARCH_PRODUCTS_SQL = """
        SELECT id AS product_id, category_id, shop_id, name AS product_name, price AS product_price
        FROM public.products
        WHERE name ILIKE :query
        """

    __GET_ALL_PRODUCTS_SQL = """
        SELECT id AS product_id, category_id, shop_id, name AS product_name, price AS product_price
        FROM public.products
        """

    __SELECT_MOST_POPULAR_PRODUCTS_SQL = """
        SELECT
            p.id AS product_id,
            p.category_id AS category_id,
            p.shop_id AS shop_id,
            p.name AS product_name,
            p.price AS product_price,
            COUNT(r.id) AS review_count
        FROM public.products p
        LEFT JOIN public.reviews AS r ON p.id = r.product_id
        GROUP BY p.id, p.category_id, p.shop_id, p.name, p.price
        ORDER BY review_count DESC
        LIMIT :N;
        """

    __SELECT_PRODUCTS_BY_IDS_SQL = """
        SELECT
            id AS product_id,
            category_id AS category_id,
            shop_id AS shop_id,
            name AS product_name,
            price AS product_price
        FROM public.products AS p
        WHERE id IN {in_part};
        """

    __GET_CAT_NAME_SQL = """
        SELECT
            name as cat_name
        FROM public.categories
        WHERE id = :id
    
    """

    def __init__(self, db: Database):
        self.__db = db

    @staticmethod
    def map_to_product(query_result) -> Product:
        return Product(product_id=int(query_result['product_id']),
                       category_id=int(query_result['category_id']),
                       shop_id=int(query_result['shop_id']),
                       name=query_result['product_name'],
                       price=float(query_result['product_price']))

    def get_product_by_id(self, product_id: int) -> tuple[Product, str, str]:
        query_result = self.__db.query_row(
            self.__GET_BY_ID_SQL, {"id": product_id})
        return self.map_to_product(query_result), query_result['category_name'], query_result['shop_name']

    # def get_shop_products_stats(self, shop_id) -> list[tuple[Product, str, tuple[int, float], int]]:
    #     products_and_stats: list[tuple[Product, str, tuple[int, float], int]]
    #     rows = self.__db.query(self.__GET_SHOP_PRODUCTS_SQL, {'id': shop_id})
    #     for row in rows:
    #         current_product = self.map_to_product(row)
    #         cat_name = self.get_cat_name(row['category_id'])
    #         cur_prod_stats = ReviewRepository.get_product_stats(row['product_id'])
    #         cur_sales = PaycheckRepository.get_sales(row['product_id'])
    #         products_and_stats.append((current_product, cat_name, cur_prod_stats, cur_sales))
    #     return products_and_stats

    def get_shop_products(self, shop_id) -> list[Product]:
        result: list[Product] = []
        rows = self.__db.query(self.__GET_SHOP_PRODUCTS_SQL, {'id': shop_id})

        for row in rows:
            result.append(self.map_to_product(row))

        return result
    
    def get_cat_name(self, category_id: int) -> int:
        return self.__db.query(self.__GET_CAT_NAME_SQL, {'id': category_id})
    

    def search_products(self, query: str) -> list[Product]:
        results = self.__db.query(self.__SEARCH_PRODUCTS_SQL, {
                                  "query": f"%{query}%"})
        return [
            self.map_to_product(row) for row in results
        ]

    def get_all_products(self) -> list[Product]:
        results = self.__db.query(self.__GET_ALL_PRODUCTS_SQL)
        return [
            self.map_to_product(row) for row in results
        ]

    def select_n_most_popular(self, n: int) -> list[Product]:
        return [self.map_to_product(row) for row in self.__db.query(self.__SELECT_MOST_POPULAR_PRODUCTS_SQL, {"N": n})]

    def get_products_by_ids(self, ids: list[int]) -> list[Product]:
        in_part = '('
        for i in range(len(ids)):
            in_part += str(ids[i])
            if i != len(ids) - 1:
                in_part += ', '
        in_part += ')'

        rows = self.__db.query(
            self.__SELECT_PRODUCTS_BY_IDS_SQL.format(in_part=in_part))
        return [self.map_to_product(row) for row in rows]


class PaycheckRepository:
    __GET_PAYCHECKS_BY_USER_ID_SQL = """
        SELECT
            pa.id AS paycheck_id,
            pa.user_id AS user_id,
            pa.total_price AS total_price,
            pa.creation_time AS creation_time,
            p.id AS product_id,
            p.category_id AS category_id,
            p.shop_id AS shop_id,
            p.name AS product_name,
            p.price AS product_price
        FROM public.paychecks AS pa
        JOIN public.paycheck_items AS pa_it ON pa_it.paycheck_id = pa.id
        RIGHT JOIN public.products AS p ON p.id = pa_it.product_id
        WHERE pa.user_id = :id
        ORDER BY pa.creation_time DESC;
        """

    __SELECT_BOUGHT_PRODUCT_SQL = """
        SELECT
            p.user_id,
            pi.product_id
        FROM public.paycheck_items AS pi
        LEFT JOIN public.paychecks AS p ON p.id = pi.paycheck_id
        WHERE p.user_id = :user_id AND pi.product_id = :product_id;
        """
    
    __GET_SALES_SQL = """
        SELECT
            COUNT(*) AS sales
        FROM public.paycheck_items
        WHERE product_id = :id
    
    """

    def __init__(self, db: Database):
        self.__db = db

    @staticmethod
    def __map_to_paycheck(query_result):
        return Paycheck(paycheck_id=int(query_result['paycheck_id']),
                        user_id=int(query_result['user_id']),
                        total_price=float(query_result['total_price']),
                        creation_time=query_result['creation_time'])

    def get_users_paychecks(self, user_id: int) -> list[tuple[Paycheck, list[Product]]]:
        paychecks_and_products: dict[int,
                                     tuple[Paycheck, list[Product]]] = dict()

        rows = self.__db.query(
            self.__GET_PAYCHECKS_BY_USER_ID_SQL, {'id': user_id})
        for row in rows:
            current_paycheck = self.__map_to_paycheck(row)
            current_product = ProductRepository.map_to_product(row)

            if current_paycheck.id not in paychecks_and_products:
                paychecks_and_products[current_paycheck.id] = (
                    current_paycheck, [])

            paychecks_and_products[current_paycheck.id][1].append(
                current_product)

        return list(paychecks_and_products.values())
    
    def get_sales(self, product_id: int) -> int:
        rows = self.__db.query(self.__GET_SALES_SQL, {'id': product_id})
        if len(rows) != 1:
            return 0, 0
        row = rows[0]
        return int(row['sales']) if (row['sales']) is not None else 0,

    def check_if_bought(self, user_id: int, product_id: int) -> bool:
        return len(self.__db.query(self.__SELECT_BOUGHT_PRODUCT_SQL, {'user_id': user_id, 'product_id': product_id})) > 0


class ShoppingCartRepository:
    __ADD_PRODUCT_TO_CART_SQL = """
        INSERT INTO public.shopping_carts (user_id, product_id)
        VALUES (:user_id, :product_id);
        """

    __DROP_PRODUCT_FROM_USERS_CART_SQL = """
        DELETE FROM public.shopping_carts
        WHERE user_id = :user_id AND product_id = :product_id;
        """

    __GET_USERS_PRODUCTS_SQL = """
        SELECT 
            p.id AS product_id,
            p.category_id AS category_id,
            p.shop_id AS shop_id,
            p.name AS product_name,
            p.price AS product_price
        FROM public.shopping_carts AS sc
        JOIN public.products AS p ON sc.product_id = p.id
        WHERE sc.user_id = :user_id
        """

    __GET_CART_TOTAL_PRICE = """
        SELECT COALESCE(SUM(p.price), 0) AS sum
        FROM public.products AS p
        JOIN public.shopping_carts AS sc ON sc.product_id = p.id
        WHERE sc.user_id = :id
        GROUP BY sc.user_id;
        """

    __GET_CART_SIZE_SQL = """
        SELECT COUNT(*) AS size
        FROM public.shopping_carts
        WHERE user_id = :user_id;
        """

    __BUY_CART_SQL = """
        CALL buy_cart(:user_id);
        """

    def __init__(self, db: Database):
        self.__db = db

    def add_product_to_cart(self, user_id: int, product_id: int):
        self.__db.transaction([(self.__ADD_PRODUCT_TO_CART_SQL, {
            "user_id": user_id, "product_id": product_id})], level="SERIALIZABLE")

    def drop_product_from_users_cart(self, user_id: int, product_id: int):
        self.__db.transaction([(self.__DROP_PRODUCT_FROM_USERS_CART_SQL, {
            "user_id": user_id, "product_id": product_id})], level="SERIALIZABLE")

    def get_users_products(self, user_id: int) -> list[Product]:
        result: list[Product] = []
        query_result = self.__db.query(
            self.__GET_USERS_PRODUCTS_SQL, {"user_id": user_id})

        for row in query_result:
            result.append(ProductRepository.map_to_product(row))

        return result

    def buy_cart(self, user_id: int):
        self.__db.transaction(
            [(self.__BUY_CART_SQL, {"user_id": user_id})], level="SERIALIZABLE")

    def get_shopping_cart_size(self, user_id) -> int:
        return self.__db.query_row(self.__GET_CART_SIZE_SQL, {"user_id": user_id})['size']

    def get_shopping_cart_price(self, user_id) -> int:
        rows = self.__db.query(self.__GET_CART_TOTAL_PRICE, {"id": user_id})
        if len(rows) != 1:
            return 0
        return rows[0]['sum']


class ReviewRepository:
    __INSERT_REVIEW_SQL = """
        INSERT INTO public.reviews (user_id, product_id, rate, text)
        VALUES (:user_id, :product_id, :rate, :text);
        """

    __DELETE_REVIEW_SQL = """
        DELETE FROM public.reviews
        WHERE user_id = :user_id AND product_id = :product_id;
        """

    __GET_PRODUCT_REVIEWS_SQL = """
        SELECT
            r.id,
            r.user_id,
            r.product_id,
            r.rate,
            r.creation_time,
            r.text,
            p.name AS product_name
        FROM public.reviews r
        JOIN public.products p ON r.product_id = p.id
        WHERE r.product_id = :id
        ORDER BY r.creation_time DESC;
        """

    __GET_USER_REVIEWS_SQL = """
        SELECT
            r.id,
            r.user_id,
            r.product_id,
            r.rate,
            r.creation_time,
            r.text,
            p.name AS product_name
        FROM public.reviews r
        JOIN public.products p ON r.product_id = p.id
        WHERE r.user_id = :id
        ORDER BY r.creation_time DESC;
        """

    __CHECK_IF_REVIEWED_SQL = """
        SELECT id
        FROM public.reviews
        WHERE user_id = :user_id AND product_id = :product_id;
        """

    __GET_PRODUCT_STATS_SQL = """
        SELECT
            COUNT(*) AS review_count,
            AVG(rate) AS avg_rate
        FROM public.reviews
        WHERE product_id = :id
        GROUP BY product_id;
        """

    __GET_USER_STATS_SQL = """
        SELECT
            COUNT(*) AS review_count,
            AVG(rate) AS avg_rate
        FROM public.reviews
        WHERE user_id = :id
        GROUP BY user_id;
        """

    def __init__(self, db: Database):
        self.__db = db

    def create_review(self, user_id: int, product_id: int, rate: float, review_text: str):
        self.__db.transaction([(self.__INSERT_REVIEW_SQL,
                                {"user_id": user_id, "product_id": product_id, "rate": rate, "text": review_text})], level="SERIALIZABLE")

    def delete_review(self, user_id: int, product_id: int):
        self.__db.transaction([self.__DELETE_REVIEW_SQL, {
            "user_id": user_id, "product_id": product_id}], level="SERIALIZABLE")

    @staticmethod
    def __map_to_review(query_result):
        return Review(review_id=query_result['id'],
                      user_id=query_result['user_id'],
                      product_id=query_result['product_id'],
                      product_name=query_result['product_name'],
                      rate=query_result['rate'],
                      creation_time=query_result['creation_time'],
                      text=query_result['text'])

    def __get_review(self, entity_id: int, query: str) -> list[Review]:
        result: list[Review] = []
        rows = self.__db.query(query, {"id": entity_id})

        for row in rows:
            result.append(self.__map_to_review(row))

        return result

    def get_product_reviews(self, product_id: int) -> list[Review]:
        return self.__get_review(product_id, self.__GET_PRODUCT_REVIEWS_SQL)

    def get_product_stats(self, product_id: int) -> tuple[int, float]:
        rows = self.__db.query(
            self.__GET_PRODUCT_STATS_SQL, {'id': product_id})
        if len(rows) != 1:
            return 0, 0
        row = rows[0]
        return int(row['review_count']) if (type(row['review_count'])) is not None else 0, float(row['avg_rate']) if type(row['avg_rate']) is not None else 0.0

    def get_user_reviews(self, user_id: int) -> list[Review]:
        return self.__get_review(user_id, self.__GET_USER_REVIEWS_SQL)

    def get_user_stats(self, user_id: int) -> tuple[int, float]:
        rows = self.__db.query(
            self.__GET_USER_STATS_SQL, {'id': user_id})
        if len(rows) != 1:
            return 0, 0
        row = rows[0]
        return int(row['review_count']) if (type(row['review_count'])) is not None else 0, float(
            row['avg_rate']) if type(row['avg_rate']) is not None else 0.0

    def check_if_reviewed(self, user_id: int, product_id: int) -> bool:
        return len(self.__db.query(self.__CHECK_IF_REVIEWED_SQL, {'user_id': user_id, 'product_id': product_id})) > 0
