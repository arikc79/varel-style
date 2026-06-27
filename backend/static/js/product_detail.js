// ── СТОРІНКА ДЕТАЛЬНОГО ПЕРЕГЛЯДУ ТОВАРУ ──
let pdProduct  = null;
let pdQty      = 1;
let pdSize     = null;
let pdImgIndex = 0;

// ── Завантажити товар з API ──
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

// ── Рендер сторінки ──
function renderProductDetail() {
  const p = pdProduct;
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
      // Ховаємо кнопки навігації, якщо фото одне
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

// ── Кількість ──
function pdChangeQty(dir) {
  pdQty = Math.max(1, pdQty + dir);
  document.getElementById('pdQtyNum').textContent = pdQty;
}

// ── Додати до кошика ──
function pdAddToCart() {
  if (!pdSize) { showToast('⚠️ Оберіть розмір!'); return; }
  for (let i = 0; i < pdQty; i++) addItem(pdProduct, pdSize);
  showToast('✓ Додано: ' + pdProduct.name);
}

// ── Старт ──
loadProductDetail();

