'use strict';

// ============================================
// HEADER SCROLL BEHAVIOR
// ============================================
const header = document.querySelector('.site-header');
const isHomePage = document.body.dataset.page === 'home';

if (header) {
  if (!isHomePage) {
    // Non-home pages: header is solid from the start
    header.classList.add('site-header--scrolled');
  }

  const onScroll = () => {
    if (isHomePage) {
      // Homepage only: toggle solid background on scroll
      header.classList.toggle('site-header--scrolled', window.scrollY > 60);
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
}

// ============================================
// MOBILE MENU
// ============================================
const menuToggle = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-nav]');

if (menuToggle && nav) {
  menuToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('nav--open');
    menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close on nav link click (mobile)
  nav.querySelectorAll('.site-nav__link').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('nav--open');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (nav.classList.contains('nav--open') && !nav.contains(e.target) && !menuToggle.contains(e.target)) {
      nav.classList.remove('nav--open');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });
}

// ============================================
// COUNTER ANIMATION FOR STATS
// ============================================
function animateCounter(el) {
  const target = parseInt(el.dataset.counter, 10);
  if (isNaN(target)) return;

  const duration = 1800; // ms
  const startTime = performance.now();

  const tick = (now) => {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(eased * target);
    el.textContent = current.toLocaleString('ru-KZ');
    if (progress < 1) {
      requestAnimationFrame(tick);
    }
  };

  requestAnimationFrame(tick);
}

const statsSection = document.querySelector('[data-stats]');

if (statsSection) {
  const counters = statsSection.querySelectorAll('[data-counter]');
  let animated = false;

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting && !animated) {
        animated = true;
        counters.forEach(animateCounter);
        observer.disconnect();
      }
    },
    { threshold: 0.3 }
  );

  observer.observe(statsSection);
}

// ============================================
// PROJECT FILTER (no page reload)
// ============================================
const filterBtns = document.querySelectorAll('.btn-filter[data-filter]');
const projectCards = document.querySelectorAll('.project-card[data-type]');

if (filterBtns.length && projectCards.length) {
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.dataset.filter;

      filterBtns.forEach(b => b.classList.remove('btn-filter--active'));
      btn.classList.add('btn-filter--active');

      projectCards.forEach(card => {
        const show = !type || card.dataset.type === type;
        card.style.display = show ? '' : 'none';
      });
    });
  });
}

// ============================================
// SCROLL REVEAL (subtle entrance animations)
// ============================================
// inspired by Martinus AOS scroll reveal — extended to timeline and pillar cards
const revealEls = document.querySelectorAll('.project-card, .service-card, .news-card, .article-card, .equipment-card, .value-item, .client-type-item, .steps__item, .timeline__item, .pillar-card');

if (revealEls.length && 'IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  revealEls.forEach(el => revealObserver.observe(el));
}
