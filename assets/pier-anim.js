/* Pier AI project page: four animated explainers (question journey, the brain, training, storage and git).
   Each <figure class="pa" data-pa="..."> is filled here. Loops run only while the figure is on screen and stop for reduced motion. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var REDUCE = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var C = { bg: "#0d0d0d", p2: "#1c1c1b", line: "#2e2e2c", path: "#3b3b38", ink: "#f3f1ec", muted: "#9a9a94",
    or: "#ff7a45", or2: "#e5541f", cream: "#fff5ec", amber: "#ffc59e" };
  var uid = 0;

  function el(tag, attrs, parent, text) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function h(tag, cls, parent, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function ease(k) { return k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; }
  function tween(ms, fn) {
    return new Promise(function (r) {
      var t0 = performance.now();
      (function f(t) { var k = Math.min(1, (t - t0) / ms); fn(k); if (k < 1) requestAnimationFrame(f); else r(); })(t0);
    });
  }
  function svgRoot(fig, vb, label) {
    var box = h("div", "pa-svg", fig);
    var s = el("svg", { viewBox: vb, role: "img", "aria-label": label }, box);
    var id = "pa" + (++uid);
    var d = el("defs", {}, s);
    var f = el("filter", { id: id + "g", x: "-50%", y: "-50%", width: "200%", height: "200%" }, d);
    el("feGaussianBlur", { stdDeviation: "5", result: "b" }, f);
    var m = el("feMerge", {}, f); el("feMergeNode", { in: "b" }, m); el("feMergeNode", { in: "SourceGraphic" }, m);
    var mk = el("marker", { id: id + "a", viewBox: "0 0 10 10", refX: "9", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse" }, d);
    el("path", { d: "M0 0L10 5L0 10z", fill: C.muted }, mk);
    s.glow = "url(#" + id + "g)"; s.arrow = "url(#" + id + "a)";
    return s;
  }
  function caption(fig) {
    var c = h("div", "pa-cap", fig); var n = h("span", "pa-n", c, "1"); var d = h("div", "", c);
    var t = h("b", "", d, ""); var p = h("p", "", d, "");
    return function (num, title, text) { n.textContent = num; t.textContent = title; p.textContent = text; };
  }
  // a loop that runs only while its figure is visible and not paused
  function runner(fig, btn, loop) {
    var st = { paused: false, visible: false, running: false };
    function gate() { return new Promise(function (r) { (function chk() { if (!st.paused && st.visible) r(); else setTimeout(chk, 250); })(); }); }
    function kick() {
      if (REDUCE || st.running) return; st.running = true;
      (async function () { for (;;) { await gate(); await loop(gate); } })();
    }
    btn.addEventListener("click", function () { st.paused = !st.paused; btn.textContent = st.paused ? "▶ Play" : "❚❚ Pause"; kick(); });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { st.visible = es[0].isIntersecting; kick(); }, { threshold: 0.2 }).observe(fig);
    else { st.visible = true; kick(); }
    if (REDUCE) btn.hidden = true;
  }
  function text(parent, x, y, s, cls, style) { return el("text", { x: x, y: y, class: cls || "", style: style || "" }, parent, s); }

  /* ============ 1. the journey of a question ============ */
  function journey(fig) {
    var s = svgRoot(fig, "0 0 1000 430", "Animation: a question travels from the student through the ear, quick answers, the library of verified answers, the brain and the spell fix to Pier, who answers out loud.");
    var ctr = h("div", "pa-ctl", fig);
    var play = h("button", "pa-btn pa-main", ctr, "❚❚ Pause"); play.type = "button";
    var qA = h("button", "pa-btn", ctr, "“What did we cover last in maths?”"); qA.type = "button";
    var qB = h("button", "pa-btn", ctr, "“What time is it?”"); qB.type = "button";
    var cap = caption(fig);
    var ST = [
      { x: 70, y: 300, n: "Student", s: "asks out loud" },
      { x: 210, y: 270, n: "Ear", s: "Parakeet-sk" },
      { x: 360, y: 300, n: "Quick answers", s: "clock, timetable, staff" },
      { x: 520, y: 270, n: "Library", s: "1,685 verified answers" },
      { x: 690, y: 300, n: "Brain", s: "language model pier-e2b" },
      { x: 840, y: 270, n: "Spell fix", s: "diacritics, i/y" },
      { x: 950, y: 300, n: "Pier", s: "speaks and shows" }];
    var mainD = "M70,300 C140,300 150,270 210,270 S290,310 360,300 S450,260 520,270 S620,310 690,300 S790,260 840,270 S920,300 950,300";
    var shortD = "M360,300 C470,90 840,90 950,300";
    el("path", { d: mainD, fill: "none", stroke: C.line, "stroke-width": "10", "stroke-linecap": "round" }, s);
    var mainP = el("path", { d: mainD, fill: "none", stroke: C.path, "stroke-width": "2", "stroke-dasharray": "2 10" }, s);
    var shortBg = el("path", { d: shortD, fill: "none", stroke: C.amber, "stroke-width": "3", "stroke-dasharray": "8 8", opacity: ".25" }, s);
    text(s, 655, 122, "shortcut: time, date, timetable, staff", "pa-sub", "fill:" + C.amber);
    var trail = el("path", { d: mainD, fill: "none", stroke: C.or, "stroke-width": "4", "stroke-linecap": "round" }, s);
    var shortTrail = el("path", { d: shortD, fill: "none", stroke: C.amber, "stroke-width": "4", "stroke-linecap": "round" }, s);
    var stEls = ST.map(function (p, i) {
      var g = el("g", {}, s);
      var ring = el("circle", { cx: p.x, cy: p.y, r: i === 0 || i === 6 ? 40 : 44, fill: C.p2, stroke: C.line, "stroke-width": "3" }, g);
      var l = text(g, p.x, p.y + 72, p.n, "pa-lbl"); text(g, p.x, p.y + 93, p.s, "pa-sub");
      return { ring: ring, l: l };
    });
    // icons
    var g = el("g", {}, s);
    el("circle", { cx: 70, cy: 288, r: 11, fill: "none", stroke: C.ink, "stroke-width": "3" }, g);
    el("path", { d: "M50 322 Q70 296 90 322", fill: "none", stroke: C.ink, "stroke-width": "3" }, g);
    el("rect", { x: 200, y: 246, width: 20, height: 32, rx: 10, fill: "none", stroke: C.or, "stroke-width": "3" }, g);
    el("path", { d: "M193 268 Q210 292 227 268 M210 284 V294 M200 294 H220", fill: "none", stroke: C.or, "stroke-width": "3" }, g);
    el("circle", { cx: 360, cy: 300, r: 22, fill: "none", stroke: C.amber, "stroke-width": "3" }, g);
    el("line", { x1: 360, y1: 300, x2: 360, y2: 286, stroke: C.amber, "stroke-width": "3", "stroke-linecap": "round" }, g);
    el("line", { x1: 360, y1: 300, x2: 374, y2: 300, stroke: C.amber, "stroke-width": "2", "stroke-linecap": "round", class: "pa-spin" }, g);
    [[498, C.or], [512, C.amber], [526, C.cream]].forEach(function (b) { el("rect", { x: b[0], y: 252, width: 10, height: 34, rx: 2, fill: b[1], opacity: ".85" }, g); });
    el("circle", { cx: 540, cy: 262, r: 9, fill: "none", stroke: C.ink, "stroke-width": "3" }, g);
    el("line", { x1: 546, y1: 268, x2: 553, y2: 276, stroke: C.ink, "stroke-width": "3", "stroke-linecap": "round" }, g);
    el("path", { d: "M670 300c-10-2-14-14-6-22c-4-12 8-22 18-16c6-8 20-6 22 4c12-2 18 12 10 20c8 8 2 22-10 20c-4 10-20 10-24 2c-6 4-12 0-10-8z", fill: "none", stroke: C.or, "stroke-width": "3" }, g);
    [[680, 290], [694, 282], [704, 296], [688, 304], [698, 309]].forEach(function (p, k) { el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: C.or, class: "pa-pulse", style: "animation-delay:" + k * 0.3 + "s" }, g); });
    text(g, 831, 280, "Aá", "", "font-weight:800;font-size:22px;fill:" + C.cream + ";text-anchor:middle");
    el("path", { d: "M840 282 l6 6 l12 -14", fill: "none", stroke: C.or, "stroke-width": "3", "stroke-linecap": "round" }, g);
    el("circle", { cx: 944, cy: 300, r: 24, fill: "#2a1a12", stroke: C.or, "stroke-width": "3" }, g);
    el("circle", { cx: 936, cy: 294, r: 3, fill: C.ink }, g); el("circle", { cx: 952, cy: 294, r: 3, fill: C.ink }, g);
    var mouth = el("ellipse", { cx: 944, cy: 309, rx: 7, ry: 2, fill: C.or }, g);
    var speak = el("g", { opacity: "0" }, s);
    ["M978 286 q8 14 0 28", "M986 280 q12 20 0 40", "M994 274 q16 26 0 52"].forEach(function (d, k) { el("path", { d: d, fill: "none", stroke: C.or, "stroke-width": "2.5", "stroke-linecap": "round", class: "pa-pulse", style: "animation-delay:" + k * 0.2 + "s" }, speak); });
    var sw = el("g", { opacity: "0" }, s);
    [0, 1, 2, 3, 4].forEach(function (k) { el("rect", { x: 110 + k * 9, y: 286, width: 5, height: 28, rx: 2, fill: C.or, class: "pa-wave", style: "animation-delay:" + k * 0.12 + "s" }, sw); });
    var chip = el("g", {}, s); var chipR = el("rect", { rx: 8, height: 30, fill: C.p2, stroke: C.or, "stroke-width": "1.5" }, chip); var chipT = text(chip, 10, 20, "", "pa-mono");
    var pk = el("g", {}, s); el("circle", { r: 11, fill: "#fff", filter: s.glow }, pk); el("circle", { r: 6, fill: C.or2 }, pk);

    function setChip(t) { chipT.textContent = t; var w = Math.max(60, t.length * 8.2 + 22); chipR.setAttribute("width", w); chip.w = w; }
    function placeXY(x, y) { pk.setAttribute("transform", "translate(" + x + "," + y + ")"); var w = chip.w || 100; chip.setAttribute("transform", "translate(" + Math.min(Math.max(x - w / 2, 4), 996 - w) + "," + (y - 78) + ")"); }
    function placeAt(path, len) { var p = path.getPointAtLength(len); placeXY(p.x, p.y); }
    function lenAt(path, pt) { var L = path.getTotalLength(), best = 0, bd = 1e9; for (var l = 0; l <= L; l += 2) { var p = path.getPointAtLength(l), d = (p.x - pt.x) * (p.x - pt.x) + (p.y - pt.y) * (p.y - pt.y); if (d < bd) { bd = d; best = l; } } return best; }
    var trailL = trail.getTotalLength(), shortL = shortTrail.getTotalLength(), stLen = ST.map(function (p) { return lenAt(mainP, p); });
    trail.style.strokeDasharray = trailL; shortTrail.style.strokeDasharray = shortL; shortTrail.style.strokeDashoffset = shortL;
    var Q = "A";
    var CAP = { A: [
      ["The student asks", "Pier is always listening, so no button is needed. For now the question is just sound.", "〰 sound"],
      ["Ear: sound becomes text", "The Parakeet-sk speech recogniser turns Slovak speech into text on the CPU and fixes names it often mishears. Audio is never saved.", "“what did we cover last in maths”"],
      ["Quick answers: no", "It is not a question about the time, the date, the timetable or a teacher. Python would answer those exactly. This one moves on.", "→ next"],
      ["Library: find a cheat sheet", "Pier searches 1,685 verified answers by letters and by meaning, and picks up to 3 of the closest. Here it finds the maths curriculum answer from EduPage.", "question + 3 cheat sheets"],
      ["The brain writes the answer", "The language model gets the question and the cheat sheets and says the answer in its own words, short and in Slovak. Without a cheat sheet on an unverified topic, it says it does not know.", "“Last time in maths we had …”"],
      ["Spell fix", "A small model sometimes breaks diacritics or i/y. A rule-based check against a Slovak dictionary fixes that before it is spoken.", "answer ✓"],
      ["Pier speaks", "The text becomes a voice (the female Piper “lili” voice on the Pi). The animated Pier talks and the answer also shows in a speech bubble.", "🔊"]],
      B: [
      ["The student asks", "“What time is it?” For now the question is just sound.", "〰 sound"],
      ["Ear: sound becomes text", "Parakeet-sk turns the speech into text.", "“what time is it”"],
      ["Quick answers: yes", "Time must never be guessed. Python reads the clock and has the answer at once, so it takes the shortcut and never asks the brain.", "“It is 10:42.”"],
      null, null, null,
      ["Pier speaks", "An exact answer with no AI involved. The date, bells, class timetables, teacher contacts and the weather work the same way.", "🔊"]] };
    function show(i) {
      var c = CAP[Q][i]; cap(i + 1, c[0], c[1]); setChip(c[2]);
      stEls.forEach(function (e, j) { var on = j === i; e.ring.setAttribute("stroke", on ? C.or : C.line); e.ring.setAttribute("filter", on ? s.glow : ""); e.l.style.fill = on ? C.or : ""; });
    }
    function setQ(q) { Q = q; qA.setAttribute("aria-pressed", q === "A"); qB.setAttribute("aria-pressed", q === "B"); shortBg.setAttribute("opacity", q === "B" ? ".6" : ".25"); }
    qA.onclick = function () { setQ("A"); }; qB.onclick = function () { setQ("B"); }; setQ("A");
    // resting frame: the question at the brain
    placeAt(mainP, stLen[4]); trail.style.strokeDashoffset = trailL - stLen[4]; show(4);
    runner(fig, play, async function (gate) {
      var q = Q; trail.style.strokeDashoffset = trailL; shortTrail.style.strokeDashoffset = shortL; speak.setAttribute("opacity", "0");
      placeAt(mainP, 0); show(0); sw.setAttribute("opacity", "1"); await wait(1600); sw.setAttribute("opacity", "0");
      var stops = q === "A" ? [1, 2, 3, 4, 5, 6] : [1, 2], prev = 0;
      for (var k = 0; k < stops.length; k++) {
        var i = stops[k], a = stLen[prev], b = stLen[i]; await gate();
        await tween(1100, function (t) { var l = a + (b - a) * ease(t); placeAt(mainP, l); trail.style.strokeDashoffset = trailL - l; });
        show(i); if (i === 6) break; await wait(i === 4 ? 2800 : 2100); prev = i;
      }
      if (q === "B") {
        await gate();
        await tween(1500, function (t) { var l = shortL * ease(t), p = shortTrail.getPointAtLength(l); placeXY(p.x, p.y); shortTrail.style.strokeDashoffset = shortL - l; });
        show(6);
      }
      speak.setAttribute("opacity", "1");
      for (var m = 0; m < 8; m++) { mouth.setAttribute("ry", m % 2 ? 2 : 6); await wait(180); }
      mouth.setAttribute("ry", 2); await wait(1800);
    });
  }

  /* ============ 2. the brain ============ */
  function brain(fig) {
    var s = svgRoot(fig, "0 0 1000 500", "Animation: the words of the question and a cheat sheet enter a neural network, signals pass through its layers, and the most likely next word is chosen.");
    var ctr = h("div", "pa-ctl", fig);
    var play = h("button", "pa-btn pa-main", ctr, "❚❚ Pause"); play.type = "button";
    h("span", "pa-hint", ctr, "Each round adds one word to the answer");
    var INPUT = ["Čo", "sme", "naposledy", "preberali", "v", "matematike", "?"];
    text(s, 120, 40, "INPUT", "pa-lbl", "fill:" + C.muted);
    text(s, 540, 40, "BRAIN: layers of artificial neurons", "pa-lbl", "fill:" + C.or);
    text(s, 870, 40, "NEXT WORD?", "pa-lbl", "fill:" + C.muted);
    var inY = [];
    INPUT.forEach(function (w, i) { var y = 72 + i * 38; inY.push(y); var g = el("g", {}, s); el("rect", { x: 40, y: y - 15, width: 160, height: 30, rx: 7, fill: C.p2, stroke: C.line }, g); text(g, 52, y + 5, w, "pa-mono"); });
    var ty = 72 + INPUT.length * 38 + 8, tg = el("g", {}, s);
    el("rect", { x: 40, y: ty - 15, width: 160, height: 46, rx: 7, fill: "rgba(255,197,158,.12)", stroke: C.amber }, tg);
    text(tg, 52, ty + 3, "CHEAT SHEET:", "pa-mono", "fill:" + C.amber); text(tg, 52, ty + 21, "maths topics + dates", "pa-mono", "fill:" + C.amber + ";font-size:12px");
    inY.push(ty + 8);
    var LX = [330, 470, 610], LN = [6, 7, 6], layers = LX.map(function (x, li) { var a = []; for (var k = 0; k < LN[li]; k++) a.push({ x: x, y: 95 + k * (300 / (LN[li] - 1)) }); return a; });
    var OUTX = 760, outY = [120, 190, 260, 330], edges = el("g", {}, s);
    function line(a, b) { el("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: C.line, "stroke-width": "1" }, edges); }
    inY.forEach(function (y) { layers[0].forEach(function (n) { line({ x: 200, y: y }, n); }); });
    for (var li = 0; li < 2; li++) layers[li].forEach(function (a) { layers[li + 1].forEach(function (b) { line(a, b); }); });
    layers[2].forEach(function (a) { outY.forEach(function (y) { line(a, { x: OUTX, y: y }); }); });
    var nodes = layers.map(function (arr) { return arr.map(function (n) { return el("circle", { cx: n.x, cy: n.y, r: 11, fill: C.p2, stroke: C.or, "stroke-width": "2" }, s); }); });
    var rows = outY.map(function (y) {
      var g = el("g", {}, s);
      var t = text(g, OUTX + 10, y - 8, "", "pa-mono"); el("rect", { x: OUTX + 10, y: y, width: 200, height: 14, rx: 3, fill: C.p2 }, g);
      var b = el("rect", { x: OUTX + 10, y: y, width: 0, height: 14, rx: 3, fill: C.muted }, g);
      var pc = text(g, OUTX + 218, y + 12, "", "pa-mono", "fill:" + C.muted + ";font-size:12px");
      return { t: t, b: b, pc: pc };
    });
    el("rect", { x: 40, y: 440, width: 920, height: 44, rx: 10, fill: C.p2, stroke: C.or }, s);
    text(s, 58, 468, "Pier:", "pa-lbl", "text-anchor:start;fill:" + C.or + ";font-size:18px");
    var ans = text(s, 112, 468, "", "", "font-size:18px");
    var sig = el("g", {}, s);
    var STEPS = [
      ["Naposledy", [["Naposledy", 62], ["Minule", 21], ["V", 11], ["Podľa", 6]]],
      ["sme", [["sme", 71], ["ste", 14], ["sa", 9], ["bola", 6]]],
      ["v", [["v", 68], ["z", 17], ["na", 10], ["mali", 5]]],
      ["matematike", [["matematike", 80], ["matike", 11], ["predmete", 6], ["škole", 3]]],
      ["mali", [["mali", 58], ["preberali", 29], ["robili", 9], ["boli", 4]]],
      ["…", [["…", 49], ["tému", 27], ["kapitolu", 15], ["test", 9]]]];
    async function signal(a, b, col, ms) { var c = el("circle", { r: 4, fill: col, filter: s.glow }, sig); await tween(ms, function (k) { c.setAttribute("cx", a.x + (b.x - a.x) * k); c.setAttribute("cy", a.y + (b.y - a.y) * k); }); c.remove(); }
    function flash(li, on) { nodes[li].forEach(function (n) { n.setAttribute("fill", on ? C.or : C.p2); n.setAttribute("filter", on ? s.glow : ""); }); }
    function out(c, k) { c.forEach(function (x, i) { var r = rows[i]; r.t.textContent = x[0]; r.b.setAttribute("width", 2 * x[1] * k); r.pc.textContent = Math.round(x[1] * k) + " %"; r.b.setAttribute("fill", i === 0 ? C.or : C.muted); }); }
    out(STEPS[3][1], 1); ans.textContent = "Naposledy sme v matematike"; flash(1, true);
    runner(fig, play, async function (gate) {
      var words = []; ans.textContent = ""; flash(0, false); flash(1, false); flash(2, false);
      for (var k = 0; k < STEPS.length; k++) {
        await gate(); var st = STEPS[k]; out(st[1], 0);
        var jobs = inY.map(function (y, i) { return signal({ x: 200, y: y }, layers[0][(i * 3) % 6], i === inY.length - 1 ? C.amber : C.cream, 600); });
        await Promise.all(jobs); flash(0, true);
        for (var l = 0; l < 2; l++) {
          jobs = layers[l].map(function (a, i) { return signal(a, layers[l + 1][(i * 2 + k) % layers[l + 1].length], C.or, 500); });
          await Promise.all(jobs); flash(l, false); flash(l + 1, true);
        }
        jobs = layers[2].map(function (a, i) { return signal(a, { x: OUTX, y: outY[i % 4] }, C.or, 450); });
        await Promise.all(jobs); flash(2, false);
        await tween(700, function (t) { out(st[1], ease(t)); }); await wait(700);
        words.push(st[0]); ans.textContent = words.join(" "); await wait(500);
      }
      await wait(2200);
    });
  }

  /* ============ 3. training ============ */
  function training(fig) {
    var s = svgRoot(fig, "0 0 1000 380", "Animation: example cards go into the brain, small LoRA patches appear on it, and the training error curve goes down.");
    var ctr = h("div", "pa-ctl", fig);
    var play = h("button", "pa-btn pa-main", ctr, "❚❚ Pause"); play.type = "button";
    h("span", "pa-hint", ctr, "Training runs at home on an RTX 3060");
    text(s, 150, 40, "EXAMPLES", "pa-lbl", "fill:" + C.muted);
    text(s, 470, 40, "BRAIN + PATCHES (LoRA)", "pa-lbl", "fill:" + C.or);
    text(s, 820, 40, "TRAINING ERROR", "pa-lbl", "fill:" + C.muted);
    var EX = [["Kedy začína prvá hodina?", "O 7:10 …"], ["Čo je moderna?", "Literárne obdobie …"], ["Kto je patrón školy?", "Pier Giorgio Frassati …"], ["Čo je IP adresa?", "Číslo zariadenia v sieti …"], ["Ďakujem.", "Rado sa stalo."]];
    el("path", { d: "M400 230c-40-6-56-56-24-88c-16-48 32-88 72-64c24-32 80-24 88 16c48-8 72 48 40 80c32 32 8 88-40 80c-16 40-80 40-96 8c-24 16-48 0-40-32z", fill: "rgba(255,122,69,.07)", stroke: C.or, "stroke-width": "3" }, s);
    [[420, 150], [460, 120], [500, 140], [540, 170], [430, 200], [480, 190], [520, 215], [470, 240], [545, 240], [450, 170]].forEach(function (p, k) { el("circle", { cx: p[0], cy: p[1], r: 4, fill: C.or, class: "pa-pulse", style: "animation-delay:" + k * 0.2 + "s" }, s); });
    var patches = el("g", {}, s), PATCH = [[410, 130], [525, 120], [575, 200], [395, 215], [490, 265], [455, 150], [540, 250], [505, 175]], PCOL = [C.amber, C.cream, C.or, C.or2];
    var cards = el("g", {}, s);
    var x0 = 700, y0 = 300, cw = 250, ch = 200;
    el("line", { x1: x0, y1: y0, x2: x0 + cw, y2: y0, stroke: C.line, "stroke-width": "2" }, s);
    el("line", { x1: x0, y1: y0, x2: x0, y2: y0 - ch, stroke: C.line, "stroke-width": "2" }, s);
    text(s, x0 + cw / 2, y0 + 24, "examples seen →", "pa-sub");
    text(s, x0, y0 - ch - 10, "error", "pa-sub", "text-anchor:start");
    var pts = []; for (var i = 0; i <= 40; i++) { var k = i / 40, v = 0.92 * Math.exp(-4.2 * k) + 0.07 + 0.03 * Math.sin(i * 1.7) * (1 - k); pts.push((x0 + k * cw).toFixed(1) + "," + (y0 - v * ch).toFixed(1)); }
    var curve = el("polyline", { points: pts.join(" "), fill: "none", stroke: C.or, "stroke-width": "3", "stroke-linejoin": "round" }, s);
    var cL = curve.getTotalLength ? curve.getTotalLength() : 600; curve.style.strokeDasharray = cL;
    text(s, x0 + cw, y0 - ch + 8, "curve shape is illustrative", "pa-sub", "text-anchor:end");
    var status = text(s, 470, 345, "", "pa-lbl", "fill:" + C.cream);
    function card(q, a) { var g = el("g", { transform: "translate(40,170)" }, cards); el("rect", { width: 240, height: 52, rx: 8, fill: C.p2, stroke: C.amber }, g); text(g, 12, 21, "? " + q, "", "font-size:14px;font-weight:600"); text(g, 12, 41, "✓ " + a, "", "font-size:13px;fill:" + C.amber); return g; }
    function patch(e, op) { var p = PATCH[e]; return el("rect", { x: p[0] - 12, y: p[1] - 8, width: 24, height: 16, rx: 4, fill: PCOL[e % 4], opacity: op, transform: "rotate(" + ((e % 3) - 1) * 12 + " " + p[0] + " " + p[1] + ")" }, patches); }
    for (var e = 0; e < 5; e++) patch(e, ".9");
    curve.style.strokeDashoffset = cL * 0.35; card(EX[0][0], EX[0][1]); status.textContent = "example 5 of thousands";
    runner(fig, play, async function (gate) {
      patches.textContent = ""; cards.textContent = ""; curve.style.strokeDashoffset = cL;
      var N = EX.length + 3;
      for (var e = 0; e < N; e++) {
        await gate(); var ex = EX[e % EX.length]; status.textContent = "example " + (e + 1) + " of thousands";
        var c = card(ex[0], ex[1]);
        await tween(1100, function (k) { c.setAttribute("transform", "translate(" + (40 + 340 * ease(k)) + ",170) scale(" + (1 - 0.7 * k) + ")"); c.setAttribute("opacity", String(1 - k * 0.9)); });
        c.remove();
        if (e < PATCH.length) { var r = patch(e, "0"); await tween(300, function (k) { r.setAttribute("opacity", String(0.9 * k)); }); }
        var to = cL * (1 - (e + 1) / N), from = parseFloat(curve.style.strokeDashoffset);
        await tween(600, function (k) { curve.style.strokeDashoffset = from + (to - from) * k; });
      }
      status.textContent = "done: smaller error, answers in Pier's style"; await wait(3000);
    });
  }

  /* ============ 4. storage and git ============ */
  function storage(fig) {
    var s = svgRoot(fig, "0 0 1000 420", "Animation: files travel from the home PC to the GitHub repository and the GitHub release, and from there to the Raspberry Pi at school.");
    var ctr = h("div", "pa-ctl", fig);
    var b1 = h("button", "pa-btn pa-main", ctr, "▶ First install on the Pi"); b1.type = "button";
    var b2 = h("button", "pa-btn", ctr, "▶ A change and an update"); b2.type = "button";
    var term = h("div", "pa-term", fig); term.setAttribute("aria-live", "polite");
    var cap = caption(fig);
    cap("·", "Four places", "The home PC (everything, including training, about 33 GB), the private GitHub repository (code and data, about 14 MB), the GitHub release “modely” (large model files, about 2.1 GB) and the Raspberry Pi at school.");
    function prompt(pc) { var l = h("div", "", term); h("span", "pa-p", l, pc ? "PS C:\\pier-ai>" : "pi@school:~$"); return l; }
    prompt(false).appendChild(document.createTextNode(" (press a button to see what is typed)"));
    var N = {
      pc: { x: 150, y: 210, c: C.or, t: "Home PC", s: "everything + training · ~33 GB" },
      repo: { x: 500, y: 95, c: C.cream, t: "GitHub repository", s: "code and data · ~14 MB · private" },
      rel: { x: 500, y: 325, c: C.amber, t: "GitHub release “modely”", s: "large files · ~2.1 GB" },
      pi: { x: 850, y: 210, c: C.or, t: "Raspberry Pi at school", s: "where Pier runs" } };
    var P = { push: "M235,190 C320,120 360,95 412,95", up: "M235,230 C320,300 360,325 412,325", pull: "M588,95 C660,95 700,150 768,190", dl: "M588,325 C660,325 700,270 768,230" };
    var paths = {};
    for (var k in P) paths[k] = el("path", { d: P[k], fill: "none", stroke: C.path, "stroke-width": "3", "stroke-dasharray": "6 7", "marker-end": s.arrow }, s);
    text(s, 300, 118, "git push", "pa-mono", "fill:" + C.muted); text(s, 290, 318, "upload", "pa-mono", "fill:" + C.muted);
    text(s, 640, 118, "git clone / pull", "pa-mono", "fill:" + C.muted); text(s, 630, 318, "stiahni-modely.sh", "pa-mono", "fill:" + C.muted);
    for (var key in N) { var n = N[key], g = el("g", {}, s);
      el("rect", { x: n.x - 88, y: n.y - 52, width: 176, height: 104, rx: 12, fill: C.p2, stroke: n.c, "stroke-width": "2.5" }, g);
      text(g, n.x, n.y + 76, n.t, "pa-lbl", "font-size:19px"); text(g, n.x, n.y + 95, n.s, "pa-sub"); }
    var n0 = N.pc;
    el("rect", { x: n0.x - 40, y: n0.y - 34, width: 80, height: 52, rx: 4, fill: "none", stroke: C.or, "stroke-width": "3" }, s);
    el("path", { d: "M" + (n0.x - 14) + " " + (n0.y + 30) + "h28 M" + n0.x + " " + (n0.y + 18) + "v12", stroke: C.or, "stroke-width": "3" }, s);
    text(s, n0.x, n0.y - 3, "pier-ai", "pa-mono", "text-anchor:middle;fill:" + C.or);
    n0 = N.repo; el("path", { d: "M" + (n0.x - 36) + " " + (n0.y - 22) + "h24l8 8h40v44h-72z", fill: "none", stroke: C.cream, "stroke-width": "3" }, s);
    n0 = N.rel; el("path", { d: "M" + (n0.x - 34) + " " + (n0.y - 14) + "l34-16l34 16v36l-34 16l-34-16z M" + (n0.x - 34) + " " + (n0.y - 14) + "l34 16l34-16 M" + n0.x + " " + (n0.y + 2) + "v36", fill: "none", stroke: C.amber, "stroke-width": "3" }, s);
    n0 = N.pi; el("rect", { x: n0.x - 40, y: n0.y - 28, width: 80, height: 52, rx: 6, fill: "none", stroke: C.or, "stroke-width": "3" }, s);
    el("rect", { x: n0.x - 12, y: n0.y - 12, width: 24, height: 20, fill: C.or, opacity: ".6" }, s);
    for (var i = 0; i < 6; i++) el("circle", { cx: n0.x - 30 + i * 12, cy: n0.y - 20, r: 2.5, fill: C.or }, s);
    var live = text(s, N.pi.x, N.pi.y - 62, "● Pier is running", "pa-lbl", "fill:" + C.or + ";font-size:18px"); live.setAttribute("opacity", "0");
    text(s, 40, 384, "save points (commits):", "pa-sub", "text-anchor:start");
    var cg = el("g", {}, s), commits = [["af3dfec", "first import"], ["660eed0", "README: install steps"]];
    function drawCommits() {
      cg.textContent = "";
      el("line", { x1: 60, y1: 405, x2: 60 + (commits.length - 1) * 200, y2: 405, stroke: C.amber, "stroke-width": "2" }, cg);
      commits.forEach(function (c, i) { var x = 60 + i * 200;
        el("circle", { cx: x, cy: 405, r: 7, fill: c[2] ? C.amber : C.bg, stroke: C.amber, "stroke-width": "2.5" }, cg);
        text(cg, x + 14, 410, c[0], "pa-mono", "font-size:12px;fill:" + C.amber); text(cg, x + 80, 410, c[1], "", "font-size:12px;fill:" + C.muted); });
    }
    drawCommits();
    var files = el("g", {}, s);
    async function send(key, label, col, ms) {
      var p = paths[key], L = p.getTotalLength(); p.setAttribute("stroke", col);
      var g = el("g", {}, files), w = label.length * 7.8 + 22;
      el("rect", { x: -w / 2, y: -14, width: w, height: 28, rx: 6, fill: C.bg, stroke: col, "stroke-width": "2", filter: s.glow }, g);
      text(g, 0, 5, label, "pa-mono", "text-anchor:middle;font-size:12px;fill:" + col);
      await tween(REDUCE ? 1 : ms, function (k) { var q = p.getPointAtLength(L * ease(k)); g.setAttribute("transform", "translate(" + q.x + "," + q.y + ")"); });
      g.remove(); p.setAttribute("stroke", C.path);
    }
    async function cmd(pc, c, out) {
      var l = prompt(pc), t = document.createTextNode(" "); l.appendChild(t);
      for (var i = 0; i < c.length; i++) { t.data += c[i]; if (!REDUCE) await wait(22); }
      if (out) h("div", "pa-out", term, out);
    }
    var busy = false;
    b1.onclick = async function () {
      if (busy) return; busy = true; term.textContent = ""; live.setAttribute("opacity", "0");
      cap("1", "At home: code goes to the repository", "The program, the screen with the face, 1,685 verified answers and the installer are saved with a commit and pushed to GitHub.");
      await cmd(true, "git push", "main -> main"); await send("push", "code and data 14 MB", C.cream, 1600);
      cap("2", "At home: large files go to the release", "A repository accepts files up to 100 MB. The brain alone is 1.55 GB, so the brain, the ear (456 MB) and the meaning search model (113 MB) go into a release.");
      await send("up", "brain 1.55 GB", C.amber, 1500); await send("up", "ear 456 MB", C.amber, 1100);
      cap("3", "At school: the Pi downloads the code", "Log in to GitHub once, then one command fetches the whole project.");
      await cmd(false, "gh repo clone tomaskooooo/pier-ai ~/pier-ai", "Cloning into 'pier-ai'... done"); await send("pull", "code and data", C.cream, 1500);
      cap("4", "At school: the installer fetches the models", "install.sh installs the programs, downloads the models from the release and the female Piper “lili” voice. It takes tens of minutes.");
      await cmd(false, "bash ~/pier-ai/pi/install.sh", "== 4/6 Ollama and the language model ..."); await send("dl", "models 2.1 GB", C.amber, 1800);
      live.setAttribute("opacity", "1"); await cmd(false, "~/pier-ai/pi/pier-ai.sh", "Pier AI is running full screen.");
      cap("✓", "Pier runs at school", "From now on the Pi does not need the home PC. The ear, the brain and the voice all run on it.");
      busy = false;
    };
    b2.onclick = async function () {
      if (busy) return; busy = true; term.textContent = "";
      cap("1", "At home: a change and a test", "For example a new verified answer is added. The tests run to check that nothing else broke.");
      await cmd(true, "git commit -m \"New answer about school clubs\"", "[main a1b2c3d] (example)");
      commits.push(["a1b2c3d", "new answer (example)", 1]); drawCommits();
      cap("2", "A new save point", "A commit is a saved state of every file. If something goes wrong, you go back to the previous one.");
      await wait(1200);
      cap("3", "Push", "The change goes to GitHub, and the whole history stays there.");
      await cmd(true, "git push", "660eed0..a1b2c3d  main -> main"); await send("push", "change", C.cream, 1500);
      cap("4", "At school: git pull", "One command on the Pi and Pier has the new version. The large models are only downloaded again after a new training round.");
      await cmd(false, "cd ~/pier-ai && git pull", "Updating 660eed0..a1b2c3d"); await send("pull", "change", C.cream, 1500); live.setAttribute("opacity", "1");
      cap("✓", "Updated", "Nothing is lost: every version stays on GitHub.");
      await wait(2500); commits.pop(); drawCommits(); busy = false;
    };
  }

  var SCENES = { journey: journey, brain: brain, training: training, storage: storage };
  [].forEach.call(document.querySelectorAll("[data-pa]"), function (fig) { var f = SCENES[fig.getAttribute("data-pa")]; if (f) f(fig); });
})();
