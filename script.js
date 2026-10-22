(function () {
  'use strict';

  /* ---- edit these two lines ---- */
  var EMAIL = 'tomas.dobos01@gmail.com';
  var LINKEDIN = 'https://www.linkedin.com/in/larping/';
  var FORM_ID = '5455881671918e463d74a84821fccd06';   // FormSubmit alias, so the address is not in the request URL
  /* ------------------------------ */

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* contact links */
  document.querySelectorAll('[data-mail]').forEach(function (a) {
    a.href = 'mailto:' + EMAIL;
    if (a.getAttribute('data-mail') === 'text') a.textContent = EMAIL;
  });
  document.querySelectorAll('[data-linkedin]').forEach(function (a) {
    if (LINKEDIN) { a.href = LINKEDIN; a.target = '_blank'; a.rel = 'noopener'; }
    else a.hidden = true;
  });

  /* sticky bar appears after the hero */
  var nav = document.getElementById('nav');
  var hero = document.querySelector('.hero');
  function onScroll() {
    if (nav && hero) nav.classList.toggle('show', window.scrollY > hero.offsetHeight * 0.7);
    updateWords();
  }

  /* fullscreen menu */
  var menu = document.getElementById('menu');
  var burgers = document.querySelectorAll('.burger');
  var closeBtn = menu && menu.querySelector('.menu-close');
  function setMenu(open) {
    if (!menu) return;
    menu.hidden = !open;
    document.body.classList.toggle('lock', open);
    burgers.forEach(function (b) { b.setAttribute('aria-expanded', String(open)); });
    if (open && closeBtn) closeBtn.focus();
  }
  burgers.forEach(function (b) { b.addEventListener('click', function () { setMenu(true); }); });
  if (closeBtn) closeBtn.addEventListener('click', function () { setMenu(false); });
  if (menu) menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu && !menu.hidden) setMenu(false); });

  /* fade-up on enter */
  var rv = document.querySelectorAll('.rv');
  rv.forEach(function (el, i) { el.style.setProperty('--d', ((i % 4) * 0.08) + 's'); });
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* word-by-word headline reveal driven by scroll */
  var headings = [];
  document.querySelectorAll('.words').forEach(function (h) {
    var words = [];
    var kids = Array.prototype.slice.call(h.childNodes);
    h.textContent = '';
    kids.forEach(function (node) {
      if (node.nodeType === 3) {
        node.textContent.split(/\s+/).filter(Boolean).forEach(function (t) {
          var s = document.createElement('span');
          s.className = 'w';
          s.textContent = t;
          h.appendChild(s);
          h.appendChild(document.createTextNode(' '));
          words.push(s);
        });
      } else {
        h.appendChild(node);
      }
    });
    headings.push({ el: h, words: words });
  });
  function updateWords() {
    var vh = window.innerHeight;
    headings.forEach(function (h) {
      var r = h.el.getBoundingClientRect();
      var p = (vh * 0.9 - r.top) / (vh * 0.55);
      p = Math.max(0, Math.min(1, p));
      var n = h.words.length;
      h.words.forEach(function (w, i) { w.classList.toggle('on', p * (n + 1) > i + 0.5); });
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', updateWords);
  requestAnimationFrame(onScroll);

  /* contact form: sends through FormSubmit (no server of my own); falls back to the plain address */
  var form = document.getElementById('form');
  var note = document.getElementById('formNote');
  function say(text, withAddress) {
    note.textContent = text;
    if (!withAddress) return;
    var a = document.createElement('a');
    a.href = 'mailto:' + EMAIL;
    a.textContent = EMAIL;
    note.appendChild(a);
  }
  if (form) {
    var send = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.elements.name.value.trim();
      var email = form.elements.email.value.trim();
      var msg = form.elements.message.value.trim();
      if (!name || !/^\S+@\S+\.\S+$/.test(email)) { say('Please add your name and a valid e-mail.'); return; }
      if (msg.length < 3) { say('Please write a short message.'); return; }
      if (form.elements._honey && form.elements._honey.value) { say('Thanks! Your message was sent.'); return; }  // bots fill the hidden field
      var label = send.textContent;
      send.disabled = true; send.textContent = 'Sending…'; form.setAttribute('aria-busy', 'true');
      say('Sending your message. This can take up to a minute.');
      var ctl = window.AbortController ? new AbortController() : null;
      var slow = setTimeout(function () { send.textContent = 'Still sending…'; }, 6000);
      var giveUp = setTimeout(function () { if (ctl) ctl.abort(); }, 90000);
      // multipart FormData is a "simple" request: no CORS preflight, which saves a whole round trip to the slow service
      var data = new FormData();
      data.append('name', name);
      data.append('email', email);
      data.append('message', msg);
      data.append('_subject', 'Portfolio message from ' + name);
      data.append('_template', 'table');
      data.append('_captcha', 'false');
      var timedOut = false;
      fetch('https://formsubmit.co/ajax/' + FORM_ID, {
        method: 'POST',
        signal: ctl ? ctl.signal : undefined,
        headers: { 'Accept': 'application/json' },
        body: data
      }).then(function (r) { return r.json().catch(function () { return {}; }); })
        .then(function (res) {
          if (res && (res.success === true || res.success === 'true')) {
            form.reset();
            say('Thanks! Your message was sent. I will reply to ' + email + '.');
          } else {
            say('Could not send it from here. Please write to ', true);
          }
        })
        .catch(function (err) {
          timedOut = !!(err && err.name === 'AbortError');
          say(timedOut ? 'This is taking unusually long. Your message may still arrive; if you do not hear back, write to '
                       : 'Could not send it from here. Please write to ', true);
        })
        .then(function () { clearTimeout(slow); clearTimeout(giveUp); send.disabled = false; send.textContent = label; form.removeAttribute('aria-busy'); });
    });
  }

  /* subtle hero parallax */
  var fine = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
  if (hero && fine && !reduce) {
    var raf = 0;
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5;
      var y = (e.clientY - r.top) / r.height - 0.5;
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        hero.style.setProperty('--px', (x * 16).toFixed(1) + 'px');
        hero.style.setProperty('--py', (y * 8).toFixed(1) + 'px');
        hero.style.setProperty('--gx', (x * -26).toFixed(1) + 'px');
        hero.style.setProperty('--gy', (y * -12).toFixed(1) + 'px');
      });
    });
  }
})();
