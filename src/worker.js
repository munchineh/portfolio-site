// Sends first-time visitors to their language, then gets out of the way.
// A manual pick in the menu sets a `lang` cookie, which always wins.
const LOCALES = ['de', 'ko', 'zh-hans', 'zh-hant'];
const BY_COUNTRY = { HK: 'zh-hant', TW: 'zh-hant', DE: 'de', KR: 'ko' };
const PAGE = /^\/(?:(?:index|evn|okx|buildlr|ninjavan|neuron)(?:\.html)?)?$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if ((request.method === 'GET' || request.method === 'HEAD') && PAGE.test(url.pathname)) {
      const cookie = (request.headers.get('Cookie') || '').match(/(?:^|;\s*)lang=([a-z-]+)/);
      const want = cookie ? cookie[1] : (BY_COUNTRY[request.cf && request.cf.country] || 'en');
      if (LOCALES.includes(want)) {
        url.pathname = `/${want}${url.pathname}`;
        return new Response(null, { status: 302, headers: { Location: url.toString(), 'Cache-Control': 'no-store', Vary: 'Cookie' } });
      }
      const res = await env.ASSETS.fetch(request);
      const out = new Response(res.body, res);
      out.headers.set('Vary', 'Cookie');
      return out;
    }
    return env.ASSETS.fetch(request);
  },
};
