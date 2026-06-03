// ── UI: АНІМАЦІЇ, TOAST, УТИЛІТИ ──

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

function observeFadeIns() {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) setTimeout(() => e.target.classList.add('visible'), i * 100);
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in:not(.visible)').forEach(el => obs.observe(el));
}

function toggleMobileMenu() {
  const nav = document.querySelector('.nav-links');
  const btn = document.getElementById('hamburger');
  nav.classList.toggle('mobile-open');
  btn.classList.toggle('open');
}

// Закрити мобільне меню при кліку на посилання
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelector('.nav-links').classList.remove('mobile-open');
    document.getElementById('hamburger').classList.remove('open');
  });
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closeLightbox();
    closeModal();
    closeCheckout();
    closeCart();
    document.querySelector('.nav-links').classList.remove('mobile-open');
    document.getElementById('hamburger')?.classList.remove('open');
  }
});

// Ініціалізація анімацій при завантаженні
observeFadeIns();

