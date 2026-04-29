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
        <span>${i.name} × ${i.qty} (${i.size}, ${i.color || 'Без кольору'})</span>
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

  const normalizedPhone = normalizePhone(phone);
  if (!normalizedPhone) {
    showToast('⚠️ Телефон має містити від 10 до 15 цифр.');
    return;
  }

  const total = cart.reduce((s, i) => s + i.price * i.qty, 0);

  const payload = {
    first_name:    firstName,
    last_name:     lastName,
    phone: normalizedPhone,
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
      color:      i.color || 'Без кольору',
      qty:        i.qty,
    })),
  };

  const btn = document.querySelector('.submit-order-btn');
  btn.textContent = 'Відправляємо…';
  btn.disabled = true;

  let shownApiError = false;

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
      const msg = extractApiError(err);
      if (msg) {
        showToast('⚠️ ' + msg);
        shownApiError = true;
      }
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
    if (!shownApiError) {
      showToast('❌ Помилка відправки. Спробуйте ще раз.');
    }
  } finally {
    btn.textContent = 'Підтвердити замовлення →';
    btn.disabled = false;
  }
}

function normalizePhone(value) {
  const digits = String(value || '').replace(/\D/g, '');
  if (digits.length < 10 || digits.length > 15) return '';

  // Common UA local format: 0XXXXXXXXX -> +380XXXXXXXXX
  if (digits.length === 10 && digits.startsWith('0')) {
    return '+38' + digits;
  }
  return '+' + digits;
}

function extractApiError(err) {
  if (!err || typeof err !== 'object') return '';
  const firstKey = Object.keys(err)[0];
  if (!firstKey) return '';
  const val = err[firstKey];
  if (Array.isArray(val) && val.length) return String(val[0]);
  if (typeof val === 'string') return val;
  return '';
}

function initPhoneInputMask() {
  const input = document.getElementById('phone');
  if (!input) return;

  input.placeholder = '+380 (67) 123-45-67';
  input.addEventListener('input', () => {
    const rawDigits = input.value.replace(/\D/g, '');
    let digits = rawDigits;

    if (digits.startsWith('380')) {
      digits = digits.slice(0, 12);
    } else if (digits.startsWith('0')) {
      digits = ('38' + digits).slice(0, 12);
    } else {
      digits = digits.slice(0, 15);
    }

    if (digits.startsWith('380')) {
      const cc = '380';
      const p1 = digits.slice(3, 5);
      const p2 = digits.slice(5, 8);
      const p3 = digits.slice(8, 10);
      const p4 = digits.slice(10, 12);
      let formatted = `+${cc}`;
      if (p1) formatted += ` (${p1}`;
      if (p1 && p1.length === 2) formatted += ')';
      if (p2) formatted += ` ${p2}`;
      if (p3) formatted += `-${p3}`;
      if (p4) formatted += `-${p4}`;
      input.value = formatted;
      return;
    }

    input.value = digits ? `+${digits}` : '';
  });
}

initPhoneInputMask();

