INSERT INTO public.users (name, login, balance) VALUES
    ('Тестов Тест Тестович', 'test', 0);
INSERT INTO public.user_credentials (user_id, password_hash) VALUES
    (1, '$2b$12$JKwzZeUNNeffTr2ws72QdeojNSPmd/fdML3A/rhiJZssERkecw.9m');
    
INSERT INTO public.shops (name, login) VALUES ('Москва ТРЦ "Метрополис"', 'yakutsk_ordzhonikidze_56_fran_0');
INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (1, '$2b$12$JKwzZeUNNeffTr2ws72QdeojNSPmd/fdML3A/rhiJZssERkecw.9m');
-- INSERT INTO public.shops (name, login) VALUES ('!Якутск ТЦ "Центральный" фран', 'yakutsk_tts_tsentralnyy_fran_1');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (2, '$2b$12$nNRbGbC..uxY2dKCgAi4N.i/cYBqTNQ1Tn5YW7MxldN6opkaMD2s6');
-- INSERT INTO public.shops (name, login) VALUES ('Адыгея ТЦ "Мега"', 'adygeya_tts_mega_2');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (3, '$2b$12$OsfuJ61uV5vEyawLqWYsO.j8Z25khND5rlf.qM2DcoQ8VYB/q4aRq');
-- INSERT INTO public.shops (name, login) VALUES ('Балашиха ТРК "Октябрь-Киномир"', 'balashiha_trk_oktyabr_kinomir_3');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (4, '$2b$12$2kUdpqnDnTtqmuUxMdqDeOKkX.auXHf401YLuGssbHRFsxGK9r7hS');
-- INSERT INTO public.shops (name, login) VALUES ('Волжский ТЦ "Волга Молл"', 'volzhskiy_tts_volga_moll_4');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (5, '$2b$12$0inVIMLpUZsNVVPWAHZnjOFYxf7lE0UDGZ332VL6jkGaf9RnOvp9y');
-- INSERT INTO public.shops (name, login) VALUES ('Вологда ТРЦ "Мармелад"', 'vologda_trts_marmelad_5');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (6, '$2b$12$.bnA/x4BgBsxY1p06I5uu.NX6bbZhUdVMpZGpL3IgbymTVniPvkx.');
-- INSERT INTO public.shops (name, login) VALUES ('Воронеж (Плехановская, 13)', 'voronezh_plehanovskaya_13_6');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (7, '$2b$12$f2R5mr3tsKOc21.BxM6F1ecFdM4Wnf946QYa52YYeI1cJgY08/hTW');
-- INSERT INTO public.shops (name, login) VALUES ('Воронеж ТРЦ "Максимир"', 'voronezh_trts_maksimir_7');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (8, '$2b$12$gnUozAa5KKP6KDvpUTVgFer1aFP1/c3cAugtN7rz5jNVyifKdieOO');
-- INSERT INTO public.shops (name, login) VALUES ('Воронеж ТРЦ Сити-Парк "Град"', 'voronezh_trts_siti_park_grad_8');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (9, '$2b$12$QnHJdtKzqJJO4FagUaiuO.RGil8JvLGQNXm1ycy7feUdAgriKF8Ty');
-- INSERT INTO public.shops (name, login) VALUES ('Выездная Торговля', 'vyezdnaya_torgovlya_9');
-- INSERT INTO public.shop_credentials (shop_id, password_hash) VALUES (10, '$2b$12$MReSUi/nftyGa2gItTl1RuiWGr3BKw9kUvk1RKPiEy5AEZFk9xiSO');


-- Создаем категории (10 разновидностей)
INSERT INTO public.categories (name) VALUES ('Гарнитуры и наушники');
INSERT INTO public.categories (name) VALUES ('Аксессуары для игровых консолей');
INSERT INTO public.categories (name) VALUES ('Игровые консоли');
INSERT INTO public.categories (name) VALUES ('Игры для консолей');
INSERT INTO public.categories (name) VALUES ('Игры для PC');
INSERT INTO public.categories (name) VALUES ('Программное обеспечение');
INSERT INTO public.categories (name) VALUES ('Обучающие программы и курсы');
INSERT INTO public.categories (name) VALUES ('Электроника и гаджеты');
INSERT INTO public.categories (name) VALUES ('Аксессуары для ПК');
INSERT INTO public.categories (name) VALUES ('Цифровой контент и подписки');

