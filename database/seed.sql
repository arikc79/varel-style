-- Тестові товари для розробки
INSERT INTO products (name, category, price, old_price, description, emoji, sizes, badge) VALUES
('Slim-Fit Jeans',     'Джинси',   2890, 3500, 'Класичні чорні джинси зі стрейч-тканини', '👖', ARRAY['28','30','32','34','36','38'], 'Хіт'),
('Regular Denim',      'Джинси',   2590, NULL, 'Класичний синій деним', '👖', ARRAY['30','32','34','36','38'], NULL),
('Oxford Shirt White', 'Сорочки',  1990, 2400, 'Оксфордська сорочка', '👔', ARRAY['S','M','L','XL','XXL'], 'New'),
('Classic Suit',       'Костюми', 12900, 15000,'Класичний двійка', '🤵', ARRAY['46','48','50','52','54'], 'Premium'),
('Leather Jacket',     'Куртки',   8900, 11000,'Шкіряна куртка', '🧥', ARRAY['S','M','L','XL'], 'Premium'),
('Air Max Pro',        'Кросівки', 6500, 7900, 'Кросівки Air Max', '👟', ARRAY['39','40','41','42','43','44','45'], 'New');
