// ── LIGHTBOX ──
let lbImages    = [];
let lbIdx       = 0;
let lbTouchX    = 0;

function openLightbox(pid, startIdx = 0) {
  const product = allProducts.find(p => p.id === pid);
  if (!product?.images?.length) { openModal(pid); return; }

  lbImages = product.images;
  lbIdx    = startIdx;

  document.getElementById('lbTrack').innerHTML = lbImages
    .map(img => `
      <div class="lb-slide">
        <img src="${img.image_url}" alt="">
      </div>`).join('');

  lbUpdate();
  document.getElementById('lightbox').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow = '';
}

function lbNav(dir) {
  lbIdx = (lbIdx + dir + lbImages.length) % lbImages.length;
  lbUpdate();
}

function lbUpdate() {
  document.getElementById('lbTrack').style.transform = `translateX(-${lbIdx * 100}%)`;
  document.getElementById('lbCounter').textContent   = `${lbIdx + 1} / ${lbImages.length}`;
  document.getElementById('lbDots').innerHTML = lbImages
    .map((_, i) => `
      <button class="lb-dot ${i === lbIdx ? 'active' : ''}"
        onclick="event.stopPropagation();lbIdx=${i};lbUpdate()"></button>`)
    .join('');
}

// ── Touch swipe ──
document.addEventListener('DOMContentLoaded', () => {
  const viewport = document.getElementById('lbViewport');
  if (!viewport) return;

  viewport.addEventListener('touchstart', e => {
    lbTouchX = e.touches[0].clientX;
  }, { passive: true });

  viewport.addEventListener('touchend', e => {
    const diff = lbTouchX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40 && lbImages.length > 1) lbNav(diff > 0 ? 1 : -1);
  });

  // Keyboard (стрілки для lightbox)
  document.addEventListener('keydown', e => {
    if (!document.getElementById('lightbox').classList.contains('open')) return;
    if (e.key === 'ArrowLeft')  lbNav(-1);
    if (e.key === 'ArrowRight') lbNav(1);
  });
});