-- Гарнитуры и наушники (10 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'HyperX Cloud Alpha S', 8500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'Logitech G Pro X', 12000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'SteelSeries Arctis 7', 13000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'Razer Kraken X', 4500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'Sony WH-1000XM4', 25000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'JBL Quantum 800', 14000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'Corsair HS70 Pro', 9000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'Apple AirPods Max', 60000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'Sennheiser HD 450BT', 12000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (1, 1, 'Bose QuietComfort 35 II', 20000.0);

-- Аксессуары для игровых консолей (8 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'DualShock 4 (PS4)', 4500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'Xbox One Controller', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'Nintendo Switch Pro Controller', 6000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'PS5 DualSense Controller', 7000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'Xbox Series X Controller', 6500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'PS Vita Memory Card 64GB', 8000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'Nintendo Switch Dock', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (2, 1, 'PS4 Charging Station', 2000.0);

-- Игровые консоли (12 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'PlayStation 5', 70000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Xbox Series X', 65000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Nintendo Switch', 30000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'PlayStation 4 Pro', 40000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Xbox One X', 35000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Nintendo Switch Lite', 20000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'PlayStation 3 Slim', 15000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Xbox 360 E', 10000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'PlayStation Vita', 12000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Nintendo 3DS XL', 18000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Sega Genesis Mini', 8000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (3, 1, 'Retro Gaming Console', 5000.0);

-- Игры для консолей (15 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'The Last of Us Part II (PS4)', 4000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Halo Infinite (Xbox Series X)', 4500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'The Legend of Zelda: Breath of the Wild (Switch)', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Spider-Man: Miles Morales (PS5)', 5500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Forza Horizon 5 (Xbox Series X)', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Animal Crossing: New Horizons (Switch)', 4500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'God of War (PS4)', 3500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Gears 5 (Xbox One)', 3000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Mario Kart 8 Deluxe (Switch)', 4000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Final Fantasy VII Remake (PS4)', 4500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'FIFA 23 (PS5)', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Call of Duty: Modern Warfare II (Xbox Series X)', 5500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Super Mario Odyssey (Switch)', 4000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Horizon Forbidden West (PS5)', 6000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (4, 1, 'Metroid Dread (Switch)', 4500.0);

-- Игры для PC (10 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Cyberpunk 2077', 3000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'The Witcher 3: Wild Hunt', 2000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Elden Ring', 4000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Red Dead Redemption 2', 3500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Assassin’s Creed Valhalla', 4500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Call of Duty: Warzone', 0.0); -- Бесплатная игра
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'World of Warcraft: Dragonflight', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Starfield', 6000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Diablo IV', 5500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (5, 1, 'Baldur’s Gate 3', 5000.0);

-- Программное обеспечение (8 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'Microsoft Office 365', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'Adobe Photoshop', 10000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'Windows 11 Pro', 12000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'AutoCAD 2023', 50000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'Final Cut Pro X', 30000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'Visual Studio Code', 0.0); -- Бесплатное ПО
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'Adobe Premiere Pro', 15000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (6, 1, 'Logic Pro X', 20000.0);

-- Обучающие программы и курсы (7 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (7, 1, 'Курс по Python для начинающих', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (7, 1, 'Курс по веб-разработке', 6000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (7, 1, 'Курс по Photoshop', 4000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (7, 1, 'Курс по Unity для разработчиков игр', 7000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (7, 1, 'Курс по Data Science', 8000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (7, 1, 'Курс по английскому языку', 3000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (7, 1, 'Курс по цифровому маркетингу', 4500.0);

-- Электроника и гаджеты (10 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Apple Watch Series 8', 30000.0); 
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Samsung Galaxy Tab S8', 50000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'DJI Mavic Air 2', 80000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'GoPro Hero 11', 40000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Amazon Echo Dot', 5000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Xiaomi Mi Band 7', 3000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Raspberry Pi 4', 6000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Kindle Paperwhite', 10000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Logitech MX Master 3S', 12000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (8, 1, 'Anker PowerCore 20000', 5000.0);

-- Аксессуары для ПК (10 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Клавиатура Logitech G Pro', 10000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Мышь Razer DeathAdder V2', 6000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Коврик для мыши SteelSeries QcK', 2000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Монитор Dell UltraSharp 27', 40000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Внешний жесткий диск Seagate 2TB', 6000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'SSD Samsung 970 EVO 1TB', 10000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Webcam Logitech C920', 8000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Колонки Creative Pebble', 3000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'ИБП APC Back-UPS 1100VA', 15000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (9, 1, 'Кабель HDMI 2.1', 2000.0);

-- Цифровой контент и подписки (10 товаров)
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Подписка на Netflix (1 месяц)', 1000.0); 
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Подписка на Spotify Premium (1 месяц)', 500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Подписка на Xbox Game Pass Ultimate', 1500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Подписка на PlayStation Plus', 2000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Ключ активации Steam (50$)', 4000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Ключ активации Origin (25$)', 2000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Электронная книга "Война и мир"', 500.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Аудиокнига "Гарри Поттер и Философский камень"', 1000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Курс по программированию на Udemy', 3000.0);
INSERT INTO public.products (category_id, shop_id, name, price) VALUES (10, 1, 'Подписка на YouTube Premium (1 месяц)', 700.0);

-- -- Сделаем тестовые рекомендации
-- INSERT INTO user_recs (user_id, product_id) VALUES (1, 1), (1, 2), (1, 3);
