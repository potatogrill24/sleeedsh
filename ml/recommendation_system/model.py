import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
import pickle
import psycopg2
from psycopg2.extras import RealDictCursor

# Параметры подключения к базе данных
DB_RECOMMEND_CONFIG = {
    "dbname": "internet_shop",  
    "user": "admin",            
    "password": "secretpassword",        
    "host": "localhost",        
    "port": 5433                
}

class RecommendationSystem:
    def __init__(self, data: pd.DataFrame):
        """
        Args:
            data (pd.DataFrame): Dataset containing the data.
        """
        self.data = data
        self.model = None
        self.trainset = None
        self.testset = None

    def load_data(self):
        """
        Prepares the data for training.
        """
        reader = Reader(rating_scale=(1, 5))  # Указываем диапазон оценок (от 1 до 5)
        surprise_data = Dataset.load_from_df(
            self.data[['user_id', 'item_id', 'rating']], reader  # Используем только три столбца
        )
        self.trainset, self.testset = train_test_split(
            surprise_data, test_size=0.25, random_state=42)
        print("Data loaded and split into train and test sets.")
        return self

    def train_model(self):
        """
        Trains the model using KNN for collaborative filtering.
        """
        self.model = KNNBasic(sim_options={'name': 'cosine', 'user_based': False})
        self.model.fit(self.trainset)
        print("Model trained using KNN-based collaborative filtering.")
        return self

    def recommend_items(self, user_id, top_n=10):
        """
        Рекомендует товары на основе оценок пользователя и категорий.
        """
        # Находим товары, которые пользователь оценил высоко
        user_ratings = self.data[self.data['user_id'] == user_id]
        high_rated_items = user_ratings[user_ratings['rating'] >= 3.5]  # Снижаем порог рейтинга

        # Проверяем, есть ли данные для рекомендаций
        if high_rated_items.empty:
            print(f"Пользователь {user_id} не оценил ни одного товара высоко.")
            return []

        # Получаем категории товаров, которые пользователь высоко оценил
        favorite_categories = high_rated_items['category_id'].unique()

        # Фильтруем товары, которые принадлежат любимым категориям пользователя
        items_in_favorite_categories = self.data[self.data['category_id'].isin(favorite_categories)]

        # Получаем рекомендации на основе похожих товаров
        recommendations = []
        for _, row in high_rated_items.iterrows():
            item_id = row['item_id']
            try:
                similar_items = self.model.get_neighbors(self.trainset.to_inner_iid(item_id), k=top_n)  # Увеличиваем k
                for similar_item in similar_items:
                    similar_item_id = self.trainset.to_raw_iid(similar_item)
                    # Проверяем, что товар принадлежит любимой категории
                    if similar_item_id in items_in_favorite_categories['item_id'].values:
                        if similar_item_id not in high_rated_items['item_id'].values and similar_item_id not in [rec[0] for rec in recommendations]:
                            # Используем рейтинг товара как вес
                            item_rating = items_in_favorite_categories[
                                items_in_favorite_categories['item_id'] == similar_item_id
                            ]['rating'].values[0]
                            recommendations.append((similar_item_id, item_rating))  # Добавляем с весом
            except Exception as e:
                print(f"Ошибка при поиске похожих товаров для item_id={item_id}: {e}")

        # Сортируем рекомендации по рейтингу
        recommendations.sort(key=lambda x: x[1], reverse=True)

        # Если рекомендаций недостаточно, добавляем популярные товары
        if len(recommendations) < 7:
            popular_items = self.data[
                (self.data['rating'] >= 4) &
                (~self.data['item_id'].isin([rec[0] for rec in recommendations]))
            ].sort_values(by='rating', ascending=False)['item_id'].unique()
            recommendations.extend([(item, 4) for item in popular_items[:top_n - len(recommendations)]])

        return [item for item, _ in recommendations[:top_n]]

    def save_model(self, file_path):
        """
        Saves the entire RecommendationSystem object to a file.
        """
        if not self.model:
            raise ValueError("Model not trained. Train the model first.")
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)  # Сохраняем весь объект
        print(f"Model saved to {file_path}.")

    def load_model(self, file_path):
        """
        Loads a model from a file.
        """
        with open(file_path, 'rb') as file:
            self.model = pickle.load(file)
        print(f"Model loaded from {file_path}.")


    def load_or_train_model():
        """
        Загружает модель из файла, если она существует, или обучает новую модель.
        """
        try:
            # Попробуйте загрузить предварительно обученную модель
            with open('recommender_model.pkl', 'rb') as file:
                recommendation_system = pickle.load(file)
            print("Model loaded from file.")
        except FileNotFoundError:
            # Если файл не найден, обучите новую модель
            try:
                reviews = pd.read_csv('ratings.csv', sep=',')
            except FileNotFoundError:
                raise FileNotFoundError("Файл ratings.csv не найден. Убедитесь, что он находится в текущей директории.")
            
            # Проверка наличия необходимых столбцов
            required_columns = ['user_id', 'item_id', 'rating', 'category_id']
            if not all(column in reviews.columns for column in required_columns):
                raise ValueError(f"Файл ratings.csv должен содержать столбцы: {required_columns}")
            
            recommendation_system = RecommendationSystem(reviews).load_data().train_model()
            recommendation_system.save_model('recommender_model.pkl')  # Сохраняем модель
            print("Model trained and saved.")
        return recommendation_system


    def save_recommendations_to_db(self, user_id, recommendations):
        """
        Сохраняет рекомендации в таблицу user_recs в базе данных.
        """
        try:
            # Подключаемся к базе данных
            with psycopg2.connect(**DB_RECOMMEND_CONFIG) as conn:
                with conn.cursor() as cur:
                    # Удаляем старые рекомендации для пользователя
                    cur.execute("DELETE FROM user_recs WHERE user_id = %s;", (int(user_id),))
                    
                    # Вставляем новые рекомендации
                    for product_id in recommendations:
                        cur.execute(
                            "INSERT INTO user_recs (user_id, product_id) VALUES (%s, %s);",
                            (int(user_id), int(product_id))  # Преобразуем numpy.int64 в int
                        )
                    conn.commit()  # Фиксируем изменения
            print(f"Рекомендации для пользователя {user_id} успешно сохранены в базу данных.")
        except Exception as e:
            print(f"Ошибка при сохранении рекомендаций в базу данных: {e}")


# def main():
#     # Загружаем или обучаем модель
#     recommendation_system = load_or_train_model()

#     # Генерируем рекомендации для пользователя с user_id = 1
#     user_id = 1
#     recommendations = recommendation_system.recommend_items(user_id, top_n=7)

#     # Выводим рекомендации в консоль
#     print(f"Рекомендации для пользователя с user_id = {user_id}:")
#     for item_id in recommendations:
#         print(f"Рекомендуемый item_id: {item_id}")

#     # Сохраняем рекомендации в базу данных
#     save_recommendations_to_db(user_id, recommendations)


# if __name__ == "__main__":
#     main()