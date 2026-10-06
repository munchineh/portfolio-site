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
    // collapse everything, then unfold the chosen category's cards one after another
    [...cards, all].forEach(el => { el.classList.remove('on'); el.style.transitionDelay = '0ms'; });
    stack.classList.toggle('on', !!cat);
    if (!cat) return;
    const btn = cats.find(c => c.dataset.cat === cat);
    grpName.textContent = btn.firstChild.textContent.trim();
    const mine = cards.filter(c => c.dataset.cat === cat);
    grpCount.textContent = mine.length;
    cards.forEach(c => c.hidden = c.dataset.cat !== cat);
    requestAnimationFrame(() => requestAnimationFrame(() => {
      [...mine, all].forEach((el, i) => { el.style.transitionDelay = `${i * 70}ms`; el.classList.add('on'); });
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
      const n = +ch, loops = 1 + (d % 2);
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


/* Remember a manual language choice so the server stops guessing */
document.querySelectorAll('.lang a[data-l]').forEach(a => a.addEventListener('click', e => {
  document.cookie = `lang=${a.dataset.l}; path=/; max-age=31536000; SameSite=Lax`;
  if (location.hash) { e.preventDefault(); location.href = a.getAttribute('href') + location.hash; }
}));

/* Name pill: shows the full name when you land, then shrinks into a Home button.
   Home page: full name only while at the very top. Case pages: shrinks shortly after landing.
   With a mouse, hovering the button opens the name back up. */
(() => {
  const el = document.querySelector('.top .name'); if (!el) return;
  const onHome = !!document.querySelector('.hero-head');
  const canHover = matchMedia('(hover: hover) and (pointer: fine)');
  let settled = onHome, hover = false, focus = false;
  const measure = () => { const was = el.classList.contains('home'); el.style.transition = 'none'; el.classList.remove('home'); el.style.width = 'auto';
    const w = el.offsetWidth; el.style.width = ''; el.style.setProperty('--nm-w', w + 'px'); el.classList.toggle('home', was); el.offsetWidth; el.style.transition = ''; };
  const update = () => { const want = onHome ? scrollY > 40 : settled; el.classList.toggle('home', want && !hover && !focus); };
  measure(); update();
  if (document.fonts) document.fonts.ready.then(() => { measure(); update(); });
  addEventListener('resize', () => { measure(); update(); });
  if (onHome) { let t = 0; addEventListener('scroll', () => { if (t) return; t = requestAnimationFrame(() => { t = 0; update(); }); }, { passive: true }); }
  else setTimeout(() => { settled = true; update(); }, 1400);
  el.addEventListener('mouseenter', () => { if (canHover.matches) { hover = true; update(); } });
  el.addEventListener('mouseleave', () => { hover = false; update(); });
  el.addEventListener('focus', () => { if (el.matches(':focus-visible')) { focus = true; update(); } });
  el.addEventListener('blur', () => { focus = false; update(); });
})();
