// =====================================================
//  Ntatemoholo Seromo — Sangoma Wisdom
//  Main JavaScript
//  File: core/static/core/main.js
// =====================================================

// ── BACKGROUND SLIDESHOW ──────────────────────────────────────────
const slides = document.querySelectorAll('#bg-canvas .slide');
const bgNames = [
  'Mountain', 'Waterfall', 'Ocean', 'Forest Lake',
  'Sunrise', 'Sunset', 'Cave', 'Meadow',
  'Starry Night', 'Forest', 'Cliffside', 'Stone Path'
];
const bgLabel = document.getElementById('bg-label');
let current = 0;

function nextSlide() {
  slides[current].classList.remove('active');
  current = (current + 1) % slides.length;
  slides[current].classList.add('active');
  bgLabel.style.opacity = '0';
  setTimeout(() => {
    bgLabel.textContent = bgNames[current];
    bgLabel.style.opacity = '1';
  }, 600);
}
setInterval(nextSlide, 7000);

// ── DAILY MESSAGES ────────────────────────────────────────────────
// The homepage message is rendered by Django admin. No client-side fallback is used.

// ── NAVBAR SCROLL ──────────────────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 30);
});

// ── MOBILE MENU ────────────────────────────────────────────────────
function toggleMenu() {
  document.getElementById('navLinks').classList.toggle('open');
}

// ── SCROLL REVEAL ─────────────────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// ── AUTH MODAL ─────────────────────────────────────────────────────
function openModal(tab) {
  document.getElementById('authModal').classList.add('open');
  switchTab(tab || 'signin');
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  document.getElementById('authModal').classList.remove('open');
  document.body.style.overflow = '';
}
function closeModalOutside(e) {
  if (e.target === document.getElementById('authModal')) closeModal();
}
function switchTab(tab) {
  document.getElementById('tabSignin').classList.toggle('active', tab === 'signin');
  document.getElementById('tabRegister').classList.toggle('active', tab === 'register');
  document.getElementById('panelSignin').classList.toggle('active', tab === 'signin');
  document.getElementById('panelRegister').classList.toggle('active', tab === 'register');
}
function handleAuth(type) {
  const label = type === 'signin'
    ? 'Welcome back. The ancestors are with you.'
    : 'Your account has been created. Welcome to the circle.';
  showToast(label);
  closeModal();
}
function handleContact(e) {
  e.preventDefault();
  showToast('Your message has been sent. We will be in touch soon. ✦');
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// ── TOAST NOTIFICATION ─────────────────────────────────────────────
function showToast(msg) {
  const t = document.createElement('div');
  t.textContent = msg;
  Object.assign(t.style, {
    position: 'fixed', bottom: '40px', left: '50%',
    transform: 'translateX(-50%) translateY(20px)',
    background: 'rgba(15,18,20,0.95)',
    border: '0.5px solid rgba(201,168,76,0.4)',
    color: '#f0ebe0',
    fontFamily: "'Raleway',sans-serif",
    fontSize: '14px', fontWeight: '300',
    padding: '14px 28px', borderRadius: '40px',
    backdropFilter: 'blur(12px)',
    zIndex: '999', opacity: '0',
    transition: 'all 0.4s ease',
    whiteSpace: 'nowrap', maxWidth: '80vw',
    textOverflow: 'ellipsis', overflow: 'hidden'
  });
  document.body.appendChild(t);
  requestAnimationFrame(() => {
    t.style.opacity = '1';
    t.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateX(-50%) translateY(10px)';
    setTimeout(() => t.remove(), 500);
  }, 3500);
}