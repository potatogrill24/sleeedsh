import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor

from internal.domain.model import Product, Paycheck

class OptimalPrice:
    def __init__(self, df: pd.DataFrame):
        self.data = df
        self.model = None
        self.data_agg = None
        self.X = None
        self.y = None

    def preprocess(self):
        self.data['date'] = pd.to_datetime(self.data['date'], format='%d.%m.%Y')
        self.data['month'] = self.data['date'].dt.month
        self.data['year'] = self.data['date'].dt.year
        self.data['day_of_week'] = self.data['date'].dt.dayofweek

        items = pd.read_csv('items.csv')

        self.data = pd.merge(self.data, items[['item_id', 'item_category_id']], on='item_id', how='left')

        self.data = self.data[(self.data['item_price'] > 0) & (self.data['item_cnt_day'] > 0)]

        self.data_agg = self.data.groupby(['item_id', 'shop_id']).agg({
            'item_price': 'mean',
            'item_cnt_day': 'sum',
            'month': 'mean',
            'day_of_week': 'mean',
            'item_category_id': 'mean'
        }).reset_index()
        self.data_agg.rename(columns={'item_price': 'avg_item_price', 'item_cnt_day': 'total_sales'}, inplace=True)

        category_dummies = pd.get_dummies(self.data_agg['item_category_id'], prefix='category')
        self.data_agg = pd.concat([self.data_agg, category_dummies], axis=1)

        features = ['avg_item_price', 'month', 'day_of_week'] + list(category_dummies.columns)
        self.X = self.data_agg[features]
        self.y = self.data_agg['total_sales']
        return self

    def fit(self):
        self.model = LGBMRegressor(
            n_estimators=1000,
            learning_rate=0.01,
            reg_alpha=0.2,
            reg_lambda=0.2,
            random_state=42,
            num_leaves=31,
            max_depth=8,
            subsample=0.8,
            colsample_bytree=0.8
        )
        self.model.fit(self.X, self.y)
        return self

    def predict_optimal_price(self, products: list[Product]):
        product_ids = [product.id for product in products]
        all_categories = self.data_agg['item_category_id'].unique()

        optimal_prices = []

        for product_id in product_ids:
            product_data = self.data_agg[self.data_agg['item_id'] == product_id]
            if product_data.empty:
                continue

            avg_price = product_data['avg_item_price'].values[0]
            avg_month = product_data['month'].values[0]
            avg_day_of_week = product_data['day_of_week'].values[0]
            avg_category = product_data['item_category_id'].values[0]

            test_prices = np.linspace(avg_price * 0.9, avg_price * 1.1, num=100)

            test_features = pd.DataFrame({
                'avg_item_price': test_prices,
                'month': np.full_like(test_prices, avg_month),
                'day_of_week': np.full_like(test_prices, avg_day_of_week),
                'item_category_id': np.full_like(test_prices, avg_category)
            })

            for cat in all_categories:
                if f'category_{cat}' not in test_features.columns:
                    test_features[f'category_{cat}'] = 0

            test_features = test_features[self.model.feature_name_]

            predicted_sales = self.model.predict(test_features)

            lambda_penalty = 0.1
            revenues = test_prices * predicted_sales - lambda_penalty * (test_prices - avg_price) ** 2

            optimal_price = test_prices[np.argmax(revenues)]

            optimal_prices.append({
                'product_id': product_id,
                'optimal_price': optimal_price
            })

        return optimal_prices