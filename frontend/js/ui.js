// ── UI: АНІМАЦІЇ, TOAST, УТИЛІТИ ──

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

function observeFadeIns() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) setTimeout(() => e.target.classList.add('visible'), i * 100);
    });
  }, {threshold: 0.1});
  document.querySelectorAll('.fade-in:not(.visible)').forEach(el => obs.observe(el));
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { closeModal(); closeCheckout(); closeCart(); }
});

// Ініціалізація
observeFadeIns();
