import assert from 'node:assert/strict';
import { test } from 'node:test';
import { fakeClassList, inlineThemeScript, publishedPages, readSite, runInSandbox } from './helpers.mjs';

function runInit({ stored, prefersDark = false, storageThrows = false, matchMediaThrows = false } = {}) {
  const classList = fakeClassList(['no-js']);
  runInSandbox(inlineThemeScript(readSite('index.html')), {
    document: { documentElement: { classList } },
    localStorage: {
      getItem() {
        if (storageThrows) throw new Error('blocked');
        return stored ?? null;
      },
    },
    window: {
      matchMedia() {
        if (matchMediaThrows) throw new Error('unsupported');
        return { matches: prefersDark };
      },
    },
  });
  return classList;
}

test('every page uses the identical early theme script', () => {
  const scripts = publishedPages().map((p) => inlineThemeScript(readSite(p)));
  scripts.forEach((s, i) => assert.ok(s, `${publishedPages()[i]} has no early theme script`));
  assert.equal(new Set(scripts).size, 1);
});

test('stored preference wins over system preference', () => {
  assert.ok(runInit({ stored: 'dark', prefersDark: false }).contains('theme-dark'));
  assert.ok(runInit({ stored: 'light', prefersDark: true }).contains('theme-light'));
});

test('system preference is used when nothing is stored', () => {
  assert.ok(runInit({ prefersDark: true }).contains('theme-dark'));
  assert.ok(runInit({ prefersDark: false }).contains('theme-light'));
});

test('an invalid stored value falls back instead of producing an unknown theme class', () => {
  const cl = runInit({ stored: 'purple', prefersDark: true });
  assert.deepEqual(cl.toArray().filter((c) => c.startsWith('theme-')), ['theme-dark']);
});

test('blocked storage falls back to the system preference', () => {
  assert.ok(runInit({ storageThrows: true, prefersDark: true }).contains('theme-dark'));
});

test('missing matchMedia falls back to light', () => {
  assert.ok(runInit({ matchMediaThrows: true }).contains('theme-light'));
});

test('no-js class is always removed', () => {
  for (const opts of [{}, { storageThrows: true }, { matchMediaThrows: true }, { stored: 'x' }]) {
    assert.equal(runInit(opts).contains('no-js'), false);
  }
});

// ---- script.js (toggle + persistence) -----------------------------------
function loadToggle({ withButton = true, setItemThrows = false, startTheme = 'theme-light' } = {}) {
  const classList = fakeClassList([startTheme]);
  const handlers = {};
  const attrs = {};
  const btn = withButton
    ? {
        textContent: '',
        addEventListener: (t, fn) => (handlers[t] = fn),
        setAttribute: (k, v) => (attrs[k] = v),
      }
    : null;
  const year = { textContent: '' };
  const stored = {};
  runInSandbox(readSite('script.js'), {
    document: {
      documentElement: { classList },
      getElementById: (id) => ({ 'theme-toggle': btn, year }[id] || null),
    },
    localStorage: {
      setItem(k, v) {
        if (setItemThrows) throw new Error('quota');
        stored[k] = v;
      },
    },
    Date,
    String,
  });
  return { classList, handlers, btn, stored, year, attrs };
}

test('toggle switches theme, persists it and reflects state accessibly', () => {
  const t = loadToggle();
  assert.equal(t.attrs['aria-pressed'], 'false');
  t.handlers.click();
  assert.ok(t.classList.contains('theme-dark') && !t.classList.contains('theme-light'));
  assert.equal(t.stored.theme, 'dark');
  assert.equal(t.attrs['aria-pressed'], 'true');
  t.handlers.click();
  assert.ok(t.classList.contains('theme-light'));
  assert.equal(t.stored.theme, 'light');
});

test('toggle still works when storage is blocked', () => {
  const t = loadToggle({ setItemThrows: true });
  assert.doesNotThrow(() => t.handlers.click());
  assert.ok(t.classList.contains('theme-dark'));
});

test('script does not throw on pages without the toggle or year', () => {
  assert.doesNotThrow(() => loadToggle({ withButton: false }));
});

test('footer year is filled in', () => {
  assert.equal(loadToggle().year.textContent, String(new Date().getFullYear()));
});
