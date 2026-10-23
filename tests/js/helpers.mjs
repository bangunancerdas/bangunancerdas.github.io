import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

export function readSite(file) {
  return fs.readFileSync(path.join(ROOT, file), 'utf8');
}

export function publishedPages() {
  const blog = fs.readdirSync(path.join(ROOT, 'blog')).filter((f) => f.endsWith('.html')).map((f) => `blog/${f}`);
  return ['index.html', '404.html', ...blog];
}

/** The inline (non-JSON-LD, no src) script in <head> that sets the theme class. */
export function inlineThemeScript(html) {
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  return scripts.find((s) => s.includes("'theme'"));
}

export function fakeClassList(initial = []) {
  const set = new Set(initial);
  return {
    add: (...c) => c.forEach((x) => set.add(x)),
    remove: (...c) => c.forEach((x) => set.delete(x)),
    contains: (c) => set.has(c),
    toArray: () => [...set],
  };
}

export function runInSandbox(code, sandbox) {
  const context = vm.createContext(sandbox);
  vm.runInContext(code, context, { timeout: 1000 });
  return context;
}
