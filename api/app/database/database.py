ORDERS_DDL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    items_count INTEGER NOT NULL CHECK (items_count > 0),
    status VARCHAR(20) NOT NULL DEFAULT 'NEW' CHECK
            (status IN ('NEW', 'PROCESSING', 'DONE')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);
"""
