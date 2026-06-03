// ── МОДАЛЬНЕ ВІКНО ТОВАРУ ──
let currentProduct  = null;
let currentQty      = 1;
let selectedSize    = null;
let selectedColor   = null;

const MODAL_COLOR_MAP = {
  'білий':'#f5f5f0','чорний':'#1a1a1a','синій':'#1e3f8f','темно-синій':'#0d1f5c',
  'блакитний':'#5fa8e8','бежевий':'#d9d0ba','молочний':'#f0ead6','сірий':'#8a8a8a',
  'графіт':'#3a3d45','хакі':'#7a7d5e','зелений':'#266b48','червоний':'#c0273a',
  'бордовий':'#681a28','коричневий':'#6b472e',
};

function openModal(id) {
  currentProduct = allProducts.find(p => p.id === id);
  if (!currentProduct) return;

  currentQty    = 1;
  selectedSize  = null;
  selectedColor = null;
  document.getElementById('qtyNum').textContent = 1;

  // ── Галерея фото або emoji ──
  const imgBox = document.getElementById('modalImg');
  if (currentProduct.images && currentProduct.images.length > 0) {
    const imgs = currentProduct.images;
    imgBox.innerHTML = `
      <div class="modal-gallery">
        <div class="modal-gallery-main">
          <img id="modalMainImg" src="${imgs[0].image_url}" alt="${currentProduct.name}">
        </div>
        ${imgs.length > 1 ? `
        <div class="modal-gallery-thumbs">
          ${imgs.map((img, i) => `
            <img src="${img.image_url}" alt="${currentProduct.name} фото ${i + 1}"
              class="modal-thumb ${i === 0 ? 'active' : ''}"
              onclick="setModalMainImg(this, '${img.image_url}')">
          `).join('')}
        </div>` : ''}
      </div>`;
  } else {
    imgBox.innerHTML = `<span style="font-size:80px">${currentProduct.emoji}</span>`;
  }

  document.getElementById('modalCat').textContent  = currentProduct.category;
  document.getElementById('modalName').textContent = currentProduct.name;
  document.getElementById('modalDesc').textContent = currentProduct.description;

  const oldPriceHTML = currentProduct.old_price
    ? `<span style="font-size:16px;color:#888;text-decoration:line-through;margin-right:8px">
         ${currentProduct.old_price.toLocaleString('uk-UA')} ₴
       </span>`
    : '';
  document.getElementById('modalPrice').innerHTML =
    oldPriceHTML + currentProduct.price.toLocaleString('uk-UA') + ' ₴';

  document.getElementById('modalSizes').innerHTML = currentProduct.sizes
    .map(s => `<button class="size-btn" onclick="selectSize(this,'${s}')">${s}</button>`)
    .join('');

  const colors = currentProduct.colors || [];
  const colorLabel = document.getElementById('modalColorLabel');
  const colorsBox  = document.getElementById('modalColors');
  if (colors.length > 0) {
    colorLabel.style.display = '';
    colorsBox.innerHTML = colors.map(c => {
      const name = String(c).trim();
      const hex  = MODAL_COLOR_MAP[name.toLowerCase()] || '#888';
      return `<button class="modal-color-swatch" title="${name}" data-color="${name}"
        style="width:32px;height:32px;border-radius:50%;background:${hex};border:2px solid rgba(255,255,255,.2);
        outline:2px solid transparent;outline-offset:2px;cursor:pointer;transition:all .2s;flex-shrink:0;"
        onclick="selectModalColor(this,'${name}')"></button>`;
    }).join('');
  } else {
    colorLabel.style.display = 'none';
    colorsBox.innerHTML = '';
  }

  const details = currentProduct.details || {};
  document.getElementById('modalDetails').innerHTML = Object.keys(details).length
    ? '<div class="size-label" style="margin-bottom:12px">Деталі товару</div>' +
      Object.entries(details).map(([k, v]) => `
        <div class="modal-detail-row">
          <span class="modal-detail-key">${k}</span>
          <span class="modal-detail-val">${v}</span>
        </div>`).join('')
    : '';

  document.getElementById('productModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function setModalMainImg(thumb, url) {
  document.getElementById('modalMainImg').src = url;
  document.querySelectorAll('.modal-thumb').forEach(t => t.classList.remove('active'));
  thumb.classList.add('active');
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

function selectModalColor(btn, color) {
  document.querySelectorAll('.modal-color-swatch').forEach(b => {
    b.style.outlineColor = 'transparent';
    b.style.borderColor  = 'rgba(255,255,255,.2)';
  });
  btn.style.outlineColor = 'var(--gold)';
  btn.style.borderColor  = 'rgba(201,168,76,.8)';
  selectedColor = color;
}

function addToCartFromModal() {
  if (!selectedSize) { showToast('⚠️ Оберіть розмір!'); return; }
  const colors = currentProduct.colors || [];
  if (colors.length > 0 && !selectedColor) { showToast('⚠️ Оберіть колір!'); return; }
  const color = selectedColor || 'Без кольору';
  for (let i = 0; i < currentQty; i++) addItem(currentProduct, selectedSize, color);
  closeModal();
  showToast('✓ Додано: ' + currentProduct.name);
}
