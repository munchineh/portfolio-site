/* Shared: glass menu that unfolds from the corner; Work opens categories; hovering a category unfolds its case cards. */
(() => {
  /* Menu: the square unfolds. Work opens an accordion of categories;
     hovering a category unfolds its case cards from the right. */
  const body = document.body, toggle = document.getElementById('toggle'), scrim = document.getElementById('scrim');
  const menu = document.getElementById('menu'), work = document.getElementById('workLink'), acc = document.getElementById('workAcc');
  const stack = document.getElementById('stack'), cards = [...stack.querySelectorAll('.scard')], all = stack.querySelector('.all');
  const cats = [...document.querySelectorAll('.menu .cat')];
  const grpName = document.getElementById('grpName'), grpCount = document.getElementById('grpCount');
  const narrow = matchMedia('(max-width: 640px)');
  let closeTimer, current = null;

  const showCat = (cat) => {
    if (cat === current) return;
    const switching = !!current && !!cat;   // moving from one category straight to another
    current = cat;
    cats.forEach(c => c.classList.toggle('hot', c.dataset.cat === cat));
    if (narrow.matches) {
      document.querySelectorAll('.menu .cases').forEach(x => x.classList.toggle('open', x.dataset.for === cat));
      return;
    }
    // sit the cards 12px to the left of the menu, wherever the menu actually is
    const r = menu.getBoundingClientRect();
    stack.style.right = `${innerWidth - r.left + 12}px`;
    stack.style.width = `${Math.min(340, r.left - 24)}px`;
    // collapse the cards, then unfold the chosen category's cards one after another.
    // When switching straight between categories, All work stays open and glides to its new spot
    // instead of folding away and unfolding again, which read as a stutter.
    const allTop = all.getBoundingClientRect().top;
    (switching ? cards : [...cards, all]).forEach(el => { el.classList.remove('on'); el.style.transitionDelay = '0ms'; });
    stack.classList.toggle('on', !!cat);
    if (!cat) return;
    const btn = cats.find(c => c.dataset.cat === cat);
    grpName.textContent = btn.firstChild.textContent.trim();
    const mine = cards.filter(c => c.dataset.cat === cat);
    grpCount.textContent = mine.length;
    cards.forEach(c => c.hidden = c.dataset.cat !== cat);
    if (switching) {
      const dy = allTop - all.getBoundingClientRect().top;
      if (dy) {
        all.style.transition = 'none';
        all.style.transform = `translateY(${dy}px)`;
        all.offsetHeight;   // apply the offset before animating it away
        all.style.transition = 'transform .45s var(--ease)';
        all.style.transform = '';
        clearTimeout(all._t); all._t = setTimeout(() => { all.style.transition = ''; }, 500);
      }
    }
    requestAnimationFrame(() => requestAnimationFrame(() => {
      (switching ? mine : [...mine, all]).forEach((el, i) => { el.style.transitionDelay = `${i * 70}ms`; el.classList.add('on'); });
    }));
  };
  const setAcc = (open) => {
    acc.classList.toggle('open', open); work.setAttribute('aria-expanded', open);
    if (!open) showCat(null);
  };
  const setOpen = (open) => {
    clearTimeout(closeTimer);
    setAcc(false);
    if (open) { body.classList.remove('menu-closing'); body.classList.add('menu-open'); }
    else { body.classList.add('menu-closing'); body.classList.remove('menu-open'); closeTimer = setTimeout(() => body.classList.remove('menu-closing'), 500); }
    toggle.setAttribute('aria-expanded', open); toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };

  toggle.addEventListener('click', () => setOpen(!body.classList.contains('menu-open')));
  scrim.addEventListener('click', () => setOpen(false));
  addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
  work.addEventListener('click', () => setAcc(!acc.classList.contains('open')));
  cats.forEach(c => {
    c.addEventListener('focus', () => { if (!narrow.matches) showCat(c.dataset.cat); });
    c.addEventListener('click', () => showCat(narrow.matches && current === c.dataset.cat ? null : c.dataset.cat));
  });
  /* Forgiving hover:
     - a short delay before the cards close, so the pointer can cross the gap
     - while heading left toward the cards, brushing past another category doesn't switch sets */
  let closeT, switchT, lastX = 0, dx = 0;
  addEventListener('mousemove', e => { dx = e.clientX - lastX; lastX = e.clientX; }, { passive: true });
  const cancelClose = () => clearTimeout(closeT);
  const scheduleClose = (ms = 380) => { cancelClose(); closeT = setTimeout(() => showCat(null), ms); };
  cats.forEach(c => {
    c.addEventListener('mouseenter', () => {
      if (narrow.matches) return;
      cancelClose(); clearTimeout(switchT);
      const headingLeft = current && dx < -1;
      if (!headingLeft) { showCat(c.dataset.cat); return; }
      switchT = setTimeout(() => { if (c.matches(':hover')) showCat(c.dataset.cat); }, 220);
    });
    c.addEventListener('mouseleave', () => clearTimeout(switchT));
  });
  document.querySelectorAll('.menu .link').forEach(l => l.addEventListener('mouseenter', () => { if (!narrow.matches && current) scheduleClose(260); }));
  menu.addEventListener('mouseleave', e => { if (!narrow.matches && !stack.contains(e.relatedTarget)) scheduleClose(); });
  stack.addEventListener('mouseenter', () => { cancelClose(); clearTimeout(switchT); });
  stack.addEventListener('mouseleave', e => { if (!menu.contains(e.relatedTarget)) scheduleClose(); });

})();

