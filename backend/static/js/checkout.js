// ── ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ──
let selectedDelivery = 'nova';
let selectedPayment  = 'card';

// Беремо CSRF-токен з cookie (Django встановлює його автоматично)
function getCsrfToken() {
  return document.cookie.split(';')
    .map(c => c.trim())
    .find(c => c.startsWith('csrftoken='))
    ?.split('=')[1] || '';
}

function openCheckout() {
  closeCart();
  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);
  document.getElementById('orderTotal').textContent = total.toLocaleString('uk-UA') + ' ₴';
  document.getElementById('orderSummaryItems').innerHTML = cart
    .map(i => `
      <div class="order-line">
        <span>${i.name} × ${i.qty} (${i.size})</span>
        <span>${(i.price * i.qty).toLocaleString('uk-UA')} ₴</span>
      </div>`).join('');
  document.getElementById('checkoutModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCheckout() {
  document.getElementById('checkoutModal').classList.remove('open');
  document.getElementById('checkoutForm').style.display  = 'block';
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

async function submitOrder() {
  const firstName = document.getElementById('firstName').value.trim();
  const lastName  = document.getElementById('lastName').value.trim();
  const phone     = document.getElementById('phone').value.trim();
  const email     = document.getElementById('email').value.trim();
  const city      = document.getElementById('city').value.trim();
  const branch    = document.getElementById('branch').value.trim();

  // Валідація
  if (!firstName) { showToast("⚠️ Введіть ім'я!"); return; }
  if (!phone)     { showToast('⚠️ Введіть номер телефону!'); return; }
  if (phone.replace(/\D/g, '').length < 10) { showToast('⚠️ Некоректний номер телефону!'); return; }
  if (!cart.length) { showToast('⚠️ Кошик порожній!'); return; }

  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);

  const payload = {
    first_name:    firstName,
    last_name:     lastName,
    phone,
    email,
    delivery_type: selectedDelivery,
    city,
    branch,
    payment_type:  selectedPayment,
    total,
    items: cart.map(i => ({
      product_id: i.id,
      name:       i.name,
      price:      i.price,
      size:       i.size,
      qty:        i.qty,
    })),
  };

  const btn = document.querySelector('.submit-order-btn');
  btn.textContent = 'Відправляємо…';
  btn.disabled = true;

  try {
    const res = await fetch('/api/orders/', {
      method:  'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken':  getCsrfToken(),
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      console.error('Помилка API:', err);
      throw new Error('HTTP ' + res.status);
    }

    // Успіх
    document.getElementById('checkoutForm').style.display  = 'none';
    document.getElementById('successScreen').style.display = 'block';
    cart = [];
    saveCart();
    updateCartUI();

  } catch (err) {
    console.error('Помилка замовлення:', err);
    showToast('❌ Помилка відправки. Спробуйте ще раз.');
  } finally {
    btn.textContent = 'Підтвердити замовлення →';
    btn.disabled = false;
  }
}

