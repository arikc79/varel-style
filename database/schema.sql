-- Схема бази даних VAREL style
-- Виконати в Supabase SQL Editor

-- Таблиця товарів
CREATE TABLE products (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  category    VARCHAR(100) NOT NULL,
  price       INTEGER NOT NULL,
  old_price   INTEGER,
  description TEXT,
  emoji       VARCHAR(10),
  sizes       TEXT[],
  badge       VARCHAR(50),
  in_stock    BOOLEAN DEFAULT true,
  created_at  TIMESTAMP DEFAULT NOW()
);

-- Таблиця замовлень
CREATE TABLE orders (
  id            SERIAL PRIMARY KEY,
  first_name    VARCHAR(100) NOT NULL,
  last_name     VARCHAR(100),
  phone         VARCHAR(20) NOT NULL,
  email         VARCHAR(255),
  delivery_type VARCHAR(20) NOT NULL,  -- 'nova' | 'ukr'
  city          VARCHAR(100),
  branch        VARCHAR(255),
  payment_type  VARCHAR(20) NOT NULL,  -- 'card' | 'cash'
  total         INTEGER NOT NULL,
  status        VARCHAR(50) DEFAULT 'new',  -- new | processing | shipped | done
  created_at    TIMESTAMP DEFAULT NOW()
);

-- Позиції замовлення
CREATE TABLE order_items (
  id         SERIAL PRIMARY KEY,
  order_id   INTEGER REFERENCES orders(id),
  product_id INTEGER REFERENCES products(id),
  name       VARCHAR(255),
  price      INTEGER,
  size       VARCHAR(10),
  qty        INTEGER DEFAULT 1
);

-- Індекси
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order ON order_items(order_id);
