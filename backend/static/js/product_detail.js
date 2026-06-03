// ── СТОРІНКА ДЕТАЛЬНОГО ПЕРЕГЛЯДУ ТОВАРУ ──
let pdProduct  = null;
let pdQty      = 1;
let pdSize     = null;
let pdColor    = null;
let pdImgIndex = 0;

const PD_COLOR_MAP = {
  // нижній регістр → HEX
  'білий':      '#f5f5f0',
  'чорний':     '#1a1a1a',
  'синій':      '#1e3f8f',
  'темно-синій':'#0d1f5c',
  'блакитний':  '#5fa8e8',
  'бежевий':    '#d9d0ba',
  'молочний':   '#f0ead6',
  'сірий':      '#8a8a8a',
  'графіт':     '#3a3d45',
  'хакі':       '#7a7d5e',
  'зелений':    '#266b48',
  'червоний':   '#c0273a',
  'бордовий':   '#681a28',
  'коричневий': '#6b472e',
  // Великий регістр (на всяк)
  'Білий':      '#f5f5f0',
  'Чорний':     '#1a1a1a',
  'Синій':      '#1e3f8f',
  'Темно-синій':'#0d1f5c',
  'Блакитний':  '#5fa8e8',
  'Бежевий':    '#d9d0ba',
  'Молочний':   '#f0ead6',
  'Сірий':      '#8a8a8a',
  'Графіт':     '#3a3d45',
  'Хакі':       '#7a7d5e',
  'Зелений':    '#266b48',
  'Червоний':   '#c0273a',
  'Бордовий':   '#681a28',
  'Коричневий': '#6b472e',
};


async function loadProductDetail() {
  try {
    const res = await fetch(`/api/products/${PRODUCT_ID}/`);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    pdProduct = await res.json();
    renderProductDetail();
  } catch (e) {
    document.getElementById('pdLoading').style.display  = 'none';
    document.getElementById('pdNotFound').style.display = 'flex';
    console.error('Деталь товару:', e);
  }
}

// ── Рендер  ──
function renderProductDetail() {
  const p = pdProduct;
  pdColor = null;
  document.title = `${p.name} — VAREL`;

  document.getElementById('pdLoading').style.display   = 'none';
  document.getElementById('pdContainer').style.display = 'flex';

  // ── Галерея ──
  const track  = document.getElementById('pdTrack');
  const thumbs = document.getElementById('pdThumbs');
  const imgs   = p.images || [];

  if (imgs.length > 0) {
    track.innerHTML = imgs.map(img =>
      `<img src="${img.image_url}" alt="${p.name}">`
    ).join('');

    thumbs.innerHTML = imgs.map((img, i) =>
      `<img src="${img.image_url}" alt="${p.name} ${i+1}"
            class="pd-thumb ${i === 0 ? 'active' : ''}"
            onclick="pdGoTo(${i})">`
    ).join('');

    if (imgs.length === 1) {
      // Ховаємо кнопки навігації
      document.querySelector('.pd-prev').style.display = 'none';
      document.querySelector('.pd-next').style.display = 'none';
      thumbs.style.display = 'none';
    }
  } else {
    track.innerHTML = `<div class="pd-emoji-placeholder">${p.emoji}</div>`;
    thumbs.style.display = 'none';
    document.querySelector('.pd-prev').style.display = 'none';
    document.querySelector('.pd-next').style.display = 'none';
  }

  // ── Назва, категорія, ціна ──
  document.getElementById('pdCat').textContent  = p.category || '';
  document.getElementById('pdName').textContent = p.name;
  document.getElementById('pdDesc').textContent = p.description;

  const oldHtml = p.old_price
    ? `<span class="pd-old-price">${p.old_price.toLocaleString('uk-UA')} ₴</span>`
    : '';
  document.getElementById('pdPrice').innerHTML =
    oldHtml + `<span class="pd-new-price">${p.price.toLocaleString('uk-UA')} ₴</span>`;

  // ── Розміри ──
  document.getElementById('pdSizes').innerHTML = (p.sizes || []).map(s =>
    `<button class="pd-size-btn" onclick="pdSelectSize(this,'${s}')">${s}</button>`
  ).join('');

  // ── Кольори ──
  const colorsContainer = document.getElementById('pdColors');
  const colorLabel      = document.getElementById('pdColorLabel');
  if (p.colors && p.colors.length > 0) {
    if (colorLabel) colorLabel.style.display = '';
    colorsContainer.style.display = 'flex';
    colorsContainer.innerHTML = p.colors.map(c => {
      const colorName  = String(c).trim();
      const colorValue = pdResolveColor(colorName);
      return `<button class="pd-color-btn" type="button" title="${pdEscapeHtml(colorName)}" data-color="${pdEscapeHtml(colorName)}" style="background:${colorValue}"></button>`;
    }).join('');
    colorsContainer.querySelectorAll('.pd-color-btn').forEach(btn => {
      btn.addEventListener('click', () => pdSelectColor(btn, btn.dataset.color || ''));
    });
  } else {
    if (colorLabel) colorLabel.style.display = 'none';
    colorsContainer.style.display = 'none';
  }
  pdUpdateColorLabel();

  // ── Деталі товару ──
  const details = p.details || {};
  document.getElementById('pdDetails').innerHTML = Object.keys(details).length
    ? '<div class="pd-detail-title">Деталі товару</div>' +
      Object.entries(details).map(([k, v]) =>
        `<div class="pd-detail-row"><span>${k}</span><span>${v}</span></div>`
      ).join('')
    : '';

  // ── Touch swipe на галереї ──
  initPdSwipe();
}

