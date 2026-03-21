// ── МОДАЛЬНЕ ВІКНО ТОВАРУ ──
let currentProduct = null;
let currentQty = 1;
let selectedSize = null;

function openModal(id) {
  currentProduct = products.find(p => p.id === id);
  if (!currentProduct) return;

  currentQty = 1;
  selectedSize = null;

  document.getElementById('qtyNum').textContent = 1;
  document.getElementById('modalImg').textContent = currentProduct.emoji;
  document.getElementById('modalCat').textContent = currentProduct.cat;
  document.getElementById('modalName').textContent = currentProduct.name;
  document.getElementById('modalDesc').textContent = currentProduct.desc;

  const oldPriceHTML = currentProduct.oldPrice
    ? `<span style="font-size:16px;color:#888;text-decoration:line-through;margin-right:8px">${currentProduct.oldPrice.toLocaleString()} ₴</span>`
    : '';
  document.getElementById('modalPrice').innerHTML = oldPriceHTML + currentProduct.price.toLocaleString() + ' ₴';

  document.getElementById('modalSizes').innerHTML = currentProduct.sizes
    .map(s => `<button class="size-btn" onclick="selectSize(this,'${s}')">${s}</button>`)
    .join('');

  document.getElementById('modalDetails').innerHTML =
    '<div class="size-label" style="margin-bottom:12px">Деталі товару</div>' +
    Object.entries(currentProduct.details)
      .map(([k, v]) => `<div class="modal-detail-row"><span class="modal-detail-key">${k}</span><span class="modal-detail-val">${v}</span></div>`)
      .join('');

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
  if (!selectedSize) {
    showToast('⚠️ Оберіть розмір!');
    return;
  }
  for (let i = 0; i < currentQty; i++) {
    addItem(currentProduct, selectedSize);
  }
  closeModal();
  showToast('✓ Додано: ' + currentProduct.name);
}

