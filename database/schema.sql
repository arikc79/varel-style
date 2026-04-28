-- Схема бази даних VAREL style
-- Відповідає Django-моделям (apps/products, apps/orders)
-- Виконати в Supabase SQL Editor або psql

-- ── Категорії ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products_category (
  id      BIGSERIAL    PRIMARY KEY,
  name    VARCHAR(100) NOT NULL UNIQUE,
  emoji   VARCHAR(10)  NOT NULL DEFAULT '👔',
  "order" SMALLINT     NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_category_order ON products_category("order", name);

-- ── Товари ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products_product (
  id          BIGSERIAL    PRIMARY KEY,
  category_id BIGINT       REFERENCES products_category(id) ON DELETE SET NULL,
  name        VARCHAR(255) NOT NULL,
  price       INTEGER      NOT NULL CHECK (price >= 0),
  old_price   INTEGER               CHECK (old_price >= 0),
  description TEXT         NOT NULL,
  emoji       VARCHAR(10)  NOT NULL DEFAULT '👔',
  sizes       JSONB        NOT NULL DEFAULT '[]',
  details     JSONB        NOT NULL DEFAULT '{}',
  badge       VARCHAR(50)  NOT NULL DEFAULT '',
  in_stock    BOOLEAN      NOT NULL DEFAULT true,
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_category ON products_product(category_id);
CREATE INDEX IF NOT EXISTS idx_product_in_stock ON products_product(in_stock);
CREATE INDEX IF NOT EXISTS idx_product_created  ON products_product(created_at DESC);

-- ── Фото товарів ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products_productimage (
  id         BIGSERIAL    PRIMARY KEY,
  product_id BIGINT       NOT NULL REFERENCES products_product(id) ON DELETE CASCADE,
  image      VARCHAR(100) NOT NULL,
  "order"    SMALLINT     NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_productimage_product ON products_productimage(product_id, "order");

-- ── Замовлення ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders_order (
  id            BIGSERIAL    PRIMARY KEY,
  first_name    VARCHAR(100) NOT NULL,
  last_name     VARCHAR(100) NOT NULL DEFAULT '',
  phone         VARCHAR(20)  NOT NULL,
  email         VARCHAR(254) NOT NULL DEFAULT '',
  delivery_type VARCHAR(10)  NOT NULL CHECK (delivery_type IN ('nova','ukr')),
  city          VARCHAR(100) NOT NULL DEFAULT '',
  branch        VARCHAR(255) NOT NULL DEFAULT '',
  payment_type  VARCHAR(10)  NOT NULL CHECK (payment_type IN ('card','cash')),
  total         INTEGER      NOT NULL CHECK (total >= 0),
  status        VARCHAR(20)  NOT NULL DEFAULT 'new'
                             CHECK (status IN ('new','processing','shipped','done')),
  created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_order_status  ON orders_order(status);
CREATE INDEX IF NOT EXISTS idx_order_created ON orders_order(created_at DESC);

-- ── Позиції замовлення ───────────────────────────────────
CREATE TABLE IF NOT EXISTS orders_orderitem (
  id         BIGSERIAL    PRIMARY KEY,
  order_id   BIGINT       NOT NULL REFERENCES orders_order(id)    ON DELETE CASCADE,
  product_id BIGINT                REFERENCES products_product(id) ON DELETE SET NULL,
  name       VARCHAR(255) NOT NULL,
  price      INTEGER      NOT NULL CHECK (price >= 0),
  size       VARCHAR(10)  NOT NULL,
  qty        INTEGER      NOT NULL DEFAULT 1 CHECK (qty >= 1)
);

CREATE INDEX IF NOT EXISTS idx_orderitem_order   ON orders_orderitem(order_id);
CREATE INDEX IF NOT EXISTS idx_orderitem_product ON orders_orderitem(product_id);
