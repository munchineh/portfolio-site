/* Search across the portfolio, in the page's language.
   Two layers:
   1. Tools and skills (search/<lang>.json): short answers for things recruiters look for, like Figma or Salesforce,
      each pointing to where it shows up. Kept by hand, from the cases and the résumé.
   2. Everything written on the site: the same-language pages are fetched on first use and split into sections,
      so copy edits show up in search without a build step.
   Loaded by site.js on first use; exposes window.MTSearch.open(). */
(() => {
  if (window.MTSearch) return;
  const LANG = (document.documentElement.lang || 'en').toLowerCase();
  const DIR = { en: '', de: 'de/', ko: 'ko/', 'zh-hans': 'zh-hans/', 'zh-hant': 'zh-hant/' }[LANG] ?? '';
  const ROOT = new URL('.', document.currentScript.src);          // site root (search.js sits next to site.js)
  const PAGES = ['index', 'evn', 'okx', 'buildlr', 'ninjavan', 'neuron', 'podcast'];
  const VERSION = 5;                                              // bump to drop cached indexes
  const pageURL = (p) => new URL(`${DIR}${p}.html`, ROOT).href;

  const STR = {
    en: { label: 'Search my work', ph: 'Search tools, skills or projects', close: 'Close', try: 'Try', tools: 'Tools and skills',
          work: 'In the work', none: (q) => `Nothing here for “${q}” yet. I'm happy to answer it by email.`, mail: 'Email me',
          loading: 'Loading the cases…', failed: "Couldn't load the cases. Check your connection and try again.",
          keys: ['to move', 'to open', 'to close'], resume: 'Résumé', home: 'Home', about: 'About' },
    de: { label: 'Meine Arbeit durchsuchen', ph: 'Tools, Skills oder Projekte suchen', close: 'Schließen', try: 'Zum Beispiel', tools: 'Tools und Skills',
          work: 'In den Projekten', none: (q) => `Zu „${q}“ gibt es hier noch nichts. Ich beantworte die Frage gern per E-Mail.`, mail: 'E-Mail schreiben',
          loading: 'Projekte werden geladen…', failed: 'Die Projekte ließen sich nicht laden. Verbindung prüfen und noch einmal versuchen.',
          keys: ['auswählen', 'öffnen', 'schließen'], resume: 'Lebenslauf', home: 'Start', about: 'Über mich' },
    ko: { label: '작업 검색', ph: '툴, 스킬, 프로젝트 검색', close: '닫기', try: '추천 검색어', tools: '툴과 스킬',
          work: '프로젝트에서', none: (q) => `아직 “${q}”에 대한 내용이 없어요. 이메일로 물어봐 주시면 기꺼이 답해 드릴게요.`, mail: '문의하기',
          loading: '프로젝트를 불러오는 중…', failed: '프로젝트를 불러오지 못했어요. 연결을 확인하고 다시 시도해 주세요.',
          keys: ['이동', '열기', '닫기'], resume: '이력서', home: '홈', about: '소개' },
    'zh-hans': { label: '搜索作品', ph: '搜索工具、技能或作品', close: '关闭', try: '试试', tools: '工具与技能',
          work: '作品中', none: (q) => `暂时没有“${q}”的相关内容，欢迎发邮件问我。`, mail: '发个邮件',
          loading: '正在加载作品…', failed: '作品加载失败，请检查网络后重试。',
          keys: ['选择', '打开', '关闭'], resume: '简历', home: '首页', about: '关于' },
    'zh-hant': { label: '搜尋作品', ph: '搜尋工具、技能或作品', close: '關閉', try: '試試看', tools: '工具與技能',
          work: '作品中', none: (q) => `目前還沒有「${q}」的相關內容，歡迎寄信問我。`, mail: '寄封信',
          loading: '正在載入作品…', failed: '作品載入失敗，請檢查網路後再試一次。',
          keys: ['選擇', '開啟', '關閉'], resume: '履歷', home: '首頁', about: '關於' },
  };
  const S = STR[LANG] || STR.en;

  /* Matching ignores case and accents, and treats British and American spellings the same. Length stays the same,
     so match positions line up with the original text for highlighting. */
  const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').normalize('NFC')
    .replace(/[’‘]/g, "'").replace(/(locali|organi|personali|customi|visuali|prioriti|optimi|summari|internationali)s/g, '$1z');
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const clean = (s) => s.replace(/\s+/g, ' ').trim();

  /* ---------- Index ---------- */
  const SKIP = '.demo, .demo-tag, .demo-note, .demo-vid, svg, script, style, video, audio, .no, .ch-no, [aria-hidden="true"], .btns, .crumbs, .c-head h1';   // the case title is already the result's heading
  const textOf = (el) => {
    const c = el.cloneNode(true);
    c.querySelectorAll(SKIP).forEach((n) => n.remove());
    c.querySelectorAll('*').forEach((n) => n.append(' '));   // keep words in separate elements apart (chips, labels, cells)
    return clean(c.textContent).replace(/ ([,.;:!?)\]%])/g, '$1').replace(/([(\[]) /g, '$1');
  };
  const indexPage = (doc, page) => {
    const label = clean((doc.querySelector('.crumbs .chip:not(.back)') || {}).textContent || (page === 'index' ? S.home : ''));
    const title = clean(doc.title.split('·')[0]);
    const units = window.mtUnits(doc);
    let chapter = '';
    return units.map((s, i) => {
      const id = s.id || 's' + (i + 1);
      if (s.matches('.chapter')) chapter = clean((s.querySelector('h2') || {}).textContent || '');
      const h = s.querySelector('.sh h2') || s.querySelector('h2') || s.querySelector('h1');
      let head = s.matches('.c-hero') ? title : clean(h ? h.textContent : (s.getAttribute('aria-label') || ''));
      if (page === 'index') {   // Home's sections are named after the menu's own links, so they match the page's language
        const nav = (sel, alt) => clean((doc.querySelector(sel) || {}).textContent || alt);
        head = s.matches('.hero') ? nav('.menu .links a .t', S.home) : s.id === 'about' ? nav('.menu a[href*="#about"] .t', S.about) : clean(s.getAttribute('aria-label') || head);
      }
      const sub = [label || title, s.matches('.sec') && chapter && chapter !== head ? chapter : ''].filter(Boolean).join(' · ');
      return { page, id, head, sub, text: textOf(s) };
    }).filter((u) => u.text);
  };

  let data = null, dataP = null;
  const KEY = `mt-search-${VERSION}-${LANG}`;
  const loadAll = () => dataP || (dataP = (async () => {
    try { const c = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (c) return (data = c); } catch (e) {}
    const toolsP = fetch(new URL(`search/${LANG}.json`, ROOT)).then((r) => r.ok ? r.json() : fetch(new URL('search/en.json', ROOT)).then((r) => r.json()));
    const parse = new DOMParser();
    const pages = await Promise.all(PAGES.map(async (p) => {
      const r = await fetch(pageURL(p), { credentials: 'same-origin' });
      if (!r.ok) return [];
      return indexPage(parse.parseFromString(await r.text(), 'text/html'), p);
    }));
    const tools = await toolsP;
    data = { tools: tools.tools || [], suggest: tools.suggest || [], units: pages.flat() };
    data.units.forEach((u) => { u.nh = norm(u.head); u.ns = norm(u.sub); u.nt = norm(u.text); });
    try { sessionStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {}
    return data;
  })().catch((e) => { dataP = null; throw e; }));

  /* ---------- Search ---------- */
  const termsOf = (q) => norm(q).split(/[\s,，、]+/).filter(Boolean);
  const findTools = (q, terms) => {
    const nq = norm(q).trim();
    return data.tools.map((t) => {
      const names = [t.name, ...(t.aka || [])].map(norm);
      let score = 0;
      names.forEach((n) => {
        if (n === nq) score = Math.max(score, 10);
        else if (n.startsWith(nq) && nq.length > 1) score = Math.max(score, 6);
        else if (nq.length > 2 && n.includes(nq)) score = Math.max(score, 3);
        else if (n.length > 2 && (' ' + nq + ' ').includes(' ' + n + ' ')) score = Math.max(score, 5);
      });
      if (!score && terms.length > 1 && terms.every((w) => names.some((n) => n.includes(w)))) score = 2;
      return { t, score };
    }).filter((x) => x.score).sort((a, b) => b.score - a.score).slice(0, 3).map((x) => x.t);
  };
  const findUnits = (q, terms) => {
    const nq = norm(q).trim();
    return data.units.map((u) => {
      const all = u.nh + ' ' + u.ns + ' ' + u.nt;
      if (!terms.every((w) => all.includes(w))) return null;
      let score = 0;
      terms.forEach((w) => {
        if (u.nh.includes(w)) score += 6;
        if (u.ns.includes(w)) score += 3;
        let n = 0; for (let i = u.nt.indexOf(w); i > -1 && n < 5; i = u.nt.indexOf(w, i + w.length)) n++;
        score += n;
      });
      if (terms.length > 1 && all.includes(nq)) score += 4;
      return { u, score };
    }).filter(Boolean).sort((a, b) => b.score - a.score).slice(0, 8).map((x) => x.u);
  };
  const mark = (s, terms) => {
    const n = norm(s), hits = [];
    terms.forEach((w) => { for (let i = n.indexOf(w); i > -1; i = n.indexOf(w, i + w.length)) hits.push([i, i + w.length]); });
    hits.sort((a, b) => a[0] - b[0]);
    let out = '', at = 0;
    hits.forEach(([a, b]) => { if (a < at) return; out += esc(s.slice(at, a)) + '<mark>' + esc(s.slice(a, b)) + '</mark>'; at = b; });
    return out + esc(s.slice(at));
  };
  const snippet = (u, terms) => {
    let i = -1; for (const w of terms) { i = u.nt.indexOf(w); if (i > -1) break; }
    if (i < 0) return u.text.slice(0, 140) + (u.text.length > 140 ? '…' : '');
    const cjk = /[　-鿿가-힯]/.test(u.text);
    let a = Math.max(0, i - (cjk ? 24 : 60)), b = Math.min(u.text.length, i + (cjk ? 70 : 120));
    if (!cjk) {
      if (a > 0) { const sp = u.text.indexOf(' ', a); if (sp > -1 && sp < i) a = sp + 1; }
      if (b < u.text.length) { const sp = u.text.lastIndexOf(' ', b); if (sp > i) b = sp; }
    }
    return (a > 0 ? '…' : '') + u.text.slice(a, b) + (b < u.text.length ? '…' : '');
  };
  /* A tools-and-skills link names a page and a phrase on it; it opens the first section with that phrase */
  const linkFor = (l) => {
    if (l.to === 'resume') return { href: new URL('Mancini_Tan_Resume.pdf', ROOT).href, label: S.resume, file: true };
    let id = l.id;
    if (!id && l.find) {
      const f = norm(l.find), u = data.units.find((x) => x.page === l.to && (x.nh + ' ' + x.nt).includes(f));
      id = u && u.id;
    }
    return { href: pageURL(l.to) + (id ? '#' + id : ''), label: l.label, terms: l.find ? [norm(l.find)] : null };
  };

  /* ---------- UI ---------- */
  let dlg, input, list, foot, active = -1, opts = [], lastTerms = [];
  const build = () => {
    dlg = document.createElement('dialog');
    dlg.className = 'srch';
    dlg.setAttribute('aria-label', S.label);
    dlg.innerHTML = `
      <div class="srch-bar">
        <svg viewBox="0 0 16 16" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="7" cy="7" r="4.75"/><path d="m10.5 10.5 3.5 3.5"/></svg>
        <input type="search" role="combobox" aria-expanded="true" aria-controls="srchList" aria-autocomplete="list"
               autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" placeholder="${esc(S.ph)}" aria-label="${esc(S.label)}">
        <button type="button" class="srch-x" aria-label="${esc(S.close)}"><kbd aria-hidden="true">Esc</kbd><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="m4 4 8 8M12 4l-8 8"/></svg></button>
      </div>
      <div class="srch-body" id="srchList" role="listbox" aria-label="${esc(S.label)}"></div>
      <div class="srch-foot" aria-hidden="true"><span><kbd>↑</kbd><kbd>↓</kbd> ${esc(S.keys[0])}</span><span><kbd>↵</kbd> ${esc(S.keys[1])}</span><span><kbd>Esc</kbd> ${esc(S.keys[2])}</span></div>`;
    document.body.appendChild(dlg);
    input = dlg.querySelector('input'); list = dlg.querySelector('.srch-body'); foot = dlg.querySelector('.srch-foot');
    dlg.querySelector('.srch-x').addEventListener('click', hide);
    dlg.addEventListener('cancel', (e) => { e.preventDefault(); hide(); });   // Esc folds the sheet back into the button
    dlg.addEventListener('pointerdown', (e) => { if (e.target === dlg && outside(e)) hide(); });   // tap outside the sheet
    addEventListener('resize', () => { if (dlg.open && dlg.classList.contains('on')) place(); });
    let t;
    input.addEventListener('input', () => { clearTimeout(t); t = setTimeout(render, 60); });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); move(e.key === 'ArrowDown' ? 1 : -1); }
      else if (e.key === 'Escape') { e.preventDefault(); hide(); }   // a search field would only clear itself on Esc
      else if (e.key === 'Enter') { const o = opts[active] || opts[0]; if (o) { e.preventDefault(); o.click(); } }
    });
    list.addEventListener('click', (e) => {
      const chip = e.target.closest('[data-q]');
      if (chip) { input.value = chip.dataset.q; render(); input.focus(); return; }
      const a = e.target.closest('a[role="option"]');
      if (!a) return;
      const terms = a.dataset.terms ? JSON.parse(a.dataset.terms) : lastTerms;
      try { sessionStorage.setItem('mt-hl', JSON.stringify(terms)); } catch (er) {}
      const to = new URL(a.href);
      if (to.pathname === location.pathname && to.hash) {       // same page: close and let the hash move us
        e.preventDefault(); dlg.classList.remove('on'); dlg.close();
        if (location.hash === to.hash) dispatchEvent(new HashChangeEvent('hashchange')); else location.hash = to.hash;
      } else { dlg.classList.remove('on'); dlg.close(); }
    });
    list.addEventListener('pointermove', (e) => { const a = e.target.closest('[role="option"]'); if (a) setActive(opts.indexOf(a), false); });
  };
  const setActive = (i, scroll = true) => {
    opts.forEach((o, j) => o.classList.toggle('on', j === i));
    active = i;
    if (opts[i]) { input.setAttribute('aria-activedescendant', opts[i].id); if (scroll) opts[i].scrollIntoView({ block: 'nearest' }); }
    else input.removeAttribute('aria-activedescendant');
  };
  const move = (d) => { if (!opts.length) return; setActive((active + d + opts.length) % opts.length); };

  const render = () => {
    const q = input.value.trim();
    if (!data) {
      list.innerHTML = `<p class="srch-msg">${esc(S.loading)}</p>`;
      loadAll().then(render, () => { list.innerHTML = `<p class="srch-msg">${esc(S.failed)}</p>`; });
      return;
    }
    let html = '';
    if (!q) {
      html = `<div class="srch-try"><span>${esc(S.try)}</span>${data.suggest.map((s) => `<button type="button" class="srch-chip" data-q="${esc(s)}">${esc(s)}</button>`).join('')}</div>`;
    } else {
      const terms = lastTerms = termsOf(q);
      const tools = findTools(q, terms), units = findUnits(q, terms);
      let n = 0;
      if (tools.length) {
        html += `<div class="srch-grp">${esc(S.tools)}</div>` + tools.map((t) => `
          <div class="srch-tool"><div class="srch-tool-h"><b>${mark(t.name, terms)}</b>${t.kind ? `<span>${esc(t.kind)}</span>` : ''}</div>
            <p>${esc(t.note)}</p>
            <div class="srch-links">${(t.links || []).map(linkFor).map((l) => `<a role="option" id="so${n++}" href="${esc(l.href)}"${l.file ? ' download' : ''}${l.terms ? ` data-terms='${esc(JSON.stringify(l.terms))}'` : ''}>${esc(l.label)}<svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">${l.file ? '<path d="M8 2.5v8.5M4.5 7.5 8 11l3.5-3.5M3 13.5h10"/>' : '<path d="M3 8h10M9 4l4 4-4 4"/>'}</svg></a>`).join('')}</div>
          </div>`).join('');
      }
      if (units.length) {
        html += `<div class="srch-grp">${esc(S.work)}</div>` + units.map((u) => `
          <a class="srch-hit" role="option" id="so${n++}" href="${esc(pageURL(u.page) + '#' + u.id)}">
            <b>${mark(u.head, terms)}</b><span class="srch-sub">${mark(u.sub, terms)}</span>
            <span class="srch-snip">${mark(snippet(u, terms), terms)}</span>
          </a>`).join('');
      }
      if (!tools.length && !units.length) {
        html = `<div class="srch-none"><p>${esc(S.none(q))}</p><a class="btn" href="mailto:mancini.tan@gmail.com?subject=${encodeURIComponent(q)}">${esc(S.mail)}</a></div>`;
      }
    }
    list.innerHTML = html;
    opts = [...list.querySelectorAll('[role="option"]')];
    setActive(q && opts.length ? 0 : -1, false);
    list.scrollTop = 0;
  };

  /* The sheet takes the open menu's box (the menu is always laid out at its open size and revealed with
     clip-path), so both land on the same spot on the page grid. It unfolds out of the search button. */
  const still = matchMedia('(prefers-reduced-motion: reduce)');
  const btn = () => document.querySelector('.srch-btn');
  const place = () => {
    const m = document.querySelector('.menu');
    const r = m ? m.getBoundingClientRect() : { left: 11, top: 11, width: Math.min(innerWidth - 22, 422), height: Math.min(innerHeight - 22, 642) };
    Object.assign(dlg.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' });
    const b = btn(), k = b ? b.getBoundingClientRect() : { top: r.top, left: r.left + r.width - 44, right: r.left + r.width, bottom: r.top + 44 };
    const px = (n) => Math.max(0, Math.round(n)) + 'px';
    dlg.style.setProperty('--from', `inset(${px(k.top - r.top)} ${px(r.left + r.width - k.right)} ${px(r.top + r.height - k.bottom)} ${px(k.left - r.left)} round 22px)`);
    return r;
  };
  const outside = (e) => { const r = dlg.getBoundingClientRect(); return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom; };
  let closing;
  function hide() {
    if (!dlg || !dlg.open || closing) return;
    place();
    dlg.classList.remove('on');
    const done = () => { clearTimeout(closing); closing = null; dlg.close(); };
    if (still.matches) { done(); return; }
    closing = setTimeout(done, 420);
  }

  window.MTSearch = {
    open(q) {
      if (!dlg) build();
      if (closing) { clearTimeout(closing); closing = null; }
      if (dlg.open) { dlg.classList.add('on'); input.focus(); return; }
      if (typeof q === 'string') input.value = q;
      if (document.body.classList.contains('menu-open')) document.getElementById('toggle').click();
      place();
      dlg.showModal();
      void dlg.offsetWidth;            // start from the button's shape, then unfold
      dlg.classList.add('on');
      input.focus({ preventScroll: true }); input.select();
      render();
    },
  };
  loadAll().catch(() => {});
})();