/* Rolling numbers: each digit spins through a column of 0–9 and lands on its value, like an odometer. */
/* A plus sign sits on the baseline; lift it so it centres on the numerals */
window.liftPlus = (el) => {
  const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [];
  while (walk.nextNode()) if (walk.currentNode.nodeValue.includes('+') && !walk.currentNode.parentElement.classList.contains('plus')) nodes.push(walk.currentNode);
  nodes.forEach(n => { const frag = document.createDocumentFragment();
    n.nodeValue.split(/(\+)/).forEach(part => { if (!part) return; if (part === '+') { const s = document.createElement('span'); s.className = 'plus'; s.textContent = '+'; frag.appendChild(s); } else frag.appendChild(document.createTextNode(part)); });
    n.replaceWith(frag); });
};
document.querySelectorAll('[data-n], .yrs').forEach(el => window.liftPlus(el));

window.rollNumber = (el) => {
  const text = el.dataset.n || el.textContent.trim();
  el.dataset.n = text;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = text; window.liftPlus(el); return; }
  el.setAttribute('aria-label', text);
  el.innerHTML = '';
  el.classList.add('roll');
  let d = 0;
  [...text].forEach(ch => {
    if (/\d/.test(ch)) {
      const n = +ch, loops = text.replace(/\D/g, '').length === 1 ? 2 : 1 + (d % 2);
      const col = document.createElement('span'); col.className = 'roll-col'; col.setAttribute('aria-hidden', 'true');
      const strip = document.createElement('span'); strip.className = 'roll-strip';
      const seq = []; for (let i = 0; i < loops * 10 + n + 1; i++) seq.push(i % 10);
      strip.innerHTML = seq.map(v => `<span>${v}</span>`).join('');
      col.appendChild(strip); el.appendChild(col);
      const steps = seq.length - 1, delay = d * 70;
      strip.style.transition = 'none'; strip.style.transform = 'translateY(0)';
      requestAnimationFrame(() => requestAnimationFrame(() => {
        strip.style.transition = `transform ${900 + d * 120}ms cubic-bezier(.2,.8,.2,1) ${delay}ms`;
        strip.style.transform = `translateY(-${steps}em)`;
      }));
      d++;
    } else {
      const s = document.createElement('span'); s.className = 'roll-ch' + (ch === '+' ? ' plus' : ''); s.setAttribute('aria-hidden', 'true'); s.textContent = ch; el.appendChild(s);
    }
  });
};

/* Theme switch: light, dark or match the system (the default). Saved per visitor. */
(() => {
  const root = document.documentElement, groups = document.querySelectorAll('.theme');
  let pick = 'system'; try { pick = localStorage.getItem('theme') || 'system'; } catch (e) {}
  const order = ['light', 'dark', 'system'];
  const apply = t => {
    pick = t;
    if (t === 'system') delete root.dataset.theme; else root.dataset.theme = t;
    try { t === 'system' ? localStorage.removeItem('theme') : localStorage.setItem('theme', t); } catch (e) {}
    groups.forEach(g => { g.style.setProperty('--i', order.indexOf(t));
      g.querySelectorAll('button').forEach(b => { const on = b.dataset.t === t; b.setAttribute('aria-checked', on); b.tabIndex = on ? 0 : -1; }); });
  };
  groups.forEach(g => {
    g.querySelectorAll('button').forEach(b => b.addEventListener('click', () => apply(b.dataset.t)));
    g.addEventListener('keydown', e => { const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!k) return;
      e.preventDefault(); const n = order[(order.indexOf(pick) + k + 3) % 3]; apply(n); g.querySelector(`[data-t="${n}"]`).focus(); });
  });
  apply(pick);
})();


