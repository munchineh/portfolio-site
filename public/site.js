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


/* Remember a manual language choice so the server stops guessing */
document.querySelectorAll('.lang a[data-l]').forEach(a => a.addEventListener('click', e => {
  document.cookie = `lang=${a.dataset.l}; path=/; max-age=31536000; SameSite=Lax`;
  if (location.hash) { e.preventDefault(); location.href = a.getAttribute('href') + location.hash; }
}));

/* Name pill: shows the full name when you land, then becomes a round Home button.
   Home page: full name only while at the very top. Case pages: becomes Home shortly after landing.
   With a mouse, hovering the button opens the name back up.
   English and German pages morph the vector name (Archivo 800, 75% width) straight into the house on a spring;
   other scripts fall back to letters folding into the house. */
(() => {
  const el = document.querySelector('.top .name'); if (!el) return;
  const onHome = !!document.querySelector('.hero-head');
  const canHover = matchMedia('(hover: hover) and (pointer: fine)');
  const still = matchMedia('(prefers-reduced-motion: reduce)');
  const label = el.querySelector('.nm-t');
  const NM = {"w": 5547, "capH": 686, "full": "M56.1 0L56.1 -687.4L285.4 -687.4L350.9 -379.9Q354.3 -363.9 359.2 -338.1Q364.2 -312.2 369.5 -285.1Q374.7 -258 378.5 -236.1L386.6 -236.1Q389.5 -253 394 -277.6Q398.5 -302.3 403.5 -329.1Q408.4 -355.9 412.6 -379.4L477.4 -687.4L701.9 -687.4L701.9 0L546.9 0L546.9 -298.4Q546.9 -336.3 548 -372.3Q549.1 -408.2 550.4 -436.7Q551.8 -465.2 551.8 -479.1L544 -479.1Q542.1 -466.7 537.9 -446.7Q533.6 -426.8 529.3 -406.1Q525 -385.4 520.9 -369.7L440 0L313 0L232 -369.5Q229.1 -382.8 224.8 -402.3Q220.4 -421.9 216.5 -442.8Q212.6 -463.6 209.3 -478.9L201.9 -478.9Q203.2 -457.5 204.1 -426.4Q205 -395.3 205.8 -361.8Q206.5 -328.3 206.5 -298.4L206.5 0ZM760.6 0L944.8 -687.4L1155.1 -687.4L1339.8 0L1168.9 0L1139.4 -124.7L954.8 -124.7L925.9 0ZM982.1 -254.3L1112.5 -254.3L1075.2 -424.6Q1073.2 -433.5 1070.2 -447.7Q1067.3 -461.9 1064 -479Q1060.7 -496.1 1057.3 -513.2Q1053.9 -530.3 1051.1 -544.2L1043.8 -544.2Q1040.8 -526.7 1036.5 -504.6Q1032.1 -482.4 1027.8 -461.1Q1023.4 -439.8 1019.7 -424.6ZM1397.5 0L1397.5 -687.4L1547.8 -687.4L1699.3 -395.8Q1703.8 -386.9 1710.1 -374.4Q1716.4 -361.8 1722.7 -348.3Q1729 -334.7 1732.8 -322.9L1737.8 -323.3Q1737.3 -343.1 1737.3 -362.4Q1737.3 -381.7 1737.3 -395.8L1737.3 -687.4L1890.1 -687.4L1890.1 0L1740.1 0L1583.5 -298.8Q1575.7 -314.9 1568.1 -334.2Q1560.5 -353.5 1554.3 -371.5L1549.6 -371.1Q1550 -353.9 1550 -334.4Q1550 -315 1550 -298.8L1550 0ZM2251.8 12Q2159.2 12 2099.4 -26.4Q2039.6 -64.7 2011 -143.7Q1982.3 -222.8 1982.3 -344.2Q1982.3 -525.6 2051.3 -612.7Q2120.2 -699.7 2258.4 -699.7Q2334.7 -699.7 2389.3 -670.4Q2443.9 -641 2473.3 -578.2Q2502.8 -515.4 2502.8 -415.4L2346.2 -415.4Q2346.2 -463.5 2336.8 -497.1Q2327.4 -530.7 2306.8 -548Q2286.2 -565.4 2252.8 -565.4Q2214.8 -565.4 2191.3 -545.7Q2167.8 -526.1 2157.5 -487Q2147.2 -447.9 2147.2 -389L2147.2 -297.5Q2147.2 -238.3 2157.6 -199.4Q2168.1 -160.5 2191.1 -141.2Q2214.1 -122 2251.9 -122Q2286.2 -122 2308 -138.6Q2329.7 -155.2 2340 -188Q2350.3 -220.9 2350.3 -269.1L2502.5 -269.1Q2502.5 -171.2 2472.7 -109Q2443 -46.9 2387.1 -17.5Q2331.2 12 2251.8 12ZM2590.5 0L2590.5 -687.4L2752.2 -687.4L2752.2 0ZM2863.5 0L2863.5 -687.4L3013.8 -687.4L3165.3 -395.8Q3169.8 -386.9 3176.1 -374.4Q3182.4 -361.8 3188.7 -348.3Q3195 -334.7 3198.8 -322.9L3203.8 -323.3Q3203.3 -343.1 3203.3 -362.4Q3203.3 -381.7 3203.3 -395.8L3203.3 -687.4L3356.1 -687.4L3356.1 0L3206.1 0L3049.5 -298.8Q3041.7 -314.9 3034.1 -334.2Q3026.5 -353.5 3020.3 -371.5L3015.6 -371.1Q3016 -353.9 3016 -334.4Q3016 -315 3016 -298.8L3016 0ZM3467.5 0L3467.5 -687.4L3629.2 -687.4L3629.2 0ZM4012.3 0L4012.3 -550.3L3844.4 -550.3L3844.4 -687.4L4340.8 -687.4L4340.8 -550.3L4174 -550.3L4174 0ZM4361.6 0L4545.8 -687.4L4756.1 -687.4L4940.8 0L4769.9 0L4740.4 -124.7L4555.8 -124.7L4526.9 0ZM4583.1 -254.3L4713.5 -254.3L4676.2 -424.6Q4674.2 -433.5 4671.2 -447.7Q4668.3 -461.9 4665 -479Q4661.7 -496.1 4658.3 -513.2Q4654.9 -530.3 4652.1 -544.2L4644.8 -544.2Q4641.8 -526.7 4637.5 -504.6Q4633.1 -482.4 4628.8 -461.1Q4624.4 -439.8 4620.7 -424.6ZM4998.5 0L4998.5 -687.4L5148.8 -687.4L5300.3 -395.8Q5304.8 -386.9 5311.1 -374.4Q5317.4 -361.8 5323.7 -348.3Q5330 -334.7 5333.8 -322.9L5338.8 -323.3Q5338.3 -343.1 5338.3 -362.4Q5338.3 -381.7 5338.3 -395.8L5338.3 -687.4L5491.1 -687.4L5491.1 0L5341.1 0L5184.5 -298.8Q5176.7 -314.9 5169.1 -334.2Q5161.5 -353.5 5155.3 -371.5L5150.6 -371.1Q5151 -353.9 5151 -334.4Q5151 -315 5151 -298.8L5151 0Z", "outer": ["M56.1 0L56.1 -687.4L285.4 -687.4L350.9 -379.9Q354.3 -363.9 359.2 -338.1Q364.2 -312.2 369.5 -285.1Q374.7 -258 378.5 -236.1L386.6 -236.1Q389.5 -253 394 -277.6Q398.5 -302.3 403.5 -329.1Q408.4 -355.9 412.6 -379.4L477.4 -687.4L701.9 -687.4L701.9 0L546.9 0L546.9 -298.4Q546.9 -336.3 548 -372.3Q549.1 -408.2 550.4 -436.7Q551.8 -465.2 551.8 -479.1L544 -479.1Q542.1 -466.7 537.9 -446.7Q533.6 -426.8 529.3 -406.1Q525 -385.4 520.9 -369.7L440 0L313 0L232 -369.5Q229.1 -382.8 224.8 -402.3Q220.4 -421.9 216.5 -442.8Q212.6 -463.6 209.3 -478.9L201.9 -478.9Q203.2 -457.5 204.1 -426.4Q205 -395.3 205.8 -361.8Q206.5 -328.3 206.5 -298.4L206.5 0Z", "M760.6 0L944.8 -687.4L1155.1 -687.4L1339.8 0L1168.9 0L1139.4 -124.7L954.8 -124.7L925.9 0Z", "M1397.5 0L1397.5 -687.4L1547.8 -687.4L1699.3 -395.8Q1703.8 -386.9 1710.1 -374.4Q1716.4 -361.8 1722.7 -348.3Q1729 -334.7 1732.8 -322.9L1737.8 -323.3Q1737.3 -343.1 1737.3 -362.4Q1737.3 -381.7 1737.3 -395.8L1737.3 -687.4L1890.1 -687.4L1890.1 0L1740.1 0L1583.5 -298.8Q1575.7 -314.9 1568.1 -334.2Q1560.5 -353.5 1554.3 -371.5L1549.6 -371.1Q1550 -353.9 1550 -334.4Q1550 -315 1550 -298.8L1550 0Z", "M2251.8 12Q2159.2 12 2099.4 -26.4Q2039.6 -64.7 2011 -143.7Q1982.3 -222.8 1982.3 -344.2Q1982.3 -525.6 2051.3 -612.7Q2120.2 -699.7 2258.4 -699.7Q2334.7 -699.7 2389.3 -670.4Q2443.9 -641 2473.3 -578.2Q2502.8 -515.4 2502.8 -415.4L2346.2 -415.4Q2346.2 -463.5 2336.8 -497.1Q2327.4 -530.7 2306.8 -548Q2286.2 -565.4 2252.8 -565.4Q2214.8 -565.4 2191.3 -545.7Q2167.8 -526.1 2157.5 -487Q2147.2 -447.9 2147.2 -389L2147.2 -297.5Q2147.2 -238.3 2157.6 -199.4Q2168.1 -160.5 2191.1 -141.2Q2214.1 -122 2251.9 -122Q2286.2 -122 2308 -138.6Q2329.7 -155.2 2340 -188Q2350.3 -220.9 2350.3 -269.1L2502.5 -269.1Q2502.5 -171.2 2472.7 -109Q2443 -46.9 2387.1 -17.5Q2331.2 12 2251.8 12Z", "M2590.5 0L2590.5 -687.4L2752.2 -687.4L2752.2 0Z", "M2863.5 0L2863.5 -687.4L3013.8 -687.4L3165.3 -395.8Q3169.8 -386.9 3176.1 -374.4Q3182.4 -361.8 3188.7 -348.3Q3195 -334.7 3198.8 -322.9L3203.8 -323.3Q3203.3 -343.1 3203.3 -362.4Q3203.3 -381.7 3203.3 -395.8L3203.3 -687.4L3356.1 -687.4L3356.1 0L3206.1 0L3049.5 -298.8Q3041.7 -314.9 3034.1 -334.2Q3026.5 -353.5 3020.3 -371.5L3015.6 -371.1Q3016 -353.9 3016 -334.4Q3016 -315 3016 -298.8L3016 0Z", "M3467.5 0L3467.5 -687.4L3629.2 -687.4L3629.2 0Z", "M4012.3 0L4012.3 -550.3L3844.4 -550.3L3844.4 -687.4L4340.8 -687.4L4340.8 -550.3L4174 -550.3L4174 0Z", "M4361.6 0L4545.8 -687.4L4756.1 -687.4L4940.8 0L4769.9 0L4740.4 -124.7L4555.8 -124.7L4526.9 0Z", "M4998.5 0L4998.5 -687.4L5148.8 -687.4L5300.3 -395.8Q5304.8 -386.9 5311.1 -374.4Q5317.4 -361.8 5323.7 -348.3Q5330 -334.7 5333.8 -322.9L5338.8 -323.3Q5338.3 -343.1 5338.3 -362.4Q5338.3 -381.7 5338.3 -395.8L5338.3 -687.4L5491.1 -687.4L5491.1 0L5341.1 0L5184.5 -298.8Q5176.7 -314.9 5169.1 -334.2Q5161.5 -353.5 5155.3 -371.5L5150.6 -371.1Q5151 -353.9 5151 -334.4Q5151 -315 5151 -298.8L5151 0Z"], "house": "M2773.5 -793.0 L3276.4 -369.5 L3144.1 -369.5 L3144.1 107.0 L2905.9 107.0 L2905.9 -157.7 L2641.1 -157.7 L2641.1 107.0 L2402.9 107.0 L2402.9 -369.5 L2270.6 -369.5 Z", "strips": ["M2373.2 -455.9 L2373.2 -369.5 L2270.6 -369.5 Z", "M2369.2 -452.5 L2473.8 -540.6 L2473.8 107.0 L2402.9 107.0 L2402.9 -369.5 L2369.2 -369.5 Z", "M2469.8 -537.2 L2574.3 -625.3 L2574.3 107.0 L2469.8 107.0 Z", "M2570.3 -621.9 L2674.9 -710.0 L2674.9 -157.7 L2641.1 -157.7 L2641.1 107.0 L2570.3 107.0 Z", "M2670.9 -706.6 L2773.5 -793.0 L2775.5 -791.3 L2775.5 -157.7 L2670.9 -157.7 Z", "M2771.5 -791.3 L2773.5 -793.0 L2876.1 -706.6 L2876.1 -157.7 L2771.5 -157.7 Z", "M2872.1 -710.0 L2976.7 -621.9 L2976.7 107.0 L2905.9 107.0 L2905.9 -157.7 L2872.1 -157.7 Z", "M2972.7 -625.3 L3077.2 -537.2 L3077.2 107.0 L2972.7 107.0 Z", "M3073.2 -540.6 L3177.8 -452.5 L3177.8 -369.5 L3144.1 -369.5 L3144.1 107.0 L3073.2 107.0 Z", "M3173.8 -455.9 L3276.4 -369.5 L3173.8 -369.5 Z"]};
  let settled = onHome, hover = false, focus = false, setState;

  if (label && label.textContent.trim() === 'Mancini Tan' && window.flubber) {
    // ---- Vector morph ----
    el.classList.add('nm-vec');
    const pad = 140, ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg'); svg.setAttribute('class', 'nm-v'); svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('viewBox', `0 ${-NM.capH - pad} ${NM.w} ${NM.capH + pad * 2}`);
    svg.style.width = NM.w / 1000 + 'em'; svg.style.height = (NM.capH + pad * 2) / 1000 + 'em';
    const full = document.createElementNS(ns, 'path'); full.setAttribute('d', NM.full);
    const morph = document.createElementNS(ns, 'path'); morph.style.display = 'none';
    svg.append(full, morph); el.appendChild(svg);
    // Each letter, left to right, squeezes into its own slice of the house, so the name folds up in order
    morph.remove(); const parts = NM.outer.map((d, i) => { const p = document.createElementNS(ns, 'path'); p.style.display = 'none'; svg.appendChild(p);
      return { p, f: window.flubber.interpolate(d, NM.strips[i], { maxSegmentLength: 24 }) }; });
    const solid = document.createElementNS(ns, 'path'); solid.setAttribute('d', NM.house); solid.style.display = 'none'; svg.appendChild(solid);
    const HOME_W = 44;
    let fullW = 0, t = 0, target = 0, raf = 0, from = 0, t0 = 0;
    const DUR = 620;
    // ease in-out, with a soft settle at the very end
    const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
    const measure = () => { fullW = svg.getBoundingClientRect().width + parseFloat(getComputedStyle(el).fontSize) * 2.2; render(); };
    const render = () => {
      el.style.width = (fullW + (HOME_W - fullW) * t).toFixed(1) + 'px';
      const atRest = t <= 0.0005, atHome = t >= 0.9995;
      full.style.display = atRest ? '' : 'none'; solid.style.display = atHome ? '' : 'none';
      parts.forEach(o => { o.p.style.display = atRest || atHome ? 'none' : ''; if (!atRest && !atHome) o.p.setAttribute('d', o.f(t)); });
    };
    const tick = now => { const k = Math.min(1, (now - t0) / DUR); t = from + (target - from) * ease(k); render();
      raf = k < 1 ? requestAnimationFrame(tick) : 0; };
    setState = home => { const nt = home ? 1 : 0; el.classList.toggle('home', home); if (nt === target) return; target = nt;
      if (still.matches) { t = target; render(); return; }
      from = t; t0 = performance.now(); if (!raf) raf = requestAnimationFrame(tick); };
    measure();
    if (document.fonts) document.fonts.ready.then(measure);
    addEventListener('resize', measure);
  } else {
    // ---- Letters fold into the house (non-Latin names) ----
    if (label && !label.querySelector('.ch')) { const txt = label.textContent; label.textContent = '';
      [...txt].forEach(c => { const s = document.createElement('span'); s.className = 'ch'; s.textContent = c; s.setAttribute('aria-hidden', 'true'); label.appendChild(s); }); }
    const chars = label ? [...label.querySelectorAll('.ch')] : [];
    const measure = () => { const was = el.classList.contains('home'); el.style.transition = 'none'; chars.forEach(c => c.style.transition = 'none');
      el.classList.remove('home'); el.style.width = 'auto';
      const w = el.offsetWidth, box = el.getBoundingClientRect(), mid = box.left + box.width / 2, n = chars.length, c0 = (n - 1) / 2;
      chars.forEach((c, i) => { const r = c.getBoundingClientRect(); c.style.setProperty('--dx', (mid - (r.left + r.width / 2)).toFixed(1) + 'px');
        c.style.setProperty('--rot', ((i - c0) * 9).toFixed(0) + 'deg'); c.style.setProperty('--k', Math.abs(i - c0).toFixed(1)); c.style.setProperty('--o', (c0 - Math.abs(i - c0)).toFixed(1)); });
      el.style.width = ''; el.style.setProperty('--nm-w', w + 'px'); el.classList.toggle('home', was); el.offsetWidth;
      el.style.transition = ''; chars.forEach(c => c.style.transition = ''); };
    setState = home => el.classList.toggle('home', home);
    measure(); if (document.fonts) document.fonts.ready.then(measure); addEventListener('resize', measure);
  }

  const update = () => setState((onHome ? scrollY > 40 : settled) && !hover && !focus);
  update();
  if (onHome) { let tk = 0; addEventListener('scroll', () => { if (tk) return; tk = requestAnimationFrame(() => { tk = 0; update(); }); }, { passive: true }); }
  else setTimeout(() => { settled = true; update(); }, 1400);
  el.addEventListener('mouseenter', () => { if (canHover.matches) { hover = true; update(); } });
  el.addEventListener('mouseleave', () => { hover = false; update(); });
  el.addEventListener('focus', () => { if (el.matches(':focus-visible')) { focus = true; update(); } });
  el.addEventListener('blur', () => { focus = false; update(); });
})();
