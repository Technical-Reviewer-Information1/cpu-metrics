(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const NS = 'http://www.w3.org/2000/svg';
  function el(n, a, t) { const e = document.createElementNS(NS, n); for (const k in a) if (a[k] != null) e.setAttribute(k, a[k]); if (t != null) e.textContent = t; return e; }
  function sci(v, dig) {
    if (v === 0) return '0';
    const d = dig === undefined ? 1 : dig;
    let ex = Math.floor(Math.log10(Math.abs(v)));
    let m = v / Math.pow(10, ex);
    if (Math.abs(+m.toFixed(d)) >= 10) { m /= 10; ex += 1; }
    return m.toFixed(d) + ' × 10<sup>' + ex + '</sup>';
  }
  const SUP = { '-': '\u207B', '0': '\u2070', '1': '\u00B9', '2': '\u00B2', '3': '\u00B3', '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079' };
  function sciPlain(v, dig) {
    if (v === 0) return '0';
    const d = dig === undefined ? 1 : dig;
    let ex = Math.floor(Math.log10(Math.abs(v)));
    let m = v / Math.pow(10, ex);
    if (Math.abs(+m.toFixed(d)) >= 10) { m /= 10; ex += 1; }
    return m.toFixed(d) + ' \u00D7 10' + String(ex).split('').map(c => SUP[c]).join('');
  }
  function bytes(v) {
    const U = [['TB', 1e12], ['GB', 1e9], ['MB', 1e6], ['kB', 1e3]];
    if (v >= 1e15) return sci(v, 2) + ' B';
    for (const u of U) if (v >= u[1]) return (Math.round(v / u[1] * 100) / 100).toLocaleString() + ' ' + u[0];
    return v + ' B';
  }

  /* ===== STEP 1 ===== */
  function drawBits() {
    const b = +$('bits').value;
    $('bitsV').textContent = b;
    const n = Math.pow(2, b);
    $('addrN').innerHTML = sci(n, 2) + ' 個';
    $('memSize').innerHTML = bytes(n);
    const note = $('bitNote');
    note.className = 'note info';
    note.innerHTML = '2<sup>' + b + '</sup> ＝ ' + sci(n, 2) + ' 個のアドレスを指定できます。' +
      (b === 32 ? '32ビットでは約4GBが上限。これが「32ビットOSではメモリを4GBまでしか使えない」と言われる理由です。'
        : b === 64 ? '64ビットでは 2<sup>64</sup>＝約1844万TB。事実上、上限を気にする必要がなくなりました。'
          : 'ビット数が1増えるごとに、扱える範囲は2倍になります。');
    $('bitTable').innerHTML = '<thead><tr><th>CPUのビット数</th><th>アドレスの数</th><th>理論上のメモリ空間</th></tr></thead><tbody>' +
      [8, 16, 32, 64].map(k => {
        const v = Math.pow(2, k);
        return '<tr' + (k === b ? ' style="background:var(--warn-bg);font-weight:700"' : '') + '><td class="mono">' + k + '</td>' +
          '<td class="mono">2<sup>' + k + '</sup></td><td class="mono">' + bytes(v) + '</td></tr>';
      }).join('') + '</tbody>';
  }

  /* ===== STEP 2 ===== */
  const JUDGE = [
    { k: 'a', t: '32ビットCPUと64ビットCPUでは、64ビットCPUの方が取り扱えるメモリ空間の理論上の上限は大きい。', ok: true,
      why: '2<sup>32</sup>（約4GB）に対して 2<sup>64</sup>。けた違いに大きくなります。STEP 1 で確かめられます。' },
    { k: 'b', t: '64ビットCPUを搭載したパソコンで動作する32ビット用のOSはない。', ok: false,
      why: '64ビットCPUでも<strong>32ビット用のOSは動きます</strong>（逆はできません）。' },
    { k: 'c', t: 'USBメモリの読み書きの速度は、64ビットCPUを採用したPCの方が32ビットCPUを採用したPCよりも2倍速い。', ok: false,
      why: 'USBメモリの速度はUSBの規格や記憶素子で決まり、<strong>CPUのビット数では2倍になりません</strong>。' }
  ];
  let jAns = {};
  function drawJudge() {
    $('jBox').innerHTML = JUDGE.map((j, i) =>
      '<div><div class="st"><span class="k">' + j.k + '</span><span class="t">' + j.t + '</span>' +
      '<span class="jb" data-i="' + i + '"><button class="btn" data-i="' + i + '" data-v="1">○</button>' +
      '<button class="btn" data-i="' + i + '" data-v="0">×</button></span></div>' +
      '<div class="note" id="jfb' + i + '" hidden style="margin-top:8px"></div></div>').join('');
    $('jBox').querySelectorAll('button[data-v]').forEach(btn => btn.addEventListener('click', () => {
      const i = +btn.dataset.i, j = JUDGE[i], ok = (btn.dataset.v === '1') === j.ok;
      const row = $('jBox').querySelector('.jb[data-i="' + i + '"]');
      row.style.pointerEvents = 'none';
      [...row.children].forEach(x => { if ((x.dataset.v === '1') === j.ok) x.classList.add('correct'); else if (x === btn) x.classList.add('wrong'); });
      const fb = $('jfb' + i); fb.hidden = false; fb.className = 'note ' + (ok ? 'ok' : 'ng');
      fb.innerHTML = '<strong>' + (j.ok ? '正しい記述です。' : '誤りです。') + '</strong>' + j.why;
      jAns[i] = ok;
      const done = Object.keys(jAns).length;
      const n = $('jNote'); n.className = 'note ' + (done === JUDGE.length ? 'ok' : 'info');
      n.innerHTML = done + ' / ' + JUDGE.length + ' 判定' + (done === JUDGE.length ? '<br>適切なのは <strong>a だけ</strong>です。' : '');
    }));
    $('jNote').className = 'note info'; $('jNote').textContent = '0 / ' + JUDGE.length + ' 判定';
  }
  const Q1 = ['a', 'a，b', 'b，c', 'c'];
  function drawQ1() {
    const box = $('q1Choices'); box.innerHTML = '';
    Q1.forEach((c, i) => {
      const b = document.createElement('button');
      b.className = 'btn'; b.style.textAlign = 'center'; b.dataset.c = c;
      b.textContent = '⓪①②③'[i] + '　' + c;
      b.addEventListener('click', () => {
        const ok = c === 'a';
        box.classList.add('locked');
        [...box.children].forEach(x => { if (x.dataset.c === 'a') x.classList.add('correct'); else if (x === b) x.classList.add('wrong'); });
        const fb = $('q1Fb'); fb.hidden = false; fb.className = 'note ' + (ok ? 'ok' : 'ng');
        fb.innerHTML = (ok ? '正解（⓪）。' : '正解は <strong>⓪　a</strong>。') + 'bとcはどちらも誤りなので、適切なのは a だけです。';
      });
      box.appendChild(b);
    });
  }

  /* ===== STEP 3 ===== */
  function drawClock() {
    const ghz = +$('ghz').value / 10, cyc = +$('cyc').value, ni = +$('ninst').value;
    $('ghzV').textContent = ghz.toFixed(1); $('cycV').textContent = cyc; $('ninstV').textContent = ni;
    const hz = ghz * 1e9;
    const ips = hz / cyc, t1 = cyc / hz, tn = cyc * ni / hz;
    $('mIPS').innerHTML = sci(ips, 1) + ' 回';
    $('mT1').innerHTML = sci(t1, 1) + ' 秒';
    $('mTn').innerHTML = sci(tn, 1) + ' 秒';
    $('cEq').innerHTML =
      '1秒間の命令数 ＝ (' + sci(hz, 1) + ') ÷ ' + cyc + ' ＝ <strong>' + sci(ips, 1) + '</strong>（回）<br>' +
      ni + '命令の時間 ＝ ' + cyc + ' × ' + ni + ' ÷ (' + sci(hz, 1) + ') ＝ <strong>' + sci(tn, 1) + '</strong>（秒）';
    // 波形
    const W = 600, H = 120, M = { l: 12, r: 12, t: 26, b: 26 };
    const show = Math.min(24, cyc * Math.min(ni, 4));
    const iw = W - M.l - M.r, ih = H - M.t - M.b;
    const cw = iw / show;
    const svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'クロック信号の波形' });
    for (let k = 0; k * cyc < show; k++) {
      const x0 = M.l + k * cyc * cw, w = Math.min(cyc * cw, M.l + iw - x0);
      if (k % 2 === 0) svg.appendChild(el('rect', { x: x0, y: M.t - 6, width: w, height: ih + 12, class: 'instband' }));
      svg.appendChild(el('line', { x1: x0, y1: M.t - 10, x2: x0, y2: M.t + ih + 10, class: 'instline' }));
      svg.appendChild(el('text', { x: x0 + w / 2, y: 16, class: 'lab b', 'text-anchor': 'middle' }, (k + 1) + '命令目'));
    }
    let d = 'M' + M.l + ' ' + (M.t + ih);
    for (let k = 0; k < show; k++) {
      const x = M.l + k * cw;
      d += ' L' + x + ' ' + M.t + ' L' + (x + cw / 2) + ' ' + M.t + ' L' + (x + cw / 2) + ' ' + (M.t + ih) + ' L' + (x + cw) + ' ' + (M.t + ih);
    }
    svg.appendChild(el('path', { d: d, class: 'wave' }));
    svg.appendChild(el('text', { x: M.l, y: H - 8, class: 'lab' }, '1周期 ＝ ' + sciPlain(1 / hz, 1) + ' 秒　／　' + cyc + '周期で1命令'));
    const box = $('clockBox'); box.innerHTML = ''; box.appendChild(svg);
    const n = $('clockNote');
    const isBook = Math.abs(ghz - 3.0) < 0.01 && cyc === 6;
    n.className = 'note ' + (isBook ? 'ok' : 'info');
    n.innerHTML = isBook
      ? '本文の条件です。3.0×10<sup>9</sup> ÷ 6 ＝ <strong>5.0×10<sup>8</sup> 回</strong>（【イ】＝②）。' +
        '2命令なら 6×2÷(3.0×10<sup>9</sup>) ＝ <strong>4.0×10<sup>-9</sup> 秒</strong>（【ウ】＝①）。'
      : '波形の1つの山と谷で1周期です。赤い点線が命令の区切りを表しています。' +
        '<strong>周期数が少ないほど</strong>、同じクロック周波数でもたくさんの命令を実行できます。';
  }

  /* ===== STEP 4 ===== */
  const BLANKS = [
    { k: 'イ', q: '3.0GHzで6周期に1命令のとき、1秒間に何回実行できるか。',
      ch: ['3.0×10⁸', '4.5×10⁸', '5.0×10⁸', '6.0×10⁸'], a: '5.0×10⁸',
      why: '3.0GHz＝3.0×10⁹Hz。3.0×10⁹ ÷ 6 ＝ 5.0×10⁸ 回です。' },
    { k: 'ウ', q: '2つの命令を実行するのに必要な時間は何秒か。',
      ch: ['3.0×10⁻⁹', '4.0×10⁻⁹', '5.0×10⁻⁹', '6.0×10⁻⁹'], a: '4.0×10⁻⁹',
      why: '2命令で 6×2＝12周期。12 ÷ (3.0×10⁹) ＝ 4.0×10⁻⁹ 秒です。1秒間に5.0×10⁸回なので、その逆数の2倍と考えても求められます。' }
  ];
  let bAns = {};
  function drawBlanks() {
    $('blankBox').innerHTML = BLANKS.map((b, i) =>
      '<div' + (i ? ' style="margin-top:18px;padding-top:16px;border-top:1px solid var(--line)"' : '') + '>' +
      '<p class="pq">【' + b.k + '】　' + b.q + '</p>' +
      '<div class="choice4" data-i="' + i + '">' + b.ch.map((c, j) =>
        '<button class="btn" data-i="' + i + '" data-c="' + c + '" style="text-align:center">' + '⓪①②③'[j] + '　' + c + '</button>').join('') +
      '</div><div class="note" id="bfb' + i + '" hidden></div></div>').join('');
    $('blankBox').querySelectorAll('button[data-c]').forEach(btn => btn.addEventListener('click', () => {
      const i = +btn.dataset.i, b = BLANKS[i], ok = btn.dataset.c === b.a;
      const row = $('blankBox').querySelector('.choice4[data-i="' + i + '"]');
      row.classList.add('locked');
      [...row.children].forEach(x => { if (x.dataset.c === b.a) x.classList.add('correct'); else if (x === btn) x.classList.add('wrong'); });
      const fb = $('bfb' + i); fb.hidden = false; fb.className = 'note ' + (ok ? 'ok' : 'ng');
      fb.innerHTML = (ok ? '正解。' : '正解は <strong>' + b.a + '</strong>。') + b.why;
      bAns[i] = ok;
      const done = Object.keys(bAns).length, right = Object.values(bAns).filter(Boolean).length;
      const n = $('blankNote');
      n.className = 'note ' + (done === BLANKS.length ? (right === done ? 'ok' : 'warn') : 'info');
      n.innerHTML = done + ' / ' + BLANKS.length + ' 問解答（正解 ' + right + ' 問）' +
        (done === BLANKS.length ? '<br>本文の答えは【イ】②　【ウ】① です。' : '');
    }));
    $('blankNote').className = 'note info';
    $('blankNote').textContent = '0 / ' + BLANKS.length + ' 問解答';
  }

  function drawFact() {
    $('factTable').innerHTML = '<thead><tr><th>性能を決める要素</th><th>意味</th><th>大きいと</th></tr></thead><tbody>' +
      '<tr><td>クロック周波数</td><td>1秒あたりのクロックの回数</td><td>速くなる（発熱・消費電力も増える）</td></tr>' +
      '<tr><td>1命令あたりの周期数</td><td>1つの命令を終えるのに必要なクロック数</td><td><strong>少ない</strong>ほど速い</td></tr>' +
      '<tr><td>コア数</td><td>CPUの中にある処理装置の数</td><td>同時に複数の処理ができる</td></tr>' +
      '<tr><td>ビット数</td><td>一度に扱えるデータの大きさ</td><td>大きなメモリ空間を扱える</td></tr>' +
      '<tr><td>キャッシュメモリ</td><td>CPUと主記憶装置の間にある高速な記憶</td><td>待ち時間が減る</td></tr></tbody>';
  }

  function init() {
    $('bits').addEventListener('input', drawBits);
    document.querySelectorAll('button[data-b]').forEach(b => b.addEventListener('click', () => { $('bits').value = b.dataset.b; drawBits(); }));
    ['ghz', 'cyc', 'ninst'].forEach(i => $(i).addEventListener('input', drawClock));
    $('preBook').addEventListener('click', () => { $('ghz').value = 30; $('cyc').value = 6; $('ninst').value = 2; drawClock(); });
    window.Terms.glossary($('glossBox'), ['CPU', 'クロック周波数', '主記憶装置', 'レジスタ', '制御装置', '演算装置']);
    drawBits(); drawJudge(); drawQ1(); drawClock(); drawBlanks(); drawFact();
    window.Terms.attach();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
