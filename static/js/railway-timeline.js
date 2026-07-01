'use strict';

(function () {
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const SLEEPER_GAP_PX = 28;

  const section = document.querySelector('[data-railway]');
  if (!section) return;

  const layout = section.querySelector('[data-railway-layout]');
  const rail = section.querySelector('[data-railway-rail]');
  const svg = section.querySelector('[data-railway-svg]');
  const sleepersMuted = section.querySelector('[data-sleepers-muted]');
  const sleepersActive = section.querySelector('[data-sleepers-active]');
  const stations = Array.from(section.querySelectorAll('[data-railway-station]'));

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Static fallback: completed track + all stations active.
  function renderStatic() {
    section.style.setProperty('--railway-progress', '1');
    stations.forEach((s) => s.classList.add('is-active'));
    buildSleepers(/* allLaid */ true);
  }

  function buildSleepers(allLaid) {
    const h = rail.getBoundingClientRect().height;
    sleepersMuted.replaceChildren();
    sleepersActive.replaceChildren();
    if (h < 4) return [];

    const count = Math.max(2, Math.floor(h / SLEEPER_GAP_PX));
    const step = h / count;
    const activeNodes = [];

    for (let i = 0; i <= count; i += 1) {
      const y = Math.round(i * step);

      const m = document.createElementNS(SVG_NS, 'line');
      m.setAttribute('x1', '15%');
      m.setAttribute('x2', '85%');
      m.setAttribute('y1', String(y));
      m.setAttribute('y2', String(y));
      sleepersMuted.appendChild(m);

      const a = document.createElementNS(SVG_NS, 'line');
      a.setAttribute('x1', '15%');
      a.setAttribute('x2', '85%');
      a.setAttribute('y1', String(y));
      a.setAttribute('y2', String(y));
      a.dataset.y = String(y);
      if (allLaid) a.classList.add('is-laid');
      sleepersActive.appendChild(a);
      activeNodes.push({ node: a, y });
    }
    return activeNodes;
  }

  if (reduceMotion) {
    renderStatic();
    return;
  }

  // Wait for GSAP + ScrollTrigger to be available.
  function ready() {
    return typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  }

  function start() {
    const { gsap, ScrollTrigger } = window;
    gsap.registerPlugin(ScrollTrigger);

    let activeSleepers = buildSleepers(false);

    const progressObj = { value: 0 };

    const applyProgress = (p) => {
      section.style.setProperty('--railway-progress', p.toFixed(4));
      const railH = rail.getBoundingClientRect().height;
      const cutoff = railH * p;
      for (let i = 0; i < activeSleepers.length; i += 1) {
        const item = activeSleepers[i];
        const shouldLay = item.y <= cutoff;
        if (shouldLay && !item.node.classList.contains('is-laid')) {
          item.node.classList.add('is-laid');
        } else if (!shouldLay && item.node.classList.contains('is-laid')) {
          item.node.classList.remove('is-laid');
        }
      }
    };

    // Main scrub: drive the rail-fill progress across the section's scroll range.
    const mainST = ScrollTrigger.create({
      trigger: layout,
      start: 'top 75%',
      end: 'bottom 70%',
      scrub: 0.6,
      onUpdate: (self) => {
        progressObj.value = self.progress;
        applyProgress(self.progress);
      },
      onRefresh: () => applyProgress(progressObj.value),
    });

    // Per-station reveal triggers — fire when the marker crosses ~mid-viewport.
    const stationTriggers = stations.map((station) => {
      const marker = station.querySelector('.railway-station__marker');
      return ScrollTrigger.create({
        trigger: marker || station,
        start: 'top 70%',
        end: 'bottom 30%',
        onEnter: () => station.classList.add('is-active'),
        onEnterBack: () => station.classList.add('is-active'),
        onLeaveBack: () => station.classList.remove('is-active'),
      });
    });

    // Rebuild sleepers on resize (rail height changes with content/breakpoints).
    let rafId = 0;
    const handleResize = () => {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        activeSleepers = buildSleepers(false);
        applyProgress(progressObj.value);
        ScrollTrigger.refresh();
      });
    };

    window.addEventListener('resize', handleResize, { passive: true });

    // Initial paint.
    requestAnimationFrame(() => {
      ScrollTrigger.refresh();
      applyProgress(progressObj.value);
    });
  }

  // Poll briefly for GSAP if scripts are loading asynchronously.
  if (ready()) {
    start();
  } else {
    let tries = 0;
    const interval = setInterval(() => {
      tries += 1;
      if (ready()) {
        clearInterval(interval);
        start();
      } else if (tries > 80) {
        // ~4s — fall back to static state if GSAP never arrived.
        clearInterval(interval);
        renderStatic();
      }
    }, 50);
  }
})();