// ── Карусель: навігація ──
function pdNav(dir) {
  const track = document.getElementById('pdTrack');
  if (!track || track.children.length <= 1) return;
  const count = track.children.length;
  pdImgIndex  = (pdImgIndex + dir + count) % count;
  pdUpdateCarousel();
}

function pdGoTo(i) {
  pdImgIndex = i;
  pdUpdateCarousel();
}

function pdUpdateCarousel() {
  document.getElementById('pdTrack').style.transform = `translateX(-${pdImgIndex * 100}%)`;
  document.querySelectorAll('.pd-thumb').forEach((t, i) => {
    t.classList.toggle('active', i === pdImgIndex);
  });
}

// ── Touch swipe ──
function initPdSwipe() {
  const vp = document.querySelector('.pd-viewport');
  if (!vp) return;
  let sx = 0;
  vp.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
  vp.addEventListener('touchend',   e => {
    const diff = sx - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) pdNav(diff > 0 ? 1 : -1);
  });
}

// ── Розмір ──
function pdSelectSize(btn, size) {
  document.querySelectorAll('.pd-size-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  pdSize = size;
}

// ── Колір ──
function pdSelectColor(btn, color) {
  document.querySelectorAll('.pd-color-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  pdColor = color;
  pdUpdateColorLabel();
}

// ── Кількість ──
function pdChangeQty(dir) {
  pdQty = Math.max(1, pdQty + dir);
  document.getElementById('pdQtyNum').textContent = pdQty;
}

// ── Додати до кошика ──
function pdAddToCart() {
  if (!pdSize) { showToast('⚠️ Оберіть розмір!'); return; }
  if ((pdProduct.colors || []).length && !pdColor) { showToast('⚠️ Оберіть колір!'); return; }
  const color = pdColor || 'Без кольору';
  for (let i = 0; i < pdQty; i++) addItem(pdProduct, pdSize, color);
  showToast('✓ Додано: ' + pdProduct.name);
}

// ── Старт ──
loadProductDetail();

function pdResolveColor(colorName) {
  const raw = String(colorName || '').trim();
  if (!raw) return '#888';

  // Пряме HEX значення з API
  if (/^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(raw)) return raw;

  // Точний збіг
  if (PD_COLOR_MAP[raw]) return PD_COLOR_MAP[raw];

  // Fallback: нижній регістр
  const lower = raw.toLowerCase();
  return PD_COLOR_MAP[lower] || '#888';
}

function pdUpdateColorLabel() {
  const label = document.getElementById('pdColorLabel');
  if (!label) return;
  label.textContent = pdColor ? `Оберіть колір: ${pdColor}` : 'Оберіть колір';
}

function pdEscapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

