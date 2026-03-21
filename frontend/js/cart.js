// ── КОШИК ──
let cart = [];

function addItem(product, size) {
  const ex = cart.find(i => i.id === product.id && i.size === size);
  if (ex) ex.qty++;
  else cart.push({...product, size, qty: 1});
  updateCartUI();
}

function removeItem(idx) {
  cart.splice(idx, 1);
  updateCartUI();
}

function updateCartUI() {
  const count = cart.reduce((s, i) => s + i.qty, 0);
  document.getElementById('cartCount').textContent = count;
  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  document.getElementById('cartTotal').textContent = total.toLocaleString() + ' ₴';
  document.getElementById('cartFooter').style.display = cart.length ? 'block' : 'none';
  document.getElementById('cartItems').innerHTML = cart.length
    ? cart.map((item, idx) => `
        <div class="cart-item">
          <div class="cart-item-img">${item.emoji}</div>
          <div>
            <div class="cart-item-name">${item.name}</div>
            <div class="cart-item-size">Розмір: ${item.size} · К-сть: ${item.qty}</div>
            <button class="cart-item-remove" onclick="removeItem(${idx})">✕ Видалити</button>
          </div>
          <div class="cart-item-price">${(item.price * item.qty).toLocaleString()} ₴</div>
        </div>`).join('')
    : '<div class="cart-empty"><div class="cart-empty-icon">🛍</div><p>Кошик порожній</p></div>';
}

function toggleCart() {
  document.getElementById('cartSidebar').classList.toggle('open');
  document.getElementById('backdrop').classList.toggle('open');
}

function closeCart() {
  document.getElementById('cartSidebar').classList.remove('open');
  document.getElementById('backdrop').classList.remove('open');
}
