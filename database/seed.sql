-- Тестові дані для розробки
-- Запускати ПІСЛЯ schema.sql та django migrate

-- Категорії
INSERT INTO products_category (name, emoji, "order") VALUES
  ('Джинси',   '👖', 0),
  ('Сорочки',  '👔', 1),
  ('Костюми',  '🤵', 2),
  ('Спорт',    '🏃', 3),
  ('Куртки',   '🧥', 4),
  ('Кросівки', '👟', 5)
ON CONFLICT (name) DO NOTHING;

-- Товари (category_id через підзапит)
INSERT INTO products_product (category_id, name, price, old_price, description, emoji, sizes, badge) VALUES
(
  (SELECT id FROM products_category WHERE name='Джинси'),
  'Slim-Fit Jeans', 2890, 3500,
  'Класичні чорні джинси зі стрейч-тканини',
  '👖', '["28","30","32","34","36","38"]', 'Хіт'
),
(
  (SELECT id FROM products_category WHERE name='Джинси'),
  'Regular Denim', 2590, NULL,
  'Класичний синій деним',
  '👖', '["30","32","34","36","38"]', ''
),
(
  (SELECT id FROM products_category WHERE name='Сорочки'),
  'Oxford Shirt White', 1990, 2400,
  'Оксфордська сорочка',
  '👔', '["S","M","L","XL","XXL"]', 'New'
),
(
  (SELECT id FROM products_category WHERE name='Костюми'),
  'Classic Suit', 12900, 15000,
  'Класичний двійка',
  '🤵', '["46","48","50","52","54"]', 'Premium'
),
(
  (SELECT id FROM products_category WHERE name='Куртки'),
  'Leather Jacket', 8900, 11000,
  'Шкіряна куртка',
  '🧥', '["S","M","L","XL"]', 'Premium'
),
(
  (SELECT id FROM products_category WHERE name='Кросівки'),
  'Air Max Pro', 6500, 7900,
  'Кросівки Air Max',
  '👟', '["39","40","41","42","43","44","45"]', 'New'
);
