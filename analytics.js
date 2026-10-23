/*
 * Privacy-conscious conversion analytics (disabled by default).
 *
 * Nothing is loaded or sent until CONFIG.enabled is true AND a provider account
 * code is set. Read README.md ("Analytics") before enabling: a provider account
 * and a privacy/consent review are required first.
 *
 * Events carry only: event name, CTA identifier and page path. Never phone
 * numbers, prefilled WhatsApp messages, query strings or anything the visitor
 * typed. Do Not Track and Global Privacy Control are respected.
 */
(function () {
  'use strict';

  var CONFIG = {
    enabled: false,
    provider: 'goatcounter', // cookieless; see README for its data practices
    goatcounterCode: '' // subdomain label of https://<code>.goatcounter.com
  };
  // Test hook / deployment override: window.BC_ANALYTICS_CONFIG = { ... }.
  var override = window.BC_ANALYTICS_CONFIG;
  if (override) {
    for (var key in CONFIG) {
      if (Object.prototype.hasOwnProperty.call(override, key)) CONFIG[key] = override[key];
    }
  }

  var CLICK_EVENTS = ['whatsapp_click', 'service_cta_click', 'portfolio_click'];
  var CTA_ID_PATTERN = /^[a-z0-9-]{1,40}$/;
  var PROVIDER_CODE_PATTERN = /^[a-z0-9-]{1,63}$/;
  var GOATCOUNTER_SCRIPT = 'https://gc.zgo.at/count.js';
  var MAX_QUEUED_EVENTS = 20;
  var ARTICLE_SELECTOR = '[data-track-article]';
  // An article counts as read once its end has been reached and the tab has been
  // visible for this long, so a quick scroll to the bottom is not counted.
  var ARTICLE_READ_MIN_SECONDS = 15;

  function privacySignalOn() {
    var nav = typeof navigator === 'undefined' ? {} : navigator;
    return nav.doNotTrack === '1' || nav.doNotTrack === 'yes' || nav.globalPrivacyControl === true;
  }

  function isEnabled() {
    return (
      CONFIG.enabled === true &&
      CONFIG.provider === 'goatcounter' &&
      PROVIDER_CODE_PATTERN.test(String(CONFIG.goatcounterCode)) &&
      !privacySignalOn()
    );
  }

  // --- provider adapter (GoatCounter) ---------------------------------
  var queue = [];

  function flush() {
    while (queue.length && window.goatcounter && typeof window.goatcounter.count === 'function') {
      var payload = queue.shift();
      try {
        window.goatcounter.count({ path: payload.event + '/' + payload.cta, title: payload.page, event: true });
      } catch (e) {}
    }
  }

  function send(payload) {
    if (queue.length < MAX_QUEUED_EVENTS) queue.push(payload);
    flush();
  }

  function loadProvider() {
    var script = document.createElement('script');
    script.async = true;
    script.src = GOATCOUNTER_SCRIPT;
    script.setAttribute('data-goatcounter', 'https://' + CONFIG.goatcounterCode + '.goatcounter.com/count');
    script.onload = flush;
    document.head.appendChild(script);
  }

  // --- event construction ----------------------------------------------
  function track(event, cta) {
    send({ event: event, cta: cta, page: window.location.pathname });
  }

  function onClick(e) {
    try {
      var el = e.target && e.target.closest && e.target.closest('[data-track]');
      if (!el) return;
      var event = el.getAttribute('data-track');
      var cta = el.getAttribute('data-cta-id');
      if (CLICK_EVENTS.indexOf(event) === -1 || typeof cta !== 'string' || !CTA_ID_PATTERN.test(cta)) return;
      track(event, cta);
    } catch (err) {}
  }

  function watchArticleRead(article) {
    var visibleSeconds = 0;
    var done = false;
    var cta = window.location.pathname
      .replace(/^\/|\.html$/g, '')
      .replace(/[^a-z0-9-]+/gi, '-')
      .toLowerCase()
      .slice(0, 100);
    var timer = setInterval(function () {
      if (done || document.visibilityState === 'hidden') return;
      visibleSeconds += 1;
      var endReached = article.getBoundingClientRect().bottom <= window.innerHeight;
      if (visibleSeconds >= ARTICLE_READ_MIN_SECONDS && endReached) {
        done = true;
        clearInterval(timer);
        try {
          track('article_read', cta);
        } catch (err) {}
      }
    }, 1000);
  }

  if (!isEnabled()) return;

  try {
    loadProvider();
    document.addEventListener('click', onClick);
    var article = document.querySelector(ARTICLE_SELECTOR);
    if (article) watchArticleRead(article);
  } catch (err) {}
})();
