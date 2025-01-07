DROP TABLE IF EXISTS public.shop_credentials CASCADE;
DROP TABLE IF EXISTS public.shops CASCADE;
DROP TABLE IF EXISTS public.user_credentials CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.categories CASCADE;
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.paychecks CASCADE;
DROP TABLE IF EXISTS public.paycheck_items CASCADE;
DROP TABLE IF EXISTS public.shopping_carts CASCADE;
DROP TABLE IF EXISTS public.reviews CASCADE;

CREATE TABLE public.shops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    login VARCHAR(256) NOT NULL UNIQUE
);

CREATE TABLE public.shop_credentials (
    id SERIAL PRIMARY KEY,
    shop_id INT REFERENCES public.shops(id) ON DELETE CASCADE,
    password_hash VARCHAR(70) NOT NULL
);

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    login VARCHAR (256) NOT NULL UNIQUE,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0 CHECK (balance >= 0)
);

CREATE TABLE public.user_credentials (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES public.users(id) ON DELETE CASCADE,
    password_hash VARCHAR(70) NOT NULL
);

CREATE TABLE public.categories (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE public.products (
    id SERIAL PRIMARY KEY NOT NULL,
    category_id INT REFERENCES public.categories(id) ON DELETE SET NULL,
    shop_id INT REFERENCES public.shops(id) ON DELETE SET NULL,
    name VARCHAR(256) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE public.paychecks (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE CASCADE,
    total_price DECIMAL(10, 2) NOT NULL DEFAULT 0,
    creation_time TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.paycheck_items (
    id SERIAL PRIMARY KEY NOT NULL,
    paycheck_id INT REFERENCES public.paychecks(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL
);

CREATE TABLE public.shopping_carts (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL
);

CREATE TABLE public.reviews (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL,
    rate DECIMAL(10, 2) NOT NULL,
    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
    text TEXT NOT NULL DEFAULT ''
);

CREATE TABLE public.user_recs (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL
);