// ── ДАНІ ТОВАРІВ ──
// TODO: замінити на fetch() з API коли бекенд буде готовий
// // Буде замість статичного масиву:
      //const res = await fetch('/api/products')
      //const products = await res.json()



const products = [
  { id:1, name:'Slim-Fit Jeans', cat:'Джинси', emoji:'👖', price:2890, oldPrice:3500,
    desc:'Класичні чорні джинси зі стрейч-тканини. Ідеальна посадка на кожен день.',
    sizes:['28','30','32','34','36','38'],
    details:{Склад:'98% Бавовна, 2% Еластан', Країна:'Туреччина', Посадка:'Slim Fit', Колір:'Чорний'},
    badge:'Хіт' },
  { id:2, name:'Regular Denim', cat:'Джинси', emoji:'👖', price:2590,
    desc:'Класичний синій деним. Прямий крій, міцна тканина.',
    sizes:['30','32','34','36','38'],
    details:{Склад:'100% Бавовна', Країна:'Туреччина', Посадка:'Regular Fit', Колір:'Синій'} },
  { id:3, name:'Oxford Shirt White', cat:'Сорочки', emoji:'👔', price:1990, oldPrice:2400,
    desc:'Класична оксфордська сорочка. Ідеальна для офісу та вечора.',
    sizes:['S','M','L','XL','XXL'],
    details:{Склад:'100% Бавовна', Країна:'Італія', Крій:'Slim', Колір:'Білий'},
    badge:'New' },
  { id:4, name:'Linen Shirt Black', cat:'Сорочки', emoji:'👔', price:2290,
    desc:'Льняна сорочка. Легка, дихаюча, ідеальна для теплого сезону.',
    sizes:['S','M','L','XL'],
    details:{Склад:'100% Льон', Країна:'Португалія', Крій:'Regular', Колір:'Чорний'} },
  { id:5, name:'Classic Suit Charcoal', cat:'Костюми', emoji:'🤵', price:12900, oldPrice:15000,
    desc:'Класичний двійка. Вовняна тканина, ідеальний крій.',
    sizes:['46','48','50','52','54'],
    details:{Склад:'70% Вовна, 30% Поліестер', Країна:'Польща', Тип:'Двійка', Колір:'Антрацит'},
    badge:'Premium' },
  { id:6, name:'Navy Blue Suit', cat:'Костюми', emoji:'🤵', price:11500,
    desc:'Темно-синій костюм — класика преміум-класу.',
    sizes:['46','48','50','52'],
    details:{Склад:'65% Вовна, 35% Поліестер', Країна:'Польща', Тип:'Двійка', Колір:'Темно-синій'} },
  { id:7, name:'Sport Suit Track', cat:'Спорт', emoji:'🏃', price:4900, oldPrice:5800,
    desc:'Стильний спортивний костюм. Дихаюча тканина.',
    sizes:['S','M','L','XL','XXL'],
    details:{Склад:'80% Поліестер, 20% Бавовна', Країна:'Туреччина', Тип:'Брюки + Худі', Колір:'Чорний'},
    badge:'Sale' },
  { id:8, name:'Jogger Set Grey', cat:'Спорт', emoji:'🏃', price:3900,
    desc:'Джоггер-сет у сірому кольорі. Мінімалістичний дизайн.',
    sizes:['S','M','L','XL'],
    details:{Склад:'75% Бавовна, 25% Поліестер', Країна:'Туреччина', Тип:'Брюки + Толстовка', Колір:'Сірий'} },
  { id:9, name:'Leather Jacket Black', cat:'Куртки', emoji:'🧥', price:8900, oldPrice:11000,
    desc:'Шкіряна куртка — вічна класика. Натуральна шкіра.',
    sizes:['S','M','L','XL'],
    details:{Склад:'100% Натуральна шкіра', Країна:'Іспанія', Тип:'Косуха', Колір:'Чорний'},
    badge:'Premium' },
  { id:10, name:'Bomber Olive', cat:'Куртки', emoji:'🧥', price:5900,
    desc:'Бомбер в кольорі олива. Сучасний фасон, тепла підкладка.',
    sizes:['S','M','L','XL','XXL'],
    details:{Склад:'Поліестер, Нейлон', Країна:'Туреччина', Тип:'Бомбер', Колір:'Олива'} },
  { id:11, name:'Air Max Pro', cat:'Кросівки', emoji:'👟', price:6500, oldPrice:7900,
    desc:"Преміальні кросівки Air Max. Легкі, дихаючі.",
    sizes:['39','40','41','42','43','44','45'],
    details:{Матеріал:'Сітка + шкіра', Підошва:'Гума Air', Країна:"В'єтнам", Колір:'Білий/Чорний'},
    badge:'New' },
  { id:12, name:'Suede Sneaker White', cat:'Кросівки', emoji:'👟', price:5200,
    desc:'Замшеві кросівки. Простота та елегантність.',
    sizes:['40','41','42','43','44'],
    details:{Матеріал:'Натуральна замша', Підошва:'Гума', Країна:'Португалія', Колір:'Білий'} },
];

