CREATE OR REPLACE PROCEDURE buy_cart(p_user_id INT)
AS $$
DECLARE
    d_paycheck_id INT;
    d_cart_price FLOAT;
    d_user_balance FLOAT;
    d_cart_size INT;
BEGIN
    SELECT COUNT(*) INTO d_cart_size
    FROM public.shopping_carts
    WHERE user_id = p_user_id;

    IF d_cart_size = 0 THEN
        ROLLBACK;
    END IF;

    SELECT COALESCE(SUM(p.price), 0) INTO d_cart_price
    FROM public.products AS p
    JOIN public.shopping_carts AS sc ON sc.product_id = p.id
    WHERE sc.user_id = p_user_id
    GROUP BY sc.user_id;

    IF d_cart_price = 0 THEN
        ROLLBACK;
    END IF;

    SELECT balance INTO d_user_balance
    FROM public.users
    WHERE id = p_user_id;

    IF d_cart_price > d_user_balance THEN
        ROLLBACK;
    END IF;

    INSERT INTO public.paychecks (user_id, total_price)
    VALUES (p_user_id, d_cart_price)
    RETURNING id INTO d_paycheck_id;

    INSERT INTO public.paycheck_items (paycheck_id, product_id)
    SELECT d_paycheck_id, product_id
    FROM public.shopping_carts
    WHERE user_id = p_user_id;

    DELETE FROM public.shopping_carts
    WHERE user_id = p_user_id;

    UPDATE public.users
    SET balance = balance - d_cart_price
    WHERE id = p_user_id;
END;
$$ LANGUAGE PLPGSQL;