/* Mobile menu: each case in the Work accordion becomes a tappable card, reusing the desktop card's logo, title and industry */
(() => {
  const cards = new Map([...document.querySelectorAll('#stack .scard')].map(c => [c.getAttribute('href'), c]));
  document.querySelectorAll('.menu .cases a').forEach(a => {
    const c = cards.get(a.getAttribute('href')); if (!c) return;
    a.classList.add('mcard');
    a.innerHTML = c.innerHTML;
  });
})();

/* Sideways rows of screens: dots under the row show how many screens there are and which one you're on */
(() => {
  document.querySelectorAll('.phones').forEach(row => {
    const items = [...row.children];
    if (items.length < 2) return;
    const pager = document.createElement('div');
    pager.className = 'pager'; pager.setAttribute('aria-hidden', 'true');
    const dots = items.map((it, i) => {
      const d = document.createElement('button');
      d.type = 'button'; d.tabIndex = -1;
      d.addEventListener('click', () => row.scrollTo({ left: it.offsetLeft - row.offsetLeft - (parseFloat(getComputedStyle(row).paddingLeft) || 0), behavior: 'smooth' }));
      pager.appendChild(d); return d;
    });
    row.after(pager);
    let cur = -1, raf = 0;
    const sync = () => {
      raf = 0;
      pager.hidden = row.scrollWidth <= row.clientWidth + 2;
      if (pager.hidden) return;
      const x = row.scrollLeft, max = row.scrollWidth - row.clientWidth;
      // the last screens can't snap to the left edge, so reaching the end lights the last dot
      let i = x >= max - 4 ? items.length - 1 : 0;
      if (i === 0) { let best = Infinity; items.forEach((it, k) => { const dx = Math.abs(it.offsetLeft - items[0].offsetLeft - x); if (dx < best) { best = dx; i = k; } }); }
      if (i !== cur) { dots.forEach((d, k) => d.classList.toggle('on', k === i)); cur = i; }
    };
    row.addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(sync); }, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(() => { cur = -1; sync(); }).observe(row);
    sync();
  });
})();

/* Pause looping animations (timer ring, pulses, cursors, demo loops) while they're off screen */
(() => {
  const els = document.querySelectorAll('.demo, .tmr, .okp, .orb, .scene, .pi, .nvp, .relay');
  if (!els.length || !('IntersectionObserver' in window)) return;
  const io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('is-off', !e.isIntersecting)), { rootMargin: '120px 0px' });
  els.forEach(el => io.observe(el));
})();

/* Remember a manual language choice so the server stops guessing */
document.querySelectorAll('.lang a[data-l]').forEach(a => a.addEventListener('click', e => {
  document.cookie = `lang=${a.dataset.l}; path=/; max-age=31536000; SameSite=Lax`;
  if (location.hash) { e.preventDefault(); location.href = a.getAttribute('href') + location.hash; }
}));

/* Name pill: shows the full name when you land, then becomes a round Home button.
   Home page: full name only while at the very top. Case pages: becomes Home shortly after landing.
   With a mouse, hovering the button opens the name back up.
   The change is a "backspace": a cursor deletes the name letter by letter, then turns into the house.
   Going back, the house turns into the cursor and the name is typed out again. */
