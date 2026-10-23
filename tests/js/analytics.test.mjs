import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readSite, runInSandbox } from './helpers.mjs';

const CODE = readSite('analytics.js');
const PHONE = '6289680858462';

function setup({ config, dnt = null, gpc = false, pathname = '/blog/post.html', hasArticle = false, countThrows = false } = {}) {
  const listeners = { document: {}, window: {} };
  const appended = [];
  const counted = [];
  const intervals = [];
  const article = hasArticle ? { bottom: 2000 } : null;
  const doc = {
    visibilityState: 'visible',
    head: { appendChild: (el) => appended.push(el) },
    createElement: () => ({ attrs: {}, setAttribute(k, v) { this.attrs[k] = v; } }),
    addEventListener: (t, fn) => (listeners.document[t] = fn),
    querySelector: (sel) => (sel === '[data-track-article]' ? article : null),
  };
  if (article) article.getBoundingClientRect = () => ({ bottom: article.bottom });
  const win = {
    BC_ANALYTICS_CONFIG: config,
    location: { pathname, search: '?secret=1', hash: '#frag' },
    innerHeight: 800,
    addEventListener: (t, fn) => (listeners.window[t] = fn),
  };
  const sandbox = {
    window: win,
    document: doc,
    navigator: { doNotTrack: dnt, globalPrivacyControl: gpc },
    setInterval: (fn) => { intervals.push(fn); return intervals.length; },
    clearInterval: () => {},
    console: { warn() {} },
  };
  runInSandbox(CODE, sandbox);
  const loadScript = () => {
    win.goatcounter = {
      count: (payload) => {
        if (countThrows) throw new Error('provider down');
        counted.push(payload);
      },
    };
    appended[0] && appended[0].onload && appended[0].onload();
  };
  const click = (attrs) => {
    let prevented = false;
    const el = { getAttribute: (k) => attrs[k] ?? null };
    listeners.document.click({ target: { closest: (s) => (s === '[data-track]' ? el : null) }, preventDefault: () => (prevented = true) });
    return { prevented };
  };
  return { listeners, appended, counted, intervals, win, doc, article, loadScript, click };
}

const ON = { enabled: true, provider: 'goatcounter', goatcounterCode: 'bangunancerdas' };

test('analytics is off by default: no listeners, no network, no script tags', () => {
  const t = setup();
  assert.deepEqual(t.listeners.document, {});
  assert.deepEqual(t.listeners.window, {});
  assert.equal(t.appended.length, 0);
});

test('enabling without a provider code stays off', () => {
  const t = setup({ config: { enabled: true, provider: 'goatcounter', goatcounterCode: '' } });
  assert.equal(t.appended.length, 0);
});

test('provider code must be a plain subdomain label (no URL injection)', () => {
  for (const code of ['evil.com/x', 'a b', '../x', 'a.b', 'x?y']) {
    const t = setup({ config: { ...ON, goatcounterCode: code } });
    assert.equal(t.appended.length, 0, code);
  }
});

test('Do Not Track and Global Privacy Control disable analytics', () => {
  assert.equal(setup({ config: ON, dnt: '1' }).appended.length, 0);
  assert.equal(setup({ config: ON, gpc: true }).appended.length, 0);
});

test('enabled: loads the provider script asynchronously from the configured account only', () => {
  const t = setup({ config: ON });
  assert.equal(t.appended.length, 1);
  const s = t.appended[0];
  assert.equal(s.async, true);
  assert.equal(s.src, 'https://gc.zgo.at/count.js');
  assert.equal(s.attrs['data-goatcounter'], 'https://bangunancerdas.goatcounter.com/count');
});

test('whatsapp click sends only event, cta id and path - never number, message or query', () => {
  const t = setup({ config: ON });
  t.loadScript();
  const { prevented } = t.click({
    'data-track': 'whatsapp_click',
    'data-cta-id': 'hero',
    href: `https://wa.me/${PHONE}?text=Halo%20Bangunan%20Cerdas`,
  });
  assert.equal(prevented, false, 'native navigation must not be blocked');
  assert.equal(t.counted.length, 1);
  const serialized = JSON.stringify(t.counted[0]);
  assert.equal(t.counted[0].event, true);
  assert.equal(t.counted[0].path, 'whatsapp_click/hero');
  assert.equal(t.counted[0].title, '/blog/post.html');
  assert.deepEqual(Object.keys(t.counted[0]).sort(), ['event', 'path', 'title']);
  for (const forbidden of [PHONE, '62896', 'Halo', 'secret', 'frag', 'wa.me']) {
    assert.ok(!serialized.includes(forbidden), `payload leaks ${forbidden}: ${serialized}`);
  }
});

test('service and portfolio events are supported; unknown events and bad ids are dropped', () => {
  const t = setup({ config: ON });
  t.loadScript();
  t.click({ 'data-track': 'service_cta_click', 'data-cta-id': 'service-home-assistant' });
  t.click({ 'data-track': 'portfolio_click', 'data-cta-id': 'portfolio-rumah-tinggal' });
  t.click({ 'data-track': 'purchase', 'data-cta-id': 'x' });
  t.click({ 'data-track': 'whatsapp_click', 'data-cta-id': 'Has Spaces & Symbols' });
  t.click({ 'data-track': 'whatsapp_click' });
  assert.deepEqual(t.counted.map((c) => c.path), ['service_cta_click/service-home-assistant', 'portfolio_click/portfolio-rumah-tinggal']);
});

test('provider failures never surface to the page', () => {
  const t = setup({ config: ON, countThrows: true });
  t.loadScript();
  assert.doesNotThrow(() => t.click({ 'data-track': 'whatsapp_click', 'data-cta-id': 'hero' }));
});

test('events fired before the provider loads are queued, then flushed once', () => {
  const t = setup({ config: ON });
  t.click({ 'data-track': 'whatsapp_click', 'data-cta-id': 'hero' });
  assert.equal(t.counted.length, 0);
  t.loadScript();
  assert.deepEqual(t.counted.map((c) => c.path), ['whatsapp_click/hero']);
});

test('queue is bounded so a blocked provider cannot grow memory without limit', () => {
  const t = setup({ config: ON });
  for (let i = 0; i < 500; i++) t.click({ 'data-track': 'whatsapp_click', 'data-cta-id': 'hero' });
  t.loadScript();
  assert.ok(t.counted.length <= 20);
});

test('article_read fires once, only after the end is reached and the minimum time elapsed', () => {
  const t = setup({ config: ON, hasArticle: true });
  t.loadScript();
  assert.equal(t.intervals.length, 1);
  const tick = t.intervals[0];
  for (let i = 0; i < 14; i++) tick();
  assert.equal(t.counted.length, 0, 'too early');
  tick(); // 15 s elapsed, but article bottom is still below the viewport
  assert.equal(t.counted.length, 0, 'end of article not reached');
  t.article.bottom = 700;
  tick();
  tick();
  assert.deepEqual(t.counted.map((c) => c.path), ['article_read/blog-post']);
});

test('article_read does not count time while the tab is hidden', () => {
  const t = setup({ config: ON, hasArticle: true });
  t.loadScript();
  t.article.bottom = 100;
  t.doc.visibilityState = 'hidden';
  for (let i = 0; i < 60; i++) t.intervals[0]();
  assert.equal(t.counted.length, 0);
  t.doc.visibilityState = 'visible';
  for (let i = 0; i < 15; i++) t.intervals[0]();
  assert.equal(t.counted.length, 1);
});

test('no article element means no timers', () => {
  const t = setup({ config: ON });
  assert.equal(t.intervals.length, 0);
});