// ── РЕНДЕР ТОВАРІВ ──
function renderProducts(filter) {
  filter = filter || 'all';
  const grid = document.getElementById('productsGrid');
  const filtered = filter === 'all' ? products : products.filter(p => p.cat === filter);
  grid.innerHTML = filtered.map(p => `
    <div class="product-card fade-in" onclick="openModal(${p.id})">
      <div class="product-img">
        <span>${p.emoji}</span>
        ${p.badge ? `<div class="product-badge">${p.badge}</div>` : ''}
      </div>
      <div class="product-info">
        <div class="product-cat">${p.cat}</div>
        <div class="product-name">${p.name}</div>
        <div class="product-desc">${p.desc.substring(0,80)}...</div>
        <div class="product-footer">
          <div class="product-price">
            ${p.oldPrice ? `<span>${p.oldPrice.toLocaleString()} ₴</span>` : ''}
            ${p.price.toLocaleString()} ₴
          </div>
          <button class="add-cart-btn" onclick="event.stopPropagation();quickAdd(${p.id})">+ Кошик</button>
        </div>
      </div>
    </div>`).join('');
  observeFadeIns();
}

// ── ФІЛЬТР (з кнопок) ──
function filterProducts(cat, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderProducts(cat);
}

// ── ПЕРЕХІД З КАТЕГОРІЙ ──
function goToProducts(cat) {
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.remove('active');
    if (b.textContent.trim() === cat) b.classList.add('active');
  });
  renderProducts(cat);
  document.getElementById('products').scrollIntoView({behavior:'smooth'});
}

// ── МОДАЛЬНЕ ВІКНО ──
let currentProduct = null;
let currentQty = 1;
let selectedSize = null;

function openModal(id) {
  currentProduct = products.find(p => p.id === id);
  currentQty = 1; selectedSize = null;
  document.getElementById('qtyNum').textContent = 1;
  document.getElementById('modalImg').textContent = currentProduct.emoji;
  document.getElementById('modalCat').textContent = currentProduct.cat;
  document.getElementById('modalName').textContent = currentProduct.name;
  document.getElementById('modalDesc').textContent = currentProduct.desc;
  document.getElementById('modalPrice').innerHTML =
    (currentProduct.oldPrice
      ? `<span style="font-size:16px;color:#888;text-decoration:line-through;margin-right:8px">${currentProduct.oldPrice.toLocaleString()} ₴</span>`
      : '') + currentProduct.price.toLocaleString() + ' ₴';
  document.getElementById('modalSizes').innerHTML = currentProduct.sizes
    .map(s => `<button class="size-btn" onclick="selectSize(this,'${s}')">${s}</button>`).join('');
  document.getElementById('modalDetails').innerHTML =
    '<div class="size-label" style="margin-bottom:12px">Деталі товару</div>' +
    Object.entries(currentProduct.details)
      .map(([k,v]) => `<div class="modal-detail-row"><span class="modal-detail-key">${k}</span><span class="modal-detail-val">${v}</span></div>`).join('');
  document.getElementById('productModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('productModal').classList.remove('open');
  document.body.style.overflow = '';
}

function selectSize(btn, size) {
  document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  selectedSize = size;
}

function changeQty(d) {
  currentQty = Math.max(1, currentQty + d);
  document.getElementById('qtyNum').textContent = currentQty;
}

function addToCartFromModal() {
  if (!selectedSize) { showToast('Оберіть розмір!'); return; }
  for (let i = 0; i < currentQty; i++) addItem(currentProduct, selectedSize);
  closeModal();
  showToast('✓ Додано: ' + currentProduct.name);
}

function quickAdd(id) {
  const p = products.find(x => x.id === id);
  addItem(p, p.sizes[0]);
  showToast('✓ ' + p.name + ' — додано до кошика');
}

// Старт
renderProducts('all');