(() => {
  const el = document.querySelector('.top .name'); if (!el) return;
  const onHome = !!document.querySelector('.hero-head');
  const canHover = matchMedia('(hover: hover) and (pointer: fine)');
  const still = matchMedia('(prefers-reduced-motion: reduce)');
  const label = el.querySelector('.nm-t'), NAME = [...label.textContent.trim()];
  const caret = document.createElement('i'); caret.className = 'nm-c'; caret.setAttribute('aria-hidden', 'true'); label.after(caret);
  const pad = () => parseFloat(getComputedStyle(el).fontSize) * 1.1;
  let shown = NAME.length, home = false, run = 0, settled = onHome, hover = false, focus = false, idle = 0;
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const fit = () => { if (home) { el.style.width = ''; return; } el.style.width = (label.getBoundingClientRect().width + (el.classList.contains('typing') ? 4 : 0) + pad() * 2).toFixed(1) + 'px'; };
  const show = n => { shown = n; label.textContent = NAME.slice(0, n).join(''); fit(); };
  const typing = on => { clearTimeout(idle); el.classList.toggle('typing', on); if (!on) fit(); };
  let target = false;
  const go = async h => {
    // keep going if we're already heading there, so continuous scrolling doesn't keep restarting it
    if (h === target && (run || h === home)) return; target = h; const me = ++run, ok = () => me === run;
    if (still.matches) { home = h; el.classList.toggle('home', h); el.classList.toggle('typing', !h); show(h ? 0 : NAME.length); run = 0; return; }
    if (h) {
      typing(true);
      for (let n = shown - 1; n >= 0; n--) { show(n); await wait(16); if (!ok()) return; }
      await wait(40); if (!ok()) return;
      home = true; el.classList.add('home'); typing(false);
    } else {
      home = false; el.classList.remove('home'); typing(true); fit(); await wait(90); if (!ok()) return;
      for (let n = shown + 1; n <= NAME.length; n++) { show(n); await wait(20); if (!ok()) return; }
    }
    if (ok()) run = 0;
  };
  const update = () => go((onHome ? scrollY > 0 : settled) && !hover && !focus);
  // the cursor blinks whenever the name is showing
  el.classList.add('typing'); fit(); if (document.fonts) document.fonts.ready.then(fit); addEventListener('resize', fit);
  update();
  if (onHome) { let tk = 0; addEventListener('scroll', () => { if (tk) return; tk = requestAnimationFrame(() => { tk = 0; update(); }); }, { passive: true }); }
  else setTimeout(() => { settled = true; update(); }, 1400);
  // On the home page the button scrolls back to the top, then the page settles with a small springy bounce
  if (onHome) el.addEventListener('click', e => {
    e.preventDefault();
    const parts = [...document.body.children].filter(n => n.matches('header.top, section, footer'));
    const bounce = () => { if (still.matches) return; parts.forEach(n => n.animate(
      [{ transform: 'translateY(0)' }, { transform: 'translateY(16px)', offset: .3 }, { transform: 'translateY(-4px)', offset: .62 }, { transform: 'translateY(1px)', offset: .84 }, { transform: 'translateY(0)' }],
      { duration: 560, easing: 'cubic-bezier(.3,.7,.4,1)' })); };
    const y0 = scrollY; if (y0 <= 0) { bounce(); return; }
    if (still.matches) { scrollTo({ top: 0, behavior: 'instant' }); return; }
    const dur = Math.min(900, 380 + y0 * 0.12), t0 = performance.now(); let stop = false;
    const cancel = () => { stop = true; }; addEventListener('wheel', cancel, { once: true, passive: true }); addEventListener('touchstart', cancel, { once: true, passive: true });
    const ease = x => 1 - Math.pow(1 - x, 3);
    const frame = now => { if (stop) return; const k = Math.min(1, (now - t0) / dur); scrollTo({ top: y0 * (1 - ease(k)), behavior: 'instant' });
      if (k < 1) requestAnimationFrame(frame); else { removeEventListener('wheel', cancel); removeEventListener('touchstart', cancel); bounce(); } };
    requestAnimationFrame(frame);
  });
  el.addEventListener('mouseenter', () => { if (canHover.matches) { hover = true; update(); } });
  el.addEventListener('mouseleave', () => { hover = false; update(); });
  el.addEventListener('focus', () => { if (el.matches(':focus-visible')) { focus = true; update(); } });
  el.addEventListener('blur', () => { focus = false; update(); });
})();

/* No orphans: when a block of text ends on a stub line, let it run a little wider so the stub folds back in.
   If there's no room for that, balance the lines instead. Runs again on resize. */
