// ── ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ──
let selectedDelivery = 'nova';
let selectedPayment = 'card';

function openCheckout() {
  closeCart();
  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  document.getElementById('orderTotal').textContent = total.toLocaleString() + ' ₴';
  document.getElementById('orderSummaryItems').innerHTML = cart
    .map(i => `<div class="order-line"><span>${i.name} × ${i.qty} (${i.size})</span><span>${(i.price * i.qty).toLocaleString()} ₴</span></div>`)
    .join('');
  document.getElementById('checkoutModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCheckout() {
  document.getElementById('checkoutModal').classList.remove('open');
  document.getElementById('checkoutForm').style.display = 'block';
  document.getElementById('successScreen').style.display = 'none';
  document.body.style.overflow = '';
}

function selectDelivery(type) {
  selectedDelivery = type;
  document.querySelectorAll('.delivery-option').forEach(d => d.classList.remove('selected'));
  document.getElementById('del-' + type).classList.add('selected');
}

function selectPayment(type) {
  selectedPayment = type;
  document.querySelectorAll('.payment-option').forEach(d => d.classList.remove('selected'));
  document.getElementById('pay-' + type).classList.add('selected');
}

function submitOrder() {
  const name = document.getElementById('firstName').value;
  const phone = document.getElementById('phone').value;
  if (!name || !phone) { showToast("Заповніть ім'я та телефон!"); return; }
  if (!cart.length) { showToast('Додайте товари до кошика!'); return; }

  // TODO: відправити замовлення на бекенд
  // fetch('/api/orders', { method:'POST', body: JSON.stringify({...}) })

  document.getElementById('checkoutForm').style.display = 'none';
  document.getElementById('successScreen').style.display = 'block';
  cart = [];
  updateCartUI();
}
