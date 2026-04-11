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
const messages = [
  "Trust the ancestors — your path is guided by those who loved you before time.",
  "Healing begins within your spirit; still the noise and listen to what is ancient.",
  "You are protected and aligned with your purpose. Walk without fear today.",
  "Peace flows through you like the sacred river — clear, constant, unstoppable.",
  "Your journey is sacred. Every step, even the uncertain ones, has been blessed.",
  "The bones do not lie. What is meant for you will find you in its season.",
  "You were not given this life to carry it alone. Your ancestors stand beside you.",
  "Like the mountain, you have survived every storm that came before this one.",
  "The sunrise does not ask permission — neither should your healing begin today.",
  "Be still as the cave in darkness; wisdom lives in the quiet, not the noise.",
  "Your roots go deeper than your pain. Draw strength from all who came before.",
  "Even the ocean, vast and powerful, knows when to be calm. So too can your heart.",
  "What grows in the wild places was not planted by human hands — so too your spirit.",
  "The stars remember every name. Yours has been spoken in the heavens since before.",
  "Flowers bloom in cracked earth. From your brokenness, something sacred will rise.",
  "Stone endures what water cannot hold. Your endurance is your greatest medicine.",
  "Walk softly upon this earth — she holds the bones of those who guide you still.",
  "A new day is not just a beginning; it is an answered prayer from the night before.",
  "You have ancestors who faced fires darker than yours, and still they sang. So can you.",
  "The clouds part for no one, yet the sun always waits patiently behind them. So does joy.",
  "To know yourself is the beginning of all wisdom — start there, today, without rushing.",
  "Let the river teach you: it does not fight its banks. It finds its way around every obstacle.",
  "In the silence after prayer, the ancestors lean in close. Be still enough to hear them.",
  "Your calling was written before your birth. You are not lost — you are still arriving.",
  "Every tree you see began as something that could be crushed underfoot. Remember this.",
  "The night is not against you. It is preparing you for a morning you have not yet imagined.",
  "Tend your inner world as you would a sacred fire — with patience, care, and intention.",
  "What the eyes cannot see, the spirit knows. Trust your deep knowing today.",
  "You are the harvest of generations of prayers and endurance. Do not forget your worth.",
  "Today, breathe. Tomorrow will come whether or not you carry its weight today."
];

function getDailyMessage() {
  const today = new Date();
  const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 86400000);
  return messages[dayOfYear % messages.length];
}

const dailyMsgEl = document.getElementById('dailyMsg');
if (dailyMsgEl) {
  dailyMsgEl.textContent = getDailyMessage();
}

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