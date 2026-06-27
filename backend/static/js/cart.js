// ── КОШИК ──

let cart = JSON.parse(localStorage.getItem('varel_cart') || '[]');

function saveCart() {
  localStorage.setItem('varel_cart', JSON.stringify(cart));
}

function addItem(product, size, color = 'Без кольору') {
  const ex = cart.find(i => i.id === product.id && i.size === size && i.color === color);
  if (ex) {
    ex.qty++;
  } else {
    cart.push({
      id:    product.id,
      name:  product.name,
      emoji: product.emoji,
      price: product.price,
      size,
      color,
      qty:   1,
    });
  }
  saveCart();
  updateCartUI();
}

function removeItem(idx) {
  cart.splice(idx, 1);
  saveCart();
  updateCartUI();
}

function updateCartUI() {
  const count = cart.reduce((s, i) => s + i.qty, 0);
  document.getElementById('cartCount').textContent = count;

  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  document.getElementById('cartTotal').textContent = total.toLocaleString('uk-UA') + ' ₴';
  document.getElementById('cartFooter').style.display = cart.length ? 'block' : 'none';

  document.getElementById('cartItems').innerHTML = cart.length
    ? cart.map((item, idx) => `
        <div class="cart-item">
          <div class="cart-item-img">${item.emoji}</div>
          <div>
            <div class="cart-item-name">${item.name}</div>
            <div class="cart-item-size">Розмір: ${item.size} · Колір: ${item.color} · К-сть: ${item.qty}</div>
            <button class="cart-item-remove" onclick="removeItem(${idx})">✕ Видалити</button>
          </div>
          <div class="cart-item-price">${(item.price * item.qty).toLocaleString('uk-UA')} ₴</div>
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

// Відображаємо збережений кошик одразу після завантаження
updateCartUI();

