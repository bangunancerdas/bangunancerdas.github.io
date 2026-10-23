(function () {
  var THEME_STORAGE_KEY = 'theme';
  var root = document.documentElement;
  var btn = document.getElementById('theme-toggle');
  var year = document.getElementById('year');

  function currentTheme() {
    return root.classList.contains('theme-dark') ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    root.classList.remove('theme-light', 'theme-dark');
    root.classList.add('theme-' + theme);
    if (btn) {
      btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      btn.setAttribute('aria-pressed', String(theme === 'dark'));
    }
  }

  if (btn) {
    applyTheme(currentTheme());
    btn.addEventListener('click', function () {
      var nextTheme = currentTheme() === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
      try {
        localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
      } catch (e) {}
    });
  }

  if (year) year.textContent = String(new Date().getFullYear());
})();
