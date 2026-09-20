'use strict';

// Native hash links remain useful without JavaScript; enhance them as panels.
const panels = [...document.querySelectorAll('main > .panel')];
const navigation = [...document.querySelectorAll('[data-panel]')];
document.body.classList.add('enhanced');
function displayPanel(focusHeading = false) {
  const requested = location.hash.slice(1);
  if (requested === 'main') return;
  const anchor = document.getElementById(requested);
  const targetPanel = anchor?.closest('main > .panel');
  const id = targetPanel ? targetPanel.id : 'about';
  panels.forEach(panel => { panel.hidden = panel.id !== id; });
  navigation.forEach(link => {
    if (link.dataset.panel === id) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  if (targetPanel && anchor !== targetPanel) {
    if (requested === 'press-sun') anchor.querySelector('details').open = true;
    requestAnimationFrame(() => {
      if (focusHeading) anchor.querySelector('h2,h3')?.focus({preventScroll:true});
      anchor.scrollIntoView({block:'start',behavior:'instant'});
    });
  } else if (focusHeading) {
    document.querySelector(`#${id} h1`).focus({preventScroll:true});
    window.scrollTo({top:0, behavior:'instant'});
  }
}
window.addEventListener('hashchange', () => displayPanel(true));
displayPanel();

let language = 'en';
try { language = localStorage.getItem('site-language') === 'zh' ? 'zh' : 'en'; } catch (_) {}
const languageButton = document.getElementById('langBtn');
function applyLanguage() {
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
  document.querySelectorAll('[data-en][data-zh]').forEach(element => { element.textContent = element.dataset[language]; });
  languageButton.textContent = language === 'en' ? '中文' : 'English';
  languageButton.setAttribute('aria-label', language === 'en' ? 'Switch to Chinese' : 'Switch to English');
}
languageButton.addEventListener('click', () => {
  language = language === 'en' ? 'zh' : 'en';
  try { localStorage.setItem('site-language', language); } catch (_) {}
  applyLanguage();
});
applyLanguage();

const filters = document.getElementById('publication-filters');
filters.hidden = false;
filters.addEventListener('click', event => {
  const button = event.target.closest('button[data-filter]');
  if (!button) return;
  filters.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelectorAll('.pub-item').forEach(item => { item.hidden = button.dataset.filter === 'first' && item.dataset.firstAuthor !== 'true'; });
});

// Bot commits do not rebuild branch-based GitHub Pages. Read main's JSON directly
// in production, with the deployed snapshot as a dated fallback.
async function loadMetrics() {
  const local = ['localhost','127.0.0.1','[::1]'].includes(location.hostname);
  const urls = local ? ['data/metrics.json'] : [
    'https://raw.githubusercontent.com/Jinchao-Song/Jinchao-Song.github.io/main/data/metrics.json',
    'data/metrics.json'
  ];
  for (const url of urls) {
    try {
      const response = await fetch(url, {cache:'no-store'});
      if (!response.ok) continue;
      return await response.json();
    } catch (_) { /* Try the last deployed snapshot if the repository is unavailable. */ }
  }
  throw new Error('Citation data unavailable');
}
loadMetrics().then(data => {
  if (data.authorId !== 'GwY9nlEAAAAJ' || data.source !== 'Google Scholar' || data.name !== 'Jinchao Song' || !Number.isInteger(data.citationCount) || data.citationCount < 0 || !Number.isInteger(data.hIndex) || data.hIndex < 0 || !/^\d{4}-\d{2}-\d{2}$/.test(data.updated)) return;
  document.getElementById('citations').textContent = data.citationCount.toLocaleString('en-US');
  document.getElementById('h-index').textContent = data.hIndex;
  document.getElementById('metrics-date').textContent = data.updated;
  document.getElementById('metrics').hidden = false;
}).catch(() => { /* Scholar and ORCID links remain available if metrics fail. */ });