(() => {
  const SEL = 'p, figcaption, .stat span, .sec .sh h2';
  const SKIP = '.menu, .stack, .scrim, [data-no-unorphan]';
  const STUB = 0.34, GROW = 1.2;
  const lineWidths = (el) => {
    const r = document.createRange(); r.selectNodeContents(el);
    const rows = [];
    for (const b of r.getClientRects()) {
      if (b.width < 1 || b.height < 1) continue;
      const row = rows.find(x => Math.abs(x.top - b.top) < b.height * 0.5);
      if (row) { row.l = Math.min(row.l, b.left); row.r = Math.max(row.r, b.right); }
      else rows.push({ top: b.top, l: b.left, r: b.right });
    }
    return rows.sort((a, b) => a.top - b.top).map(x => x.r - x.l);
  };
  const innerWidth = (el) => { const cs = getComputedStyle(el); return el.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight); };
  const fix = (el) => {
    el.style.maxWidth = ''; el.style.textWrap = '';
    const w = el.getBoundingClientRect().width;
    if (!w) return;
    const rows = lineWidths(el);
    if (rows.length < 2 || rows[rows.length - 1] >= w * STUB) return;
    const room = el.parentElement ? innerWidth(el.parentElement) : w;
    const cap = Math.min(w * GROW, room);
    if (cap > w + 4) {
      el.style.maxWidth = cap + 'px';
      if (lineWidths(el).length < rows.length) return;
      el.style.maxWidth = '';
    }
    if (rows.length <= 6) el.style.textWrap = 'balance';
  };
  const run = () => document.querySelectorAll(SEL).forEach(el => { if (!el.closest(SKIP) && el.textContent.trim()) fix(el); });
  let t;
  const later = () => { clearTimeout(t); t = setTimeout(run, 150); };
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(run);
  addEventListener('resize', later);
  addEventListener('load', run);
})();

/* Email links: open the mail app if there is one, and always copy the address so the click is never a dead end */
(() => {
  let toast, t;
  const say = (msg) => {
    if (!toast) { toast = document.createElement('div'); toast.className = 'toast'; toast.setAttribute('role', 'status'); document.body.appendChild(toast); }
    toast.textContent = msg; toast.classList.add('on');
    clearTimeout(t); t = setTimeout(() => toast.classList.remove('on'), 2600);
  };
  const lang = (document.documentElement.lang || 'en').toLowerCase();
  const copied = { de: 'E-Mail-Adresse kopiert', ko: '이메일 주소를 복사했어요', 'zh-hans': '邮箱地址已复制', 'zh-hant': '電子郵件地址已複製' }[lang] || 'Email address copied';
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="mailto:"]');
    if (!a) return;
    const addr = decodeURIComponent(a.getAttribute('href').slice(7).split('?')[0]);
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(addr).then(() => say(`${copied}: ${addr}`), () => {});
  });
})();

/* Rotating word in a headline: <em class="swap" data-words="a|b|c">. Pauses off-screen and for reduced motion. */
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.swap[data-words]').forEach(box => {
    const words = box.dataset.words.split('|');
    if (words.length < 2 || still.matches) return;
    box.setAttribute('aria-label', words[0]);
    box.innerHTML = words.map((w, i) => `<i aria-hidden="true"${i ? '' : ' class="on"'}>${w}</i>`).join('');
    const items = [...box.children];
    box.classList.add('live');
    const size = () => items.map(i => i.getBoundingClientRect().width);
    let widths = size(), n = 0, seen = true, timer;
    box.style.width = widths[0] + 'px';
    /* Line breaks are decided by the longest word, not the one showing, so a short word never pulls the next words up */
    const line = box.closest('.line');
    let tail = null;
    if (line && box.nextSibling && box.nextSibling.nodeType === 3 && box.nextSibling.textContent.trim()) {
      tail = document.createElement('span'); tail.className = 'swap-tail';
      tail.textContent = box.nextSibling.textContent; box.nextSibling.replaceWith(tail);
    }
    const fit = () => {
      if (!tail) return;
      line.classList.remove('tail-down');
      const keep = box.style.width;
      box.style.transition = 'none'; box.style.width = Math.max(...widths) + 'px';
      const rects = tail.getClientRects(), last = rects[rects.length - 1];
      const wraps = !!last && last.top > box.getBoundingClientRect().top + 2;
      box.style.width = keep; void box.offsetWidth; box.style.transition = '';
      line.classList.toggle('tail-down', wraps);
    };
    fit();
    const step = () => {
      if (!seen || document.hidden) return;
      const prev = items[n]; n = (n + 1) % items.length; const next = items[n];
      prev.classList.remove('on'); prev.classList.add('out');
      next.classList.add('on');
      box.style.width = widths[n] + 'px';
      setTimeout(() => { prev.style.transition = 'none'; prev.classList.remove('out'); void prev.offsetWidth; prev.style.transition = ''; }, 460);
    };
    const start = () => { clearInterval(timer); timer = setInterval(step, 1500); };
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => { widths = size(); box.style.width = widths[n] + 'px'; fit(); start(); });
    addEventListener('resize', () => { widths = size(); box.style.width = widths[n] + 'px'; fit(); });
    new IntersectionObserver(([e]) => { seen = e.isIntersecting; }).observe(box);
  });
})();
