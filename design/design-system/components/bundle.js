/* @ds-bundle: {"format":4,"namespace":"Donut","components":[{"name":"Icon"},{"name":"Button"},{"name":"IconButton"},{"name":"Chip"},{"name":"SegmentedControl"},{"name":"SelectCard"},{"name":"Toggle"},{"name":"Checkbox"},{"name":"NumberField"},{"name":"ExclusionRow"},{"name":"DistributionEditor"},{"name":"MacroRing"},{"name":"MacroBar"},{"name":"MacroLine"},{"name":"Delta"},{"name":"Badge"},{"name":"Notice"},{"name":"MealCard"},{"name":"DayStrip"},{"name":"RebalanceProposal"},{"name":"IngredientRow"},{"name":"SwapOption"},{"name":"ChangeItem"},{"name":"CompareCard"},{"name":"ConfidencePrompt"},{"name":"ShoppingItem"},{"name":"StatTile"},{"name":"PlanCard"},{"name":"LockedPreview"},{"name":"SectionHeader"},{"name":"NavBar"},{"name":"Avatar"},{"name":"OnboardingProgress"},{"name":"TabBar"},{"name":"BottomAccessory"},{"name":"RecipeHero"},{"name":"PhoneFrame"},{"name":"AppShell"},{"name":"SideNav"},{"name":"TopBar"},{"name":"Dialog"},{"name":"Sheet"},{"name":"Toast"},{"name":"ToastRegion"},{"name":"TextField"},{"name":"Select"},{"name":"WeekTable"},{"name":"OfflineBanner"},{"name":"InstallPrompt"},{"name":"ProfileFileCard"},{"name":"Tooltip"}]} */
(function () {
  var React = window.React;
  var h = React.createElement;
  var useState = React.useState;
  var useEffect = React.useEffect;
  var useRef = React.useRef;

  /* Stable id for label / aria-describedby wiring (no hydration, so a counter is enough). */
  var uidSeq = 0;
  function useUid(prefix) {
    var r = useRef(null);
    if (r.current == null) r.current = (prefix || 'fm') + '-' + (++uidSeq);
    return r.current;
  }

  function cx() {
    var out = [];
    for (var i = 0; i < arguments.length; i++) if (arguments[i]) out.push(arguments[i]);
    return out.join(' ');
  }
  function fmt(n) {
    return Math.round(n).toLocaleString('en-US');
  }
  function signed(n, digits) {
    var abs = Math.abs(n);
    var s = digits ? abs.toFixed(digits) : String(Math.round(abs));
    if (n > 0) return '+' + s;
    if (n < 0) return '−' + s;
    return s;
  }

  /* ---------- Icon ---------- */
  var PATHS = {
    check: 'M5 12.5l4.5 4.5L19 7.5',
    plus: 'M12 5v14M5 12h14',
    minus: 'M5 12h14',
    close: 'M6 6l12 12M18 6L6 18',
    'chevron-right': 'M9 5l7 7-7 7',
    'chevron-left': 'M15 5l-7 7 7 7',
    'chevron-down': 'M5 9l7 7 7-7',
    swap: 'M7 4L3 8l4 4M3 8h14M17 20l4-4-4-4M21 16H7',
    today: 'M12 8a4 4 0 110 8 4 4 0 010-8zM12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4',
    plan: 'M6 5h12a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2zM4 10h16M8 3v4M16 3v4',
    cart: 'M5 8h14l-1.2 11.1a2 2 0 01-2 1.9H8.2a2 2 0 01-2-1.9zM9 8V6.5a3 3 0 016 0V8',
    user: 'M12 4.5a3.5 3.5 0 110 7 3.5 3.5 0 010-7zM5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5',
    lock: 'M7 11h10a1 1 0 011 1v7a1 1 0 01-1 1H7a1 1 0 01-1-1v-7a1 1 0 011-1zM8.5 11V8a3.5 3.5 0 017 0v3',
    clock: 'M12 3.5a8.5 8.5 0 110 17 8.5 8.5 0 010-17zM12 7.5V12l3 2',
    flame: 'M12 21c3.9 0 6.5-2.6 6.5-6.2 0-3.3-2.3-5.4-3.6-7.6-.5 1.9-1.6 3-2.9 3.3.3-2.9-1-5.6-3.4-7.5.1 2.8-1.2 4.6-2.5 6.2C5 10.6 5.5 12.4 5.5 14.8 5.5 18.4 8.1 21 12 21z',
    info: 'M12 3a9 9 0 110 18 9 9 0 010-18zM12 11v5M12 8h.01',
    alert: 'M12 4l9 16H3zM12 10v4M12 17h.01',
    link: 'M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1',
    doc: 'M7 3h7l5 5v12a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1zM14 3v5h5',
    text: 'M5 6h14M5 10h14M5 14h10M5 18h7',
    edit: 'M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4',
    trash: 'M5 7h14M10 7V4.5h4V7M7 7l1 13h8l1-13',
    box: 'M4 8l8-4 8 4v8l-8 4-8-4zM4 8l8 4 8-4M12 12v8',
    leaf: 'M5 19c0-8 5-13 14-14 0 9-5 14-13 14M5 19l7-7',
    repeat: 'M4 11V9a3 3 0 013-3h11M15 3l3 3-3 3M20 13v2a3 3 0 01-3 3H6M9 21l-3-3 3-3',
    search: 'M11 4.5a6.5 6.5 0 110 13 6.5 6.5 0 010-13zM16 16l4.5 4.5',
    fridge: 'M7 3h10a1 1 0 011 1v16a1 1 0 01-1 1H7a1 1 0 01-1-1V4a1 1 0 011-1zM6 10h12M9 6v2M9 13v3',
    wallet: 'M4 7a2 2 0 012-2h11v4M4 7v10a2 2 0 002 2h13V9H6a2 2 0 01-2-2zM16 14h.01',
    heart: 'M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z',
    target: 'M12 3.5a8.5 8.5 0 110 17 8.5 8.5 0 010-17zM12 8a4 4 0 110 8 4 4 0 010-8zM12 11.5v1',
    more: 'M6 12h.01M12 12h.01M18 12h.01',
    settings: 'M12 9a3 3 0 110 6 3 3 0 010-6zM12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1',
    arrow: 'M5 12h14M13 6l6 6-6 6',
    play: 'M8 5.5v13l10.5-6.5z',
    'wifi-off': 'M3 3l18 18M8.5 16.5a5 5 0 017 0M5 12.9a10 10 0 015.2-2.8M16.8 10.4A10 10 0 0119 12.9M2 8.8a15 15 0 014.4-2.7M11 5.1A15 15 0 0122 8.8M12 19.5h.01',
    shield: 'M12 3l7 3v5c0 4.6-3 8.3-7 10-4-1.7-7-5.4-7-10V6z',
    cloud: 'M7 19h10.5a4 4 0 000-8h-.3A5.5 5.5 0 006.6 9.6 4.75 4.75 0 007 19z',
    download: 'M12 4v11M7 10l5 5 5-5M5 20h14',
    upload: 'M12 20V9M7 14l5-5 5 5M5 4h14'
  };
  function Icon(p) {
    var size = p.size || 22;
    var d = PATHS[p.name] || PATHS.info;
    return h('svg', {
      className: cx('fm-icon', p.className),
      width: size, height: size, viewBox: '0 0 24 24', fill: 'none',
      stroke: 'currentColor', strokeWidth: p.weight || 1.75, strokeLinecap: 'round', strokeLinejoin: 'round',
      'aria-hidden': p.label ? undefined : 'true', role: p.label ? 'img' : undefined, 'aria-label': p.label
    }, h('path', { d: d }));
  }
  Icon.names = Object.keys(PATHS);

  /* ---------- Actions ---------- */
  function Button(p) {
    var variant = p.variant || 'primary';
    var size = p.size || 'md';
    var rest = Object.assign({}, p);
    ['variant', 'size', 'icon', 'trailingIcon', 'block', 'className', 'children'].forEach(function (k) { delete rest[k]; });
    return h('button', Object.assign({ type: 'button' }, rest, {
      className: cx('fm-btn', 'fm-btn-' + variant, 'fm-btn-' + size, p.block && 'fm-btn-block', variant.indexOf('glass') === 0 && 'fm-glass', p.className)
    }),
      p.icon && h(Icon, { name: p.icon, size: size === 'sm' ? 16 : 20 }),
      p.children && h('span', null, p.children),
      p.trailingIcon && h(Icon, { name: p.trailingIcon, size: size === 'sm' ? 16 : 20 }));
  }

  function IconButton(p) {
    return h('button', {
      type: 'button', className: cx('fm-iconbtn', p.variant && 'fm-iconbtn-' + p.variant, p.variant && p.variant.indexOf('glass') === 0 && 'fm-glass', p.className),
      'aria-label': p.label, onClick: p.onClick, disabled: p.disabled,
      'aria-describedby': p['aria-describedby'], 'aria-disabled': p['aria-disabled'],
      'aria-haspopup': p['aria-haspopup'], 'aria-expanded': p['aria-expanded']
    }, h(Icon, { name: p.icon, size: p.size || 22 }));
  }

  /* ---------- Inputs ---------- */
  function Chip(p) {
    var ctl = useState(!!p.selected);
    var sel = p.onChange ? !!p.selected : ctl[0];
    function toggle() { if (p.onChange) p.onChange(!sel); else ctl[1](!sel); }
    return h('button', {
      type: 'button', className: cx('fm-chip', sel && 'is-selected', p.className),
      'aria-pressed': sel, onClick: toggle, disabled: p.disabled
    }, sel && h(Icon, { name: 'check', size: 16, weight: 2.25 }), p.icon && !sel && h(Icon, { name: p.icon, size: 16 }), h('span', null, p.children));
  }

  function SegmentedControl(p) {
    var opts = p.options || [];
    var ctl = useState(p.value != null ? p.value : (opts[0] && (opts[0].value != null ? opts[0].value : opts[0])));
    var val = p.onChange ? p.value : ctl[0];
    return h('div', { className: cx('fm-seg', p.className), role: 'radiogroup', 'aria-label': p.label },
      opts.map(function (o) {
        var v = o.value != null ? o.value : o;
        var label = o.label != null ? o.label : o;
        var on = v === val;
        return h('button', {
          key: String(v), type: 'button', role: 'radio', 'aria-checked': on,
          className: cx('fm-seg-item', on && 'is-selected'),
          onClick: function () { if (p.onChange) p.onChange(v); else ctl[1](v); }
        }, label);
      }));
  }

  function SelectCard(p) {
    var ctl = useState(!!p.selected);
    var sel = p.onChange ? !!p.selected : ctl[0];
    return h('button', {
      type: 'button', role: p.multiple ? 'checkbox' : 'radio', 'aria-checked': sel,
      className: cx('fm-selectcard', sel && 'is-selected', p.className),
      onClick: function () { if (p.onChange) p.onChange(!sel); else ctl[1](!sel); }
    },
      p.icon && h('span', { className: 'fm-selectcard-icon' }, h(Icon, { name: p.icon, size: 22 })),
      h('span', { className: 'fm-selectcard-body' },
        h('span', { className: 'fm-selectcard-title' }, p.title),
        p.description && h('span', { className: 'fm-selectcard-desc' }, p.description)),
      p.meta && h('span', { className: 'fm-selectcard-meta' }, p.meta),
      h('span', { className: cx('fm-selectcard-mark', p.multiple && 'is-square') }, sel && h(Icon, { name: 'check', size: 14, weight: 2.5 })));
  }

  function Toggle(p) {
    var ctl = useState(!!p.checked);
    var on = p.onChange ? !!p.checked : ctl[0];
    return h('label', { className: cx('fm-toggle-row', p.className) },
      h('span', { className: 'fm-toggle-text' },
        h('span', { className: 'fm-toggle-label' }, p.label),
        p.description && h('span', { className: 'fm-toggle-desc' }, p.description)),
      h('button', {
        type: 'button', role: 'switch', 'aria-checked': on, 'aria-label': p.label,
        className: cx('fm-toggle', on && 'is-on'), disabled: p.disabled,
        onClick: function () { if (p.onChange) p.onChange(!on); else ctl[1](!on); }
      }, h('span', { className: 'fm-toggle-knob' })));
  }

  function Checkbox(p) {
    var ctl = useState(!!p.checked);
    var on = p.onChange ? !!p.checked : ctl[0];
    return h('button', {
      type: 'button', role: 'checkbox', 'aria-checked': on, 'aria-label': p.label,
      className: cx('fm-check', on && 'is-on', p.className),
      onClick: function () { if (p.onChange) p.onChange(!on); else ctl[1](!on); }
    }, on && h(Icon, { name: 'check', size: 16, weight: 2.5 }));
  }

  function NumberField(p) {
    var hintId = useUid('fm-nf') + '-d';
    return h('label', { className: cx('fm-field', p.large && 'fm-field-lg', p.error && 'is-error', p.className) },
      p.label && h('span', { className: 'fm-field-label' }, p.label),
      h('span', { className: 'fm-field-box' },
        h('input', {
          className: 'fm-field-input', inputMode: 'numeric', defaultValue: p.value, placeholder: p.placeholder,
          'aria-invalid': p.error ? 'true' : undefined,
          'aria-describedby': (p.error || p.hint) ? hintId : undefined
        }),
        p.unit && h('span', { className: 'fm-field-unit' }, p.unit)),
      (p.error || p.hint) && h('span', { id: hintId, className: cx('fm-field-hint', p.error && 'is-error') },
        p.error && h(Icon, { name: 'alert', size: 14 }), p.error || p.hint));
  }

  var SEVERITIES = [
    { id: 'allergy', label: 'Allergy' },
    { id: 'intolerance', label: 'Intolerance' },
    { id: 'dislike', label: "Don't like" },
    { id: 'prefer-not', label: 'Prefer not' }
  ];
  function ExclusionRow(p) {
    var ctl = useState(p.severity || null);
    var sev = p.onChange ? p.severity : ctl[0];
    var rl = useState(!!p.relaxed);
    function set(v) { var nv = v === sev ? null : v; if (p.onChange) p.onChange(nv); else ctl[1](nv); }
    return h('div', { className: cx('fm-excl', sev && 'is-set', p.className) },
      h('div', { className: 'fm-excl-head' },
        h('span', { className: 'fm-excl-name' }, p.name),
        p.examples && h('span', { className: 'fm-excl-ex' }, p.examples)),
      h('div', { className: 'fm-excl-tiers', role: 'radiogroup', 'aria-label': 'Severity for ' + p.name },
        SEVERITIES.map(function (s) {
          var on = sev === s.id;
          return h('button', {
            key: s.id, type: 'button', role: 'radio', 'aria-checked': on,
            className: cx('fm-excl-tier', 'fm-tier-' + s.id, on && 'is-selected'), onClick: function () { set(s.id); }
          }, s.id === 'allergy' && on && h(Icon, { name: 'alert', size: 14 }), s.label);
        })),
      sev === 'allergy' && h('p', { className: 'fm-excl-note is-allergy' }, h(Icon, { name: 'shield', size: 14, weight: 2 }),
        'Never planned or suggested \u2014 including \u201cmay contain\u201d traces.'),
      sev === 'intolerance' && h('div', { className: 'fm-excl-relax' },
        h(Checkbox, { checked: rl[0], onChange: function (v) { rl[1](v); }, label: 'Avoid when possible' }),
        h('span', null, rl[0]
          ? h(React.Fragment, null, h('b', null, 'Avoid when possible. '), 'Used only when nothing else fits, and always labelled.')
          : h(React.Fragment, null, h('b', null, 'Never planned. '), 'Traces are OK. Tick to allow it when nothing else fits.'))));
  }

  function DistributionEditor(p) {
    var meals = p.meals || [];
    var kcal = p.kcal || 0;
    var colors = ['var(--basil)', 'var(--paprika)', 'var(--macro-fat)', 'var(--macro-carbs)', 'var(--ink-muted)'];
    return h('div', { className: cx('fm-dist', p.className) },
      h('div', { className: 'fm-dist-bar', role: 'img', 'aria-label': meals.map(function (m) { return m.name + ' ' + m.pct + '%'; }).join(', ') },
        meals.map(function (m, i) {
          return h('span', { key: m.name, className: 'fm-dist-seg', style: { flexGrow: m.pct, background: colors[i % colors.length] } });
        })),
      h('div', { className: 'fm-dist-rows' },
        meals.map(function (m, i) {
          return h('div', { key: m.name, className: 'fm-dist-row' },
            h('span', { className: 'fm-dot', style: { background: colors[i % colors.length] } }),
            h('span', { className: 'fm-dist-name' }, m.name),
            h('span', { className: 'fm-dist-kcal' }, kcal ? fmt(kcal * m.pct / 100) + ' kcal' : ''),
            h('span', { className: 'fm-dist-stepper' },
              h(IconButton, { icon: 'minus', label: 'Less for ' + m.name, size: 18, variant: 'sunken' }),
              h('span', { className: 'fm-dist-pct' }, m.pct + '%'),
              h(IconButton, { icon: 'plus', label: 'More for ' + m.name, size: 18, variant: 'sunken' })));
        })));
  }

  /* ---------- Nutrition ---------- */
  var MACROS = {
    protein: { letter: 'P', label: 'Protein', color: 'var(--macro-protein)' },
    carbs: { letter: 'C', label: 'Carbs', color: 'var(--macro-carbs)' },
    fat: { letter: 'F', label: 'Fat', color: 'var(--macro-fat)' }
  };

  function MacroRing(p) {
    var size = p.size || 168;
    var stroke = p.stroke || Math.round(size / 12);
    var r = (size - stroke) / 2;
    var c = 2 * Math.PI * r;
    var pct = p.target ? Math.min(p.value / p.target, 1) : 0;
    var over = p.target && p.value > p.target * 1.03;
    var inner = r - stroke - 3;
    var ci = 2 * Math.PI * inner;
    var macros = p.macros || null;
    var rings = [];
    if (macros) {
      var gap = 4 / ci;
      var start = 0;
      ['protein', 'carbs', 'fat'].forEach(function (k) {
        var m = macros[k];
        if (!m) return;
        var frac = Math.max(0, m.share - gap);
        rings.push(h('circle', {
          key: k, cx: size / 2, cy: size / 2, r: inner, fill: 'none', stroke: MACROS[k].color, strokeWidth: 4,
          strokeDasharray: (frac * ci) + ' ' + ci, strokeDashoffset: -start * ci, strokeLinecap: 'butt',
          transform: 'rotate(-90 ' + size / 2 + ' ' + size / 2 + ')'
        }));
        start += m.share;
      });
    }
    return h('div', { className: cx('fm-ring', p.className), style: { width: size, height: size } },
      h('svg', { width: size, height: size, viewBox: '0 0 ' + size + ' ' + size, 'aria-hidden': 'true' },
        h('circle', { cx: size / 2, cy: size / 2, r: r, fill: 'none', stroke: 'var(--macro-track)', strokeWidth: stroke }),
        h('circle', {
          cx: size / 2, cy: size / 2, r: r, fill: 'none', stroke: over ? 'var(--warning)' : 'var(--basil)', strokeWidth: stroke,
          strokeDasharray: (pct * c) + ' ' + c, strokeLinecap: 'round', transform: 'rotate(-90 ' + size / 2 + ' ' + size / 2 + ')'
        }),
        rings),
      h('div', { className: 'fm-ring-center', role: 'img', 'aria-label': fmt(p.value) + ' of ' + fmt(p.target) + ' kilocalories' },
        h('span', { className: 'fm-ring-value', style: size < 168 ? { fontSize: Math.round(size * 0.235), lineHeight: 1 } : null }, fmt(p.value)),
        size >= 140 && h('span', { className: 'fm-ring-label' }, p.label || ('of ' + fmt(p.target) + ' kcal'))));
  }

  function MacroBar(p) {
    var m = MACROS[p.macro] || MACROS.protein;
    var pct = p.target ? Math.min(p.value / p.target, 1) * 100 : 0;
    var met = p.mode === 'min' ? p.value >= p.target : Math.abs(p.value - p.target) <= p.target * 0.05;
    return h('div', { className: cx('fm-mbar', p.compact && 'is-compact', p.className) },
      h('div', { className: 'fm-mbar-head' },
        h('span', { className: 'fm-mbar-label' }, h('span', { className: 'fm-dot', style: { background: m.color } }), m.label),
        h('span', { className: 'fm-mbar-val' },
          h('b', null, fmt(p.value)), ' / ', (p.mode === 'min' ? '≥' : '') + fmt(p.target) + ' g',
          met && h(Icon, { name: 'check', size: 14, weight: 2.5, className: 'fm-mbar-ok', label: 'Target met' }))),
      h('div', { className: 'fm-mbar-track' }, h('span', { className: 'fm-mbar-fill', style: { width: pct + '%', background: m.color } })));
  }

  function MacroLine(p) {
    var items = [];
    if (p.kcal != null) items.push(h('span', { key: 'k', className: 'fm-mline-kcal' }, fmt(p.kcal), h('small', null, ' kcal')));
    ['protein', 'carbs', 'fat'].forEach(function (k) {
      if (p[k] == null) return;
      items.push(h('span', { key: k, className: 'fm-mline-item' },
        h('span', { className: 'fm-dot', style: { background: MACROS[k].color } }), fmt(p[k]), h('small', null, ' ' + MACROS[k].letter)));
    });
    return h('span', { className: cx('fm-mline', p.size === 'lg' && 'is-lg', p.className) }, items);
  }

  function Delta(p) {
    var items = p.items || [];
    return h('span', { className: cx('fm-delta', p.className) },
      items.map(function (it, i) {
        var tone = it.tone || 'neutral';
        var txt = it.unit === 'PLN' ? signed(it.value, 2) + ' PLN' : signed(it.value) + (it.unit === 'kcal' ? ' kcal' : ' g ' + (it.letter || 'P'));
        return h('span', { key: i, className: cx('fm-delta-item', 'is-' + tone) }, txt);
      }));
  }

  /* ---------- Status ---------- */
  function Badge(p) {
    return h('span', { className: cx('fm-badge', 'fm-badge-' + (p.tone || 'neutral'), p.className) },
      p.icon && h(Icon, { name: p.icon, size: 13, weight: 2 }), p.children);
  }

  var NOTICE_ICONS = { danger: 'alert', warning: 'alert', info: 'info', offline: 'wifi-off' };
  function Notice(p) {
    var tone = p.tone || 'info';
    return h('section', { className: cx('fm-notice', 'is-' + tone, p.className), role: tone === 'danger' ? 'alert' : 'status' },
      h('div', { className: 'fm-notice-head' },
        h('span', { className: 'fm-notice-icon' }, h(Icon, { name: p.icon || NOTICE_ICONS[tone], size: 18, weight: 2 })),
        h('div', { className: 'fm-notice-text' },
          p.title && h('p', { className: 'fm-notice-title' }, p.title),
          p.body && h('p', { className: 'fm-notice-body' }, p.body))),
      p.items && h('ul', { className: 'fm-notice-items' }, p.items.map(function (it, i) { return h('li', { key: i }, it); })),
      p.actions && h('div', { className: 'fm-notice-actions' }, p.actions.map(function (a, i) {
        return h(Button, { key: i, variant: i === 0 ? 'primary' : 'quiet', size: 'sm', icon: a.icon }, a.label || a);
      })));
  }

  /* ---------- Meals ---------- */
  function MealCard(p) {
    var status = p.status || 'planned';
    var locked = status === 'eaten' || status === 'skipped';
    var badges = (p.badges || []).slice();
    if (p.prep) badges.unshift({ label: 'Meal prep ' + p.prep.portion + ' \u00b7 cook ' + p.prep.cook + ' \u00b7 eat by ' + p.prep.eatBy, tone: 'paprika', icon: 'repeat' });
    if (status === 'cooked') badges.unshift({ label: 'Cooked', tone: 'basil', icon: 'flame' });
    var pill = status === 'eaten' ? { cls: 'is-on', icon: 'lock', text: 'Eaten', label: 'Eaten. Locked: swaps and rebalances won\u2019t change it' }
      : status === 'skipped' ? { cls: 'is-skipped', icon: 'lock', text: 'Skipped', label: 'Skipped. Locked: swaps and rebalances won\u2019t change it' }
      : { cls: '', icon: 'check', text: 'Eat', label: 'Mark as eaten' };
    return h('article', { className: cx('fm-meal', locked && 'is-locked', 'is-' + status, p.className) },
      h('div', { className: 'fm-meal-top' },
        h('span', { className: 'fm-meal-slot' }, p.slot, p.time && h('span', { className: 'fm-meal-time' }, ' \u00b7 ' + p.time)),
        p.onToggleEaten !== false && h('button', {
          type: 'button', className: cx('fm-meal-eat', pill.cls), 'aria-pressed': status === 'eaten', 'aria-label': pill.label
        }, h(Icon, { name: pill.icon, size: 15, weight: 2.25 }), pill.text)),
      h('h3', { className: 'fm-meal-title' }, p.title),
      h(MacroLine, { kcal: p.kcal, protein: p.protein, carbs: p.carbs, fat: p.fat }),
      badges.length ? h('div', { className: 'fm-meal-badges' }, badges.map(function (b, i) {
        return h(Badge, { key: i, tone: b.tone, icon: b.icon }, b.label);
      })) : null,
      p.actions !== false && h('div', { className: 'fm-meal-actions' },
        h(Button, { variant: 'secondary', size: 'sm', icon: 'doc' }, 'Recipe'),
        !locked && p.swappable !== false && h(Button, { variant: 'quiet', size: 'sm', icon: 'swap' }, 'Swap')));
  }

  function DayStrip(p) {
    var days = p.days || [];
    return h('div', { className: cx('fm-days', p.className), role: 'tablist' },
      days.map(function (d, i) {
        var on = i === (p.selected || 0);
        return h('button', { key: i, type: 'button', role: 'tab', 'aria-selected': on, className: cx('fm-day', on && 'is-selected') },
          h('span', { className: 'fm-day-name' }, d.name),
          h('span', { className: 'fm-day-num' }, d.num),
          h('span', { className: cx('fm-day-dot', 'is-' + (d.state || 'planned')), 'aria-label': d.state || 'planned' }));
      }));
  }

  function RebalanceProposal(p) {
    var adj = p.adjustments || [];
    var st = useState(adj.map(function (a) { return a.accepted !== false; }));
    var unreachable = !!p.unreachable;
    return h('section', { className: cx('fm-rebal', unreachable && 'is-unreachable', p.className), 'aria-live': 'polite' },
      h('div', { className: 'fm-rebal-head' },
        h(Icon, { name: unreachable ? 'alert' : 'target', size: 20 }),
        h('div', null,
          h('p', { className: 'fm-rebal-title' }, p.title || 'Rebalance your day?'),
          p.body && h('p', { className: 'fm-rebal-body' }, p.body))),
      (adj.length || (p.locked && p.locked.length)) ? h('div', { className: 'fm-rebal-list' },
        adj.map(function (a, i) {
          return h('div', { key: 'a' + i, className: cx('fm-rebal-row', !st[0][i] && 'is-off') },
            h(Checkbox, { checked: st[0][i], label: 'Adjust ' + a.meal, onChange: function (v) { var n = st[0].slice(); n[i] = v; st[1](n); } }),
            h('span', { className: 'fm-rebal-meal' }, a.meal, h('small', null, ' portion ' + a.portion)),
            h('span', { className: 'fm-rebal-delta' }, a.kcal));
        }),
        (p.locked || []).map(function (l, i) {
          return h('div', { key: 'l' + i, className: 'fm-rebal-row is-locked' },
            h('span', { className: 'fm-rebal-lock' }, h(Icon, { name: 'lock', size: 15 })),
            h('span', { className: 'fm-rebal-meal' }, l.meal, h('small', null, ' ' + l.reason)),
            h('span', { className: 'fm-rebal-delta' }, 'no change'));
        })) : null,
      p.before && h('div', { className: 'fm-rebal-compare' },
        h('div', null, h('span', { className: 'fm-cap' }, 'Now'), h(MacroLine, { kcal: p.before.kcal, protein: p.before.protein })),
        h(Icon, { name: 'arrow', size: 18, className: 'fm-muted' }),
        h('div', null, h('span', { className: 'fm-cap' }, unreachable ? 'Best possible' : 'With changes'), h(MacroLine, { kcal: p.after.kcal, protein: p.after.protein }))),
      h('div', { className: 'fm-rebal-actions' }, unreachable
        ? [h(Button, { key: 1, variant: 'primary', size: 'sm' }, 'Accept anyway'), h(Button, { key: 2, variant: 'quiet', size: 'sm' }, 'Different swap'), h(Button, { key: 3, variant: 'quiet', size: 'sm' }, 'Undo swap')]
        : [h(Button, { key: 1, variant: 'primary', size: 'sm' }, p.cta || 'Apply changes'), h(Button, { key: 2, variant: 'quiet', size: 'sm' }, 'Keep day as is')]));
  }

  /* ---------- Recipes ---------- */
  function IngredientRow(p) {
    var changed = p.was != null;
    return h('div', { className: cx('fm-ing', changed && 'is-changed', p.excluded && 'is-excluded', p.className) },
      p.checkable && h(Checkbox, { checked: p.checked, label: p.name }),
      h('div', { className: 'fm-ing-main' },
        h('span', { className: 'fm-ing-name' }, p.name,
          p.excluded && h(Badge, { tone: 'danger', icon: 'alert' }, p.excluded)),
        h('span', { className: 'fm-ing-amount' },
          changed && h('s', { className: 'fm-ing-was' }, p.was), changed && ' → ',
          h('span', { className: changed ? 'fm-ing-now' : '' }, p.amount),
          p.role && h('span', { className: 'fm-ing-role' }, ' · ' + p.role))),
      p.swappable !== false && h('button', { type: 'button', className: 'fm-ing-swap', 'aria-label': 'Swap ' + p.name },
        h(Icon, { name: 'swap', size: 18 }), h('span', null, 'Swap')));
  }

  function SwapOption(p) {
    return h('button', {
      type: 'button', role: 'radio', 'aria-checked': !!p.selected,
      className: cx('fm-swapopt', p.selected && 'is-selected', p.className)
    },
      h('span', { className: 'fm-swapopt-body' },
        h('span', { className: 'fm-swapopt-title' }, p.title,
          p.amount && h('span', { className: 'fm-swapopt-amt' }, ' ' + p.amount),
          p.best && h(Badge, { tone: 'basil' }, 'Best fit')),
        p.delta && h(Delta, { items: p.delta }),
        p.note && h('span', { className: 'fm-swapopt-note' }, p.note)),
      h('span', { className: 'fm-selectcard-mark' }, p.selected && h(Icon, { name: 'check', size: 14, weight: 2.5 })));
  }

  function ChangeItem(p) {
    var ctl = useState(!p.rejected);
    var kept = ctl[0];
    return h('li', { className: cx('fm-change', !kept && 'is-rejected', p.className) },
      h('span', { className: 'fm-change-icon' }, h(Icon, { name: p.icon || 'edit', size: 16 })),
      h('span', { className: 'fm-change-body' },
        h('span', { className: 'fm-change-what' }, p.what),
        h('span', { className: 'fm-change-effect' }, kept ? p.effect : 'Rejected. Donut re-solves without it.')),
      p.decidable !== false && h('button', {
        type: 'button', className: cx('fm-change-toggle', kept && 'is-on'), 'aria-pressed': kept,
        'aria-label': (kept ? 'Keep: ' : 'Rejected: ') + p.what, onClick: function () { ctl[1](!kept); }
      }, kept ? h(React.Fragment, null, h(Icon, { name: 'check', size: 14, weight: 2.5 }), 'Keep') : 'Undo'));
  }

  function CompareCard(p) {
    var o = p.original, y = p.yours;
    function col(label, d, isYours) {
      return h('div', { className: cx('fm-cmp-col', isYours && 'is-yours') },
        h('span', { className: 'fm-cap' }, label),
        h('span', { className: 'fm-cmp-kcal' }, fmt(d.kcal), h('small', null, ' kcal')),
        h('span', { className: 'fm-cmp-p' }, h('span', { className: 'fm-dot', style: { background: 'var(--macro-protein)' } }), fmt(d.protein) + ' g protein'),
        !isYours && p.sourceKcal != null && h('span', { className: 'fm-cmp-source' }, 'Source says ' + fmt(p.sourceKcal) + ' kcal'));
    }
    return h('section', { className: cx('fm-cmp', p.className) },
      p.missed
        ? h('p', { className: 'fm-cmp-missed' }, h(Icon, { name: 'alert', size: 16, weight: 2 }), p.missed)
        : p.found !== false && h('p', { className: 'fm-cmp-found' }, h(Icon, { name: 'check', size: 16, weight: 2.5 }), p.foundLabel || 'Optimized version found'),
      h('div', { className: 'fm-cmp-grid' },
        col(p.originalLabel || 'Original', o, false),
        h('span', { className: 'fm-cmp-arrow' }, h(Icon, { name: 'arrow', size: 20 })),
        col(p.yoursLabel || 'Your version', y, true)),
      p.target && h('p', { className: 'fm-cmp-target' }, p.target),
      p.sourceKcal != null && h('p', { className: 'fm-cmp-target' }, 'Donut calculates every number itself. The source\u2019s figure is shown for comparison only.'));
  }

  function ConfidencePrompt(p) {
    var ctl = useState(p.selected != null ? p.selected : null);
    return h('section', { className: cx('fm-conf', p.className) },
      h('div', { className: 'fm-conf-head' },
        h(Badge, { tone: 'warning', icon: 'alert' }, 'Check this'),
        h('span', { className: 'fm-conf-raw' }, '“' + p.raw + '”')),
      h('p', { className: 'fm-conf-q' }, p.question),
      h('div', { className: 'fm-conf-opts' }, (p.options || []).map(function (o) {
        return h(Chip, { key: o, selected: ctl[0] === o, onChange: function () { ctl[1](o); } }, o);
      })),
      ctl[0] == null && h('p', { className: 'fm-conf-note' }, h(Icon, { name: 'lock', size: 13, weight: 2 }), p.note || 'Until you choose, this recipe can\u2019t be planned.'));
  }

  /* ---------- Shopping ---------- */
  function ShoppingItem(p) {
    var ctl = useState(!!p.checked);
    var on = ctl[0];
    return h('div', { className: cx('fm-shop', on && !p.extra && 'is-done', on && p.extra && 'is-grown', p.className) },
      h(Checkbox, { checked: on, onChange: function (v) { ctl[1](v); }, label: p.name }),
      h('div', { className: 'fm-shop-main' },
        h('span', { className: 'fm-shop-name' }, p.name),
        (p.packages || p.pantry) && h('span', { className: 'fm-shop-meta' },
          p.packages && h('span', null, h(Icon, { name: 'box', size: 13 }), ' ' + p.packages),
          p.pantry && h('span', { className: 'fm-shop-pantry' }, h(Icon, { name: 'fridge', size: 13 }), ' ' + p.pantry)),
        p.extra && h('span', { className: 'fm-shop-extra' }, h(Icon, { name: 'plus', size: 13, weight: 2.25 }), ' ' + p.extra + ' more to buy')),
      h('span', { className: 'fm-shop-qty' }, p.qty, p.price && h('small', null, p.price)));
  }

  function StatTile(p) {
    return h('div', { className: cx('fm-stat', p.className) },
      h('span', { className: 'fm-stat-value' }, p.value, p.unit && h('small', null, ' ' + p.unit)),
      h('span', { className: 'fm-stat-label' }, p.label),
      p.note && h('span', { className: 'fm-stat-note' }, p.note));
  }

  /* ---------- Monetization ---------- */
  function PlanCard(p) {
    var tier = p.tier || 'standard';
    return h('div', { className: cx('fm-plan', 'fm-plan-' + tier, p.selected && 'is-selected', p.soon && 'is-soon', p.className), role: 'radio', 'aria-checked': !!p.selected },
      h('div', { className: 'fm-plan-head' },
        h('span', { className: 'fm-plan-name' }, p.name),
        p.flag && h(Badge, { tone: tier === 'premium' ? 'premium' : 'basil' }, p.flag)),
      h('p', { className: 'fm-plan-promise' }, p.promise),
      h('div', { className: 'fm-plan-price' },
        h('span', { className: 'fm-plan-amount' }, p.price),
        p.period && h('span', { className: 'fm-plan-period' }, p.period)),
      p.subprice && h('p', { className: 'fm-plan-sub' }, p.subprice),
      p.features && h('ul', { className: 'fm-plan-feats' }, p.features.map(function (f, i) {
        return h('li', { key: i }, h(Icon, { name: 'check', size: 16, weight: 2.25 }), f);
      })));
  }

  function LockedPreview(p) {
    return h('section', { className: cx('fm-locked', p.tier === 'premium' && 'is-premium', p.className) },
      h('p', { className: 'fm-locked-kicker' }, h(Icon, { name: 'check', size: 16, weight: 2.5 }), p.kicker),
      h('div', { className: 'fm-locked-stats' }, (p.stats || []).map(function (s, i) {
        return h('div', { key: i, className: 'fm-locked-stat' },
          h('span', { className: 'fm-cap' }, s.label),
          h('span', { className: 'fm-locked-from' }, s.from),
          h('span', { className: 'fm-locked-to' }, s.to));
      })),
      p.note && h('p', { className: 'fm-locked-note' }, p.note),
      h(Button, { variant: p.tier === 'premium' ? 'premium' : 'primary', block: true, icon: 'lock' }, p.cta));
  }

  /* ---------- Navigation ---------- */
  function SectionHeader(p) {
    return h('div', { className: cx('fm-sechead', p.className) },
      h('span', { className: 'fm-cap' }, p.title),
      p.meta && h('span', { className: 'fm-sechead-meta' }, p.meta),
      p.action && h('button', { type: 'button', className: 'fm-link' }, p.action));
  }

  function NavBar(p) {
    var trailing = (p.trailing || p.avatar)
      ? h('span', { className: 'fm-nav-right' }, p.trailing && h('span', { className: 'fm-glass fm-glass-group' }, p.trailing), p.avatar)
      : h('span', { className: 'fm-nav-spacer' });
    var lead = p.back
      ? h('button', { type: 'button', className: 'fm-glass fm-glassbtn', 'aria-label': p.back === 'Cancel' ? 'Cancel' : 'Back to ' + p.back },
          h(Icon, { name: p.back === 'Cancel' ? 'close' : 'chevron-left', size: 22, weight: 2 }))
      : h('span', { className: 'fm-nav-spacer' });
    return h('header', { className: cx('fm-nav', p.large && 'is-large', p.overlay && 'is-overlay', p.className) },
      (p.back || p.trailing || p.avatar || !p.large) && h('div', { className: 'fm-nav-row' },
        lead,
        !p.large && h('span', { className: 'fm-nav-title' }, p.title),
        trailing),
      p.large && h('h1', { className: 'fm-nav-large' }, p.title),
      p.subtitle && h('p', { className: 'fm-nav-sub' }, p.subtitle));
  }

  function Avatar(p) {
    var size = p.size || 36;
    return h('button', {
      type: 'button', className: cx('fm-avatar', p.className), 'aria-label': p.label || 'Profile',
      style: { width: Math.max(44, size), height: Math.max(44, size) }
    },
      h('span', { className: 'fm-avatar-face', style: { width: size, height: size, fontSize: Math.round(size * 0.38) } }, p.initials || h(Icon, { name: 'user', size: Math.round(size * 0.55) })),
      p.badge && h('span', { className: 'fm-avatar-badge', 'aria-label': typeof p.badge === 'string' ? p.badge : 'New' }));
  }

  function OnboardingProgress(p) {
    var total = p.total || 14;
    var step = p.step || 1;
    return h('div', { className: cx('fm-onbprog', p.className) },
      h('button', { type: 'button', className: 'fm-glass fm-glassbtn', 'aria-label': 'Back' }, h(Icon, { name: 'chevron-left', size: 22, weight: 2 })),
      h('div', { className: 'fm-onbprog-track', role: 'progressbar', 'aria-valuemin': 1, 'aria-valuemax': total, 'aria-valuenow': step },
        h('span', { style: { width: (step / total * 100) + '%' } })),
      h('span', { className: 'fm-onbprog-count' }, step + '/' + total));
  }

  var TABS = [
    { id: 'today', label: 'Today', icon: 'today' },
    { id: 'plan', label: 'Plan', icon: 'plan' },
    { id: 'shopping', label: 'Shopping', icon: 'cart' }
  ];
  function TabBar(p) {
    var active = p.active || 'today';
    var min = !!p.minimized;
    var copy = wc(p.lang);
    var tabs = min ? TABS.filter(function (t) { return t.id === active; }) : TABS;
    var bar = h('nav', { className: cx('fm-glass', 'fm-tabbar', min && 'is-min'), 'aria-label': copy.nav },
      tabs.map(function (t) {
        var on = t.id === active;
        var label = copy[t.id];
        var props = { key: t.id, className: cx('fm-tab', on && 'is-active'), 'aria-current': on ? 'page' : undefined, 'aria-label': label };
        var inner = [h(Icon, { key: 'i', name: t.icon, size: min ? 24 : 23, weight: on ? 2.1 : 1.7 }), !min && h('span', { key: 'l' }, label)];
        /* Web: `links` renders real <a href> so Back, refresh and deep links work. */
        return p.links
          ? h('a', Object.assign(props, { href: (p.hrefs && p.hrefs[t.id]) || '/' + t.id, onClick: p.onNavigate ? function (e) { p.onNavigate(t.id, e); } : undefined }), inner)
          : h('button', Object.assign(props, { type: 'button' }), inner);
      }));
    var add = h('button', { type: 'button', className: 'fm-glass fm-glass-accent fm-tab-add', 'aria-label': copy.add, onClick: p.onAdd },
      h(Icon, { name: 'plus', size: 26, weight: 2.25 }));
    return h('div', { className: cx('fm-tabbar-wrap', min && 'is-min', p.className) },
      p.accessory && !min && h('div', { className: 'fm-tabbar-acc' }, p.accessory),
      h('div', { className: 'fm-tabbar-row' }, bar, min && p.accessory && h('div', { className: 'fm-tabbar-inline' }, p.accessory), add));
  }

  function BottomAccessory(p) {
    return h('div', { className: cx('fm-glass', 'fm-acc', p.className), role: 'status' },
      h('span', { className: cx('fm-acc-icon', 'is-' + (p.tone || 'basil')) }, h(Icon, { name: p.icon || 'clock', size: 18, weight: 2 })),
      h('span', { className: 'fm-acc-text' },
        h('span', { className: 'fm-acc-title' }, p.title),
        p.subtitle && h('span', { className: 'fm-acc-sub' }, p.subtitle)),
      p.progress != null && h('span', { className: 'fm-acc-progress', style: { width: Math.round(p.progress * 100) + '%' } }),
      p.action && h('button', { type: 'button', className: 'fm-acc-action' }, p.action));
  }

  function RecipeHero(p) {
    var m = p.macros || { protein: 0.34, carbs: 0.4, fat: 0.26 };
    var H = p.height || 300, W = 375, cxp = W / 2, cyp = H / 2 + 22, R = 92, C = 2 * Math.PI * 62;
    var start = 0;
    var arcs = ['protein', 'carbs', 'fat'].map(function (k) {
      var frac = m[k] || 0;
      var el = h('circle', { key: k, cx: cxp, cy: cyp, r: 62, fill: 'none', stroke: MACROS[k].color, strokeWidth: 40,
        strokeDasharray: Math.max(0, frac * C - 5) + ' ' + C, strokeDashoffset: -start * C, transform: 'rotate(-90 ' + cxp + ' ' + cyp + ')' });
      start += frac;
      return el;
    });
    return h('div', { className: cx('fm-hero', 'is-' + (p.tone || 'paprika'), p.className), style: { height: H } },
      h('svg', { width: '100%', height: H, viewBox: '0 0 ' + W + ' ' + H, preserveAspectRatio: 'xMidYMid slice', 'aria-hidden': 'true' },
        h('circle', { className: 'fm-hero-disc', cx: 40, cy: 40, r: 70 }),
        h('circle', { className: 'fm-hero-disc', cx: W - 20, cy: H - 10, r: 90 }),
        h('circle', { className: 'fm-hero-plate', cx: cxp, cy: cyp, r: R + 16 }),
        h('circle', { className: 'fm-hero-rim', cx: cxp, cy: cyp, r: R }),
        arcs,
        h('circle', { className: 'fm-hero-center', cx: cxp, cy: cyp, r: 30 })),
      p.children);
  }

  function PhoneFrame(p) {
    return h('div', { className: cx('fm-phone', p.className) },
      p.caption && h('p', { className: 'fm-phone-caption' }, p.caption),
      h('div', { className: 'fm-phone-body', 'data-theme': p.theme },
        h('div', { className: 'fm-phone-status' },
          h('span', null, '9:41'),
          h('span', { className: 'fm-phone-island' }),
          h('span', { className: 'fm-phone-sig' }, h('i'), h('i'), h('i'))),
        h('div', { className: 'fm-phone-screen' }, p.children, p.footer),
        h('div', { className: 'fm-phone-home' }, h('span'))));
  }

  /* =====================================================================
     Web (mobile-first responsive PWA). Breakpoints: sm < 600, md 600–1023,
     lg >= 1024. Numbers repeat tokens.json `breakpoint-*`, because media and
     container queries can't read CSS variables.
     ===================================================================== */
  var WEB_COPY = {
    en: {
      skip: 'Skip to main content', nav: 'Main', today: 'Today', plan: 'Plan', shopping: 'Shopping', add: 'Add recipe', profile: 'Profile',
      backTo: 'Back to', close: 'Close', optional: 'optional', dismiss: 'Dismiss', notNow: 'Not now',
      offline: 'You’re offline. Your plan and meal check-offs still work.',
      pending: { one: '# change is waiting to sync.', other: '# changes are waiting to sync.' },
      syncing: { one: 'You’re back online. Syncing # change…', other: 'You’re back online. Syncing # changes…' },
      synced: 'You’re back online. Everything is synced.',
      stuck: 'Some check-offs haven’t synced yet.', retry: 'Try again',
      installTitle: 'Use your plan offline',
      installBody: 'Add Donut to your home screen to use your plan without a connection.',
      installCta: 'Install Donut',
      installIos: 'In Safari, tap Share, then Add to Home Screen.',
      pfTitle: 'Nutrition profile · In this browser',
      pfWhere: 'Your profile is saved in this browser on this device. We receive it only to build a plan or swap, and don’t keep it.',
      pfLoss: 'If you clear this site’s data, use private browsing, or switch browser or device, your profile won’t be there. Download a copy to keep it safe.',
      pfDownload: 'Download my profile', pfLoad: 'Load a profile file',
      pfWarn: 'This file contains your allergies and targets. Keep it private.',
      pfLast: 'Last downloaded {date}', pfNever: 'Not downloaded yet',
      pfInvalid: 'We can’t read this file. Choose a profile file downloaded from Donut (.json).',
      pfPersist: 'Your browser may clear stored data when space runs low. Download a copy of your profile to be safe.',
      wkCaption: 'Your plan', wkMeal: 'Meal', wkTotal: 'Day total', wkNoMeal: 'No meal', wkToday: 'Today', wkCook: 'Cook day',
      eat: 'Eat', eaten: 'Eaten', skipped: 'Skipped', locked: 'Locked', queued: 'Saved on this device, will sync',
      eatA11y: 'Eat {slot}, {day}'
    },
    pl: {
      skip: 'Przejdź do treści', nav: 'Menu główne', today: 'Dzisiaj', plan: 'Plan', shopping: 'Zakupy', add: 'Dodaj przepis', profile: 'Profil',
      backTo: 'Wróć do:', close: 'Zamknij', optional: 'opcjonalnie', dismiss: 'Zamknij', notNow: 'Nie teraz',
      offline: 'Jesteś offline. Plan i odhaczanie posiłków nadal działają.',
      pending: { one: '# zmiana czeka na synchronizację.', few: '# zmiany czekają na synchronizację.', many: '# zmian czeka na synchronizację.' },
      syncing: { one: 'Znów jesteś online. Synchronizujemy # zmianę…', few: 'Znów jesteś online. Synchronizujemy # zmiany…', many: 'Znów jesteś online. Synchronizujemy # zmian…' },
      synced: 'Znów jesteś online. Wszystko jest zsynchronizowane.',
      stuck: 'Część odhaczonych posiłków jeszcze się nie zsynchronizowała.', retry: 'Spróbuj ponownie',
      installTitle: 'Korzystaj z planu offline',
      installBody: 'Dodaj Donut do ekranu początkowego, aby korzystać z planu bez internetu.',
      installCta: 'Zainstaluj Donut',
      installIos: 'W Safari stuknij Udostępnij, a potem Do ekranu początkowego.',
      pfTitle: 'Profil żywieniowy · W tej przeglądarce',
      pfWhere: 'Twój profil jest zapisany w tej przeglądarce na tym urządzeniu. Otrzymujemy go tylko, by ułożyć plan lub zamianę, i go nie przechowujemy.',
      pfLoss: 'Jeśli wyczyścisz dane tej witryny, użyjesz trybu prywatnego albo zmienisz przeglądarkę lub urządzenie, profilu tam nie będzie. Pobierz kopię, aby go nie stracić.',
      pfDownload: 'Pobierz mój profil', pfLoad: 'Wczytaj plik profilu',
      pfWarn: 'Ten plik zawiera Twoje alergie i cele. Nie udostępniaj go.',
      pfLast: 'Ostatnio pobrano: {date}', pfNever: 'Jeszcze nie pobrano',
      pfInvalid: 'Nie możemy odczytać tego pliku. Wybierz plik profilu pobrany z Donut (.json).',
      pfPersist: 'Przeglądarka może usunąć zapisane dane, gdy zabraknie miejsca. Pobierz kopię profilu na wszelki wypadek.',
      wkCaption: 'Twój plan', wkMeal: 'Posiłek', wkTotal: 'Suma dnia', wkNoMeal: 'Brak posiłku', wkToday: 'Dzisiaj', wkCook: 'Dzień gotowania',
      eat: 'Zjedz', eaten: 'Zjedzone', skipped: 'Pominięte', locked: 'Zablokowane', queued: 'Zapisano na tym urządzeniu, zsynchronizuje się później',
      eatA11y: 'Zjedz: {slot}, {day}'
    }
  };
  function wc(lang) { return WEB_COPY[lang === 'pl' ? 'pl' : 'en']; }
  function fill(s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  /* ICU-style plural for integers: EN one/other, PL one/few/many. */
  function plural(lang, n, f) {
    var form;
    if (lang === 'pl') {
      var m10 = n % 10, m100 = n % 100;
      form = n === 1 ? f.one : (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) ? f.few : f.many;
    } else form = n === 1 ? f.one : f.other;
    return form.replace('#', String(n));
  }
  function useMedia(query) {
    var get = function () { return !!(window.matchMedia && window.matchMedia(query).matches); };
    var st = useState(get);
    useEffect(function () {
      if (!window.matchMedia) return;
      var mq = window.matchMedia(query);
      function on() { st[1](mq.matches); }
      on();
      if (mq.addEventListener) mq.addEventListener('change', on); else mq.addListener(on);
      return function () { if (mq.removeEventListener) mq.removeEventListener('change', on); else mq.removeListener(on); };
    }, [query]);
    return st[0];
  }

  /* ---------- SideNav ---------- */
  function SideNav(p) {
    var t = wc(p.lang);
    var active = p.active || 'today';
    function item(tb) {
      var on = tb.id === active;
      return h('li', { key: tb.id },
        h('a', {
          href: (p.hrefs && p.hrefs[tb.id]) || '/' + tb.id, className: cx('fm-sidenav-item', on && 'is-active'),
          'aria-current': on ? 'page' : undefined, onClick: p.onNavigate ? function (e) { p.onNavigate(tb.id, e); } : undefined
        },
          h('span', { className: 'fm-sidenav-ico' }, h(Icon, { name: tb.icon, size: 22, weight: on ? 2.1 : 1.75 })),
          h('span', { className: 'fm-sidenav-label' }, t[tb.id])));
    }
    return h('nav', { className: cx('fm-sidenav', p.variant === 'rail' && 'is-rail', p.variant === 'full' && 'is-full', p.className), 'aria-label': t.nav },
      h('span', { className: 'fm-sidenav-name' }, 'Donut'),
      h('button', { type: 'button', className: 'fm-sidenav-add', onClick: p.onAdd },
        h('span', { className: 'fm-sidenav-ico' }, h(Icon, { name: 'plus', size: 22, weight: 2.25 })),
        h('span', { className: 'fm-sidenav-label' }, t.add)),
      h('ul', { className: 'fm-sidenav-list' }, TABS.map(item)),
      h('div', { className: 'fm-sidenav-foot' }, p.avatar || h(Avatar, { label: t.profile })));
  }

  /* ---------- TopBar ---------- */
  function TopBar(p) {
    var t = wc(p.lang);
    var Hn = 'h' + (p.level || 1);
    var back = p.back && h('a', { href: p.back.href || '#', className: 'fm-topbar-back', onClick: p.back.onClick },
      h(Icon, { name: 'chevron-left', size: 20, weight: 2 }),
      h('span', { className: 'fm-vh' }, t.backTo + ' '), h('span', null, p.back.label));
    var actions = (p.actions || p.avatar) && h('div', { className: 'fm-topbar-actions' },
      p.actions, p.avatar && h('span', { className: 'fm-topbar-avatar' }, p.avatar));
    var title = h(Hn, { id: p.titleId, tabIndex: -1, className: p.large ? 'fm-topbar-large' : 'fm-topbar-title' }, p.title);
    return h('header', { className: cx('fm-topbar', p.large && 'is-large', p.sticky && 'is-sticky', p.className) },
      p.large
        ? [back && h('div', { key: 'b', className: 'fm-topbar-row' }, back),
           h('div', { key: 't', className: 'fm-topbar-row' }, title, actions)]
        : h('div', { className: 'fm-topbar-row' }, back, title, actions),
      p.subtitle && h('p', { className: 'fm-topbar-sub' }, p.subtitle));
  }

  /* ---------- Dialog and Sheet ---------- */
  function DialogBase(p, kind) {
    var t = wc(p.lang);
    var ref = useRef(null);
    var opener = useRef(null);
    var titleId = useUid('fm-dlg');
    var descId = titleId + '-d';
    var wide = useMedia('(min-width: 600px)');
    var pres = kind === 'sheet' ? (p.presentation && p.presentation !== 'auto' ? p.presentation : (wide ? 'modal' : 'sheet')) : 'modal';
    var preview = !!p.preview;
    function close(reason) { if (p.onClose) p.onClose(reason); }

    useEffect(function () {
      var d = ref.current;
      if (!d || preview) return;
      if (p.open && !d.open) {
        opener.current = document.activeElement;
        if (d.showModal) d.showModal(); else d.setAttribute('open', '');
        var target = d.querySelector('[data-autofocus]') || d.querySelector('.fm-dlg-title');
        if (target) target.focus();
      } else if (!p.open && d.open) {
        if (d.close) d.close(); else d.removeAttribute('open');
      }
    }, [p.open, preview]);

    useEffect(function () {
      var d = ref.current;
      if (!d || preview) return;
      function onClosed() {
        var o = opener.current;
        opener.current = null;
        if (o && o.focus && document.contains(o)) o.focus();
      }
      d.addEventListener('close', onClosed);
      return function () { d.removeEventListener('close', onClosed); };
    }, [preview]);

    var panel = h('div', { className: 'fm-dlg-panel' },
      h('div', { className: 'fm-dlg-head' },
        h('h2', { id: titleId, className: 'fm-dlg-title', tabIndex: -1 }, p.title),
        p.closeButton !== false && h(IconButton, { icon: 'close', label: t.close, onClick: function () { close('close'); } })),
      p.description && h('p', { id: descId, className: 'fm-dlg-desc' }, p.description),
      p.children && h('div', { className: 'fm-dlg-body' }, p.children),
      p.actions && h('div', { className: 'fm-dlg-actions' }, p.actions));
    var cls = cx('fm-dlg', 'is-' + pres, preview && 'is-preview', p.className);
    var labels = { 'aria-labelledby': titleId, 'aria-describedby': p.description ? descId : undefined };
    if (preview) return h('div', Object.assign({ className: cls, role: 'dialog' }, labels), panel);
    return h('dialog', Object.assign({
      ref: ref, className: cls, 'aria-modal': 'true',
      onCancel: function (e) { if (p.onClose) { e.preventDefault(); close('escape'); } },
      onClick: function (e) { if (e.target === ref.current && p.closeOnBackdrop !== false) close('backdrop'); }
    }, labels), panel);
  }
  function Dialog(p) { return DialogBase(p, 'dialog'); }
  function Sheet(p) { return DialogBase(p, 'sheet'); }

  /* ---------- Toast ---------- */
  function ToastRegion(p) {
    /* Render once per page, empty, so screen readers register the live region before a toast appears. */
    return h('div', { className: cx('fm-toasts', p.className), role: 'status', 'aria-live': 'polite', 'aria-atomic': 'false' },
      h('div', { className: 'fm-toasts-stack' }, p.children));
  }
  function Toast(p) {
    var t = wc(p.lang);
    var dur = p.duration == null ? 10000 : p.duration;
    var timer = useRef(null), left = useRef(dur), since = useRef(0), hover = useRef(false), focus = useRef(false);
    function dismiss(reason) { if (p.onDismiss) p.onDismiss(reason); }
    function stop() {
      if (!timer.current) return;
      clearTimeout(timer.current); timer.current = null;
      left.current = Math.max(0, left.current - (Date.now() - since.current));
    }
    function go() {
      if (!dur || !p.onDismiss || timer.current || hover.current || focus.current) return;
      since.current = Date.now();
      timer.current = setTimeout(function () { timer.current = null; dismiss('timeout'); }, left.current);
    }
    useEffect(function () {
      go();
      function onVis() { if (document.hidden) stop(); else go(); }
      document.addEventListener('visibilitychange', onVis);
      return function () { stop(); document.removeEventListener('visibilitychange', onVis); };
    }, []);
    return h('div', {
      className: cx('fm-toast', p.className),
      onMouseEnter: function () { hover.current = true; stop(); },
      onMouseLeave: function () { hover.current = false; go(); },
      onFocus: function () { focus.current = true; stop(); },
      onBlur: function (e) { if (!e.currentTarget.contains(e.relatedTarget)) { focus.current = false; go(); } },
      onKeyDown: function (e) { if (e.key === 'Escape') dismiss('escape'); }
    },
      p.icon && h(Icon, { name: p.icon, size: 18, weight: 2 }),
      h('span', { className: 'fm-toast-msg' }, p.message),
      p.action && h('button', {
        type: 'button', className: 'fm-toast-action',
        onClick: function () { if (p.action.onClick) p.action.onClick(); dismiss('action'); }
      }, p.action.label),
      p.onDismiss && h('button', { type: 'button', className: 'fm-toast-close', 'aria-label': t.dismiss, onClick: function () { dismiss('close'); } },
        h(Icon, { name: 'close', size: 18, weight: 2 })));
  }

  /* ---------- TextField and Select ---------- */
  function fieldIds(p, prefix, auto) {
    var id = p.id || auto;
    var hintId = id + '-hint', errId = id + '-err';
    return { id: id, hintId: hintId, errId: errId, describedBy: [p.hint && hintId, p.error && errId].filter(Boolean).join(' ') || undefined };
  }
  function fieldShell(p, ids, t, control) {
    return h('div', { className: cx('fm-tf', p.error && 'is-error', p.disabled && 'is-disabled', p.className) },
      h('label', { htmlFor: ids.id, className: 'fm-field-label' }, p.label,
        p.optional && h('span', { className: 'fm-tf-opt' }, ' (' + t.optional + ')')),
      p.hint && h('span', { id: ids.hintId, className: 'fm-field-hint fm-tf-hint' }, p.hint),
      control,
      /* Always rendered so the polite live region exists before an error appears. */
      h('span', { id: ids.errId, className: 'fm-field-hint is-error fm-tf-err', 'aria-live': 'polite' },
        p.error && h(Icon, { name: 'alert', size: 14 }), p.error || null));
  }
  var FIELD_OWN = ['label', 'hint', 'error', 'optional', 'multiline', 'onChange', 'className', 'lang', 'options', 'placeholderOption'];
  function omit(p, keys) { var r = Object.assign({}, p); keys.forEach(function (k) { delete r[k]; }); return r; }

  function TextField(p) {
    var t = wc(p.lang);
    var ids = fieldIds(p, 'fm-tf', useUid('fm-tf'));
    var rest = omit(p, FIELD_OWN);
    var control = h(p.multiline ? 'textarea' : 'input', Object.assign(rest, {
      id: ids.id, className: 'fm-tf-input', type: p.multiline ? undefined : (p.type || 'text'), rows: p.multiline ? (p.rows || 4) : undefined,
      'aria-invalid': p.error ? 'true' : undefined, 'aria-describedby': ids.describedBy,
      onChange: p.onChange ? function (e) { p.onChange(e.target.value, e); } : undefined
    }));
    return fieldShell(p, ids, t, control);
  }

  function Select(p) {
    var t = wc(p.lang);
    var ids = fieldIds(p, 'fm-sel', useUid('fm-sel'));
    var rest = omit(p, FIELD_OWN.concat(['placeholder']));
    if (rest.value == null && rest.defaultValue == null && p.placeholder) rest.defaultValue = '';
    var control = h('span', { className: 'fm-select-box' },
      h('select', Object.assign(rest, {
        id: ids.id, className: 'fm-select',
        'aria-invalid': p.error ? 'true' : undefined, 'aria-describedby': ids.describedBy,
        onChange: p.onChange ? function (e) { p.onChange(e.target.value, e); } : undefined
      }),
        p.placeholder && h('option', { value: '', disabled: true }, p.placeholder),
        (p.options || []).map(function (o) {
          var v = o.value != null ? o.value : o;
          return h('option', { key: String(v), value: v, disabled: o.disabled }, o.label != null ? o.label : o);
        })),
      h(Icon, { name: 'chevron-down', size: 20, className: 'fm-select-chev' }));
    return fieldShell(p, ids, t, control);
  }

  /* ---------- Tooltip ---------- */
  function Tooltip(p) {
    var id = useUid('fm-tip');
    var st = useState(false);
    var shown = p.open != null ? p.open : st[0];
    var delay = useRef(null);
    function show(ms) { clearTimeout(delay.current); delay.current = setTimeout(function () { st[1](true); }, ms); }
    function hide() { clearTimeout(delay.current); st[1](false); }
    useEffect(function () {
      if (!st[0]) return;
      function onKey(e) { if (e.key === 'Escape') hide(); }
      document.addEventListener('keydown', onKey);
      return function () { document.removeEventListener('keydown', onKey); };
    }, [st[0]]);
    useEffect(function () { return function () { clearTimeout(delay.current); }; }, []);
    var child = React.Children.only(p.children);
    var trigger = p.describe ? React.cloneElement(child, { 'aria-describedby': id }) : child;
    return h('span', {
      className: cx('fm-tip-wrap', p.className),
      onMouseEnter: function () { show(p.delay == null ? 400 : p.delay); },
      onMouseLeave: hide,
      onFocus: function (e) { var el = e.target; if (!el.matches || el.matches(':focus-visible')) show(0); },
      onBlur: hide
    },
      trigger,
      h('span', {
        id: id, role: 'tooltip', className: cx('fm-tip', 'is-' + (p.placement || 'bottom'), shown && 'is-open'),
        /* Label mode repeats the trigger's aria-label, so hide it from assistive tech to avoid a double read. */
        'aria-hidden': p.describe ? undefined : 'true'
      }, h('span', { className: 'fm-tip-bubble' }, p.label)));
  }

  /* ---------- WeekTable ---------- */
  function WeekMeal(p) {
    var m = p.meal, t = p.t;
    var locked = m.status === 'eaten' || m.status === 'skipped';
    var nav = { className: 'fm-wk-title', 'data-wk-r': p.r, 'data-wk-c': p.c };
    var title = m.href
      ? h('a', Object.assign({ href: m.href }, nav), m.title)
      : h('button', Object.assign({ type: 'button', onClick: p.onOpen }, nav), m.title);
    var status;
    if (locked) {
      status = h('span', { className: cx('fm-meal-eat', 'is-static', m.status === 'eaten' ? 'is-on' : 'is-skipped') },
        h(Icon, { name: 'lock', size: 15, weight: 2.25, label: t.locked }), m.status === 'eaten' ? t.eaten : t.skipped);
    } else {
      var btn = h('button', {
        type: 'button', className: cx('fm-meal-eat', m.eatHint && 'is-disabled'),
        'aria-label': fill(t.eatA11y, { slot: String(p.slotLabel).toLocaleLowerCase(p.lang === 'pl' ? 'pl' : 'en'), day: p.dayLabel }),
        'aria-disabled': m.eatHint ? 'true' : undefined, onClick: m.eatHint ? undefined : p.onEat
      }, h(Icon, { name: 'check', size: 15, weight: 2.25 }), t.eat);
      status = m.eatHint ? h(Tooltip, { label: m.eatHint, describe: true, placement: 'top' }, btn) : btn;
    }
    return h('div', { className: cx('fm-wk-meal', 'is-' + (m.status || 'planned'), m.batch && 'is-batch', p.joinsNext && 'joins-next') },
      title,
      h(MacroLine, { kcal: m.kcal, protein: m.protein }),
      (m.badges && m.badges.length) ? h('div', { className: 'fm-meal-badges' }, m.badges.map(function (b, i) {
        return h(Badge, { key: i, tone: b.tone, icon: b.icon }, b.label);
      })) : null,
      h('div', { className: 'fm-wk-status' }, status,
        m.queued && h('span', { className: 'fm-wk-queued' }, h(Icon, { name: 'clock', size: 16, label: t.queued }))));
  }

  function WeekTable(p) {
    var t = wc(p.lang);
    var days = p.days || [], slots = p.slots || [], meals = p.meals || {};
    var wide = useMedia('(min-width: 1024px)');
    var layout = p.layout && p.layout !== 'auto' ? p.layout : (wide ? 'table' : 'list');
    var uid = useUid('fm-wk');
    var caption = p.caption || t.wkCaption;
    function at(d, s) { return meals[d.id] && meals[d.id][s.id]; }
    function dayBadges(d) {
      return [d.today && h(Badge, { key: 't', tone: 'basil' }, t.wkToday), d.cook && h(Badge, { key: 'c', tone: 'paprika', icon: 'repeat' }, t.wkCook)];
    }
    function cell(d, di, s, si) {
      var m = at(d, s);
      if (!m) return h('span', { className: 'fm-wk-empty' }, h('span', { 'aria-hidden': 'true' }, '—'), h('span', { className: 'fm-vh' }, t.wkNoMeal));
      var nd = days[di + 1], nm = nd && at(nd, s);
      return h(WeekMeal, {
        meal: m, t: t, lang: p.lang, r: si, c: di, slotLabel: s.label, dayLabel: d.label || d.name,
        joinsNext: layout === 'table' && m.batch && nm && nm.batch === m.batch,
        onEat: function () { if (p.onEat) p.onEat(d.id, s.id); },
        onOpen: function () { if (p.onOpen) p.onOpen(d.id, s.id); }
      });
    }
    /* Arrow keys move between meal titles; Tab still reaches every control. */
    function onKey(e) {
      var el = e.target;
      if (!el || !el.getAttribute || el.getAttribute('data-wk-r') == null) return;
      var root = e.currentTarget;
      var all = Array.prototype.slice.call(root.querySelectorAll('[data-wk-r]'));
      var r = +el.getAttribute('data-wk-r'), c = +el.getAttribute('data-wk-c'), k = e.key, next = null;
      function get(rr, cc) { return root.querySelector('[data-wk-r="' + rr + '"][data-wk-c="' + cc + '"]'); }
      function scan(dr, dc) {
        for (var rr = r + dr, cc = c + dc; rr >= 0 && rr < slots.length && cc >= 0 && cc < days.length; rr += dr, cc += dc) {
          var x = get(rr, cc); if (x) return x;
        }
        return null;
      }
      if ((k === 'Home' || k === 'End') && e.ctrlKey) next = k === 'Home' ? all[0] : all[all.length - 1];
      else if (layout === 'table') {
        if (k === 'ArrowRight') next = scan(0, 1);
        else if (k === 'ArrowLeft') next = scan(0, -1);
        else if (k === 'ArrowDown') next = scan(1, 0);
        else if (k === 'ArrowUp') next = scan(-1, 0);
        else if (k === 'Home') { for (var i = 0; i < days.length && !next; i++) next = get(r, i); }
        else if (k === 'End') { for (var j = days.length - 1; j >= 0 && !next; j--) next = get(r, j); }
      } else {
        var idx = all.indexOf(el);
        if (k === 'ArrowDown') next = all[idx + 1];
        else if (k === 'ArrowUp') next = all[idx - 1];
        else if (k === 'Home') next = all[0];
        else if (k === 'End') next = all[all.length - 1];
      }
      if (next) { e.preventDefault(); next.focus(); }
    }

    if (layout === 'table') {
      return h('div', {
        className: cx('fm-wk', 'is-table', p.className), role: 'region', 'aria-labelledby': uid, tabIndex: 0,
        onKeyDown: onKey, style: { '--wk-cols': days.length }
      },
        h('table', { className: 'fm-wk-table' },
          h('caption', { id: uid, className: p.showCaption ? 'fm-wk-caption' : 'fm-vh' }, caption),
          h('thead', null, h('tr', null,
            h('th', { scope: 'col', className: 'fm-wk-corner' }, h('span', { className: 'fm-vh' }, t.wkMeal)),
            days.map(function (d) {
              return h('th', { key: d.id, scope: 'col', className: cx('fm-wk-dayhead', d.today && 'is-today'), 'aria-current': d.today ? 'date' : undefined },
                h('span', { className: 'fm-wk-dname' }, d.name, ' ', h('span', { className: 'fm-wk-ddate' }, d.date)),
                (d.today || d.cook) && h('span', { className: 'fm-wk-dbadges' }, dayBadges(d)));
            }))),
          h('tbody', null,
            h('tr', { className: 'fm-wk-totals' },
              h('th', { scope: 'row', className: 'fm-wk-slot' }, t.wkTotal),
              days.map(function (d) { return h('td', { key: d.id }, d.totals && h(MacroLine, { kcal: d.totals.kcal, protein: d.totals.protein })); })),
            slots.map(function (s, si) {
              return h('tr', { key: s.id },
                h('th', { scope: 'row', className: 'fm-wk-slot' }, s.label),
                days.map(function (d, di) { return h('td', { key: d.id, className: d.today ? 'is-today' : undefined }, cell(d, di, s, si)); }));
            }))));
    }

    var Hn = 'h' + (p.headingLevel || 2);
    return h('div', { className: cx('fm-wk', 'is-list', p.className), onKeyDown: onKey },
      h('ol', { className: 'fm-wk-days', 'aria-label': caption },
        days.map(function (d, di) {
          var hid = uid + '-d' + di;
          return h('li', { key: d.id, className: cx('fm-wk-day', d.today && 'is-today') },
            h('section', { 'aria-labelledby': hid },
              h('div', { className: 'fm-wk-dayhead' },
                h(Hn, { id: hid, className: 'fm-wk-dname', 'aria-current': d.today ? 'date' : undefined }, d.name, ' ', h('span', { className: 'fm-wk-ddate' }, d.date)),
                dayBadges(d),
                d.totals && h(MacroLine, { kcal: d.totals.kcal, protein: d.totals.protein })),
              h('ol', { className: 'fm-wk-meals' }, slots.map(function (s, si) {
                return h('li', { key: s.id, className: 'fm-wk-row' }, h('span', { className: 'fm-cap' }, s.label), cell(d, di, s, si));
              }))));
        })));
  }

  /* ---------- OfflineBanner ---------- */
  function OfflineBanner(p) {
    var lang = p.lang === 'pl' ? 'pl' : 'en';
    var t = wc(lang);
    var st = p.state || 'offline';
    var n = p.pending || 0;
    var icon = null, text = null, action = null, tone = st;
    if (st === 'offline') { icon = 'wifi-off'; text = t.offline + (n ? ' ' + plural(lang, n, t.pending) : ''); }
    else if (st === 'syncing') { icon = 'repeat'; tone = 'online'; text = plural(lang, n || 1, t.syncing); }
    else if (st === 'synced') { icon = 'check'; tone = 'online'; text = t.synced; }
    else if (st === 'stuck') { icon = 'alert'; text = t.stuck + (n ? ' ' + plural(lang, n, t.pending) : ''); action = h(Button, { variant: 'quiet', size: 'sm', onClick: p.onRetry }, t.retry); }
    /* state 'none' keeps an empty live region mounted so the next change is announced. */
    return h('div', { className: cx('fm-obanner', 'is-' + (st === 'none' ? 'empty' : tone), p.sticky && 'is-sticky', p.className), role: 'status' },
      icon && h(Icon, { name: icon, size: 18, weight: 2 }),
      text && h('p', { className: 'fm-obanner-text' }, text),
      action);
  }

  /* ---------- InstallPrompt ---------- */
  function InstallPrompt(p) {
    var t = wc(p.lang);
    var titleId = useUid('fm-install');
    var platform = p.platform || 'prompt';
    if (platform === 'none') return null;
    return h('section', { className: cx('fm-install', p.className), 'aria-labelledby': titleId },
      h('span', { className: 'fm-install-icon' }, h(Icon, { name: 'download', size: 18, weight: 2 })),
      h('div', { className: 'fm-install-text' },
        h('p', { id: titleId, className: 'fm-install-title' }, t.installTitle),
        h('p', { className: 'fm-install-body' }, t.installBody),
        platform === 'ios' && h('p', { className: 'fm-install-body fm-install-steps' }, t.installIos),
        h('div', { className: 'fm-install-actions' },
          platform === 'prompt' && h(Button, { variant: 'secondary', size: 'sm', icon: 'download', onClick: p.onInstall }, t.installCta),
          h(Button, { variant: 'quiet', size: 'sm', onClick: p.onDismiss }, t.notNow))));
  }

  /* ---------- ProfileFileCard ---------- */
  function ProfileFileCard(p) {
    var t = wc(p.lang);
    var input = useRef(null);
    var titleId = useUid('fm-pfile');
    var warnId = titleId + '-w';
    var mode = p.mode || 'both';
    var canDown = mode !== 'load', canLoad = mode !== 'download';
    return h('section', { className: cx('fm-pfile', p.className), 'aria-labelledby': titleId },
      h('div', { className: 'fm-pfile-head' },
        h('span', { className: 'fm-pfile-icon' }, h(Icon, { name: 'user', size: 22 })),
        h('div', null,
          h('p', { id: titleId, className: 'fm-pfile-title' }, p.title || t.pfTitle),
          canDown && h('p', { className: 'fm-pfile-meta' }, p.lastDownloaded ? fill(t.pfLast, { date: p.lastDownloaded }) : t.pfNever))),
      h('p', { className: 'fm-pfile-body' }, t.pfWhere),
      h('p', { className: 'fm-pfile-body' }, t.pfLoss),
      p.persistRefused && h('p', { className: 'fm-pfile-meta' }, t.pfPersist),
      h('div', { className: 'fm-pfile-actions' },
        canDown && h(Button, { variant: 'secondary', icon: 'download', onClick: p.onDownload, 'aria-describedby': warnId }, t.pfDownload),
        canLoad && h(Button, { variant: 'quiet', icon: 'upload', onClick: function () { if (input.current) input.current.click(); } }, t.pfLoad),
        canLoad && h('input', {
          ref: input, type: 'file', accept: '.json,application/json', className: 'fm-vh', tabIndex: -1, 'aria-hidden': 'true',
          onChange: function (e) { var f = e.target.files && e.target.files[0]; if (f && p.onLoad) p.onLoad(f); e.target.value = ''; }
        })),
      canDown && h('p', { id: warnId, className: 'fm-pfile-warn' }, h(Icon, { name: 'lock', size: 14, weight: 2 }), t.pfWarn),
      p.error && h('p', { className: 'fm-pfile-error', role: 'alert' }, h(Icon, { name: 'alert', size: 14, weight: 2 }), p.error === true ? t.pfInvalid : p.error));
  }

  /* ---------- AppShell ---------- */
  function AppShell(p) {
    var t = wc(p.lang);
    var mainId = p.mainId || 'main';
    var nav = p.nav !== false;
    return h('div', { className: cx('fm-shell', p.contained && 'is-contained', p.accessory && 'has-acc', !nav && 'no-nav', p.className), style: p.style },
      h('a', { href: '#' + mainId, className: 'fm-skip' }, t.skip),
      h('div', { className: 'fm-shell-frame' },
        nav && h('div', { className: 'fm-shell-side' },
          h(SideNav, { active: p.active, lang: p.lang, hrefs: p.hrefs, onNavigate: p.onNavigate, onAdd: p.onAdd, avatar: p.avatar })),
        h('main', { id: mainId, className: 'fm-shell-main', tabIndex: -1 },
          h('div', { className: cx('fm-shell-content', p.aside && 'has-aside', p.narrow && 'is-narrow') },
            (p.banner || p.header || p.notices) && h('div', { className: 'fm-shell-top' }, p.banner, p.header, p.notices),
            p.aside && h('aside', { className: 'fm-shell-aside', 'aria-label': p.asideLabel }, p.aside),
            h('div', { className: 'fm-shell-primary' }, p.children)),
          h(ToastRegion, { className: 'fm-shell-toasts' }, p.toasts)),
        nav && h('div', { className: 'fm-shell-bottom' },
          h(TabBar, { active: p.active, lang: p.lang, links: true, hrefs: p.hrefs, onNavigate: p.onNavigate, onAdd: p.onAdd, accessory: p.accessory }))));
  }

  var C = window;
  C.Donut = C.Donut || {};
  Object.assign(C.Donut, {
    Icon: Icon, Button: Button, IconButton: IconButton, Chip: Chip, SegmentedControl: SegmentedControl,
    SelectCard: SelectCard, Toggle: Toggle, Checkbox: Checkbox, NumberField: NumberField, ExclusionRow: ExclusionRow,
    DistributionEditor: DistributionEditor, MacroRing: MacroRing, MacroBar: MacroBar, MacroLine: MacroLine, Delta: Delta,
    Badge: Badge, Notice: Notice, MealCard: MealCard, DayStrip: DayStrip, RebalanceProposal: RebalanceProposal, IngredientRow: IngredientRow,
    SwapOption: SwapOption, ChangeItem: ChangeItem, CompareCard: CompareCard, ConfidencePrompt: ConfidencePrompt,
    ShoppingItem: ShoppingItem, StatTile: StatTile, PlanCard: PlanCard, LockedPreview: LockedPreview,
    SectionHeader: SectionHeader, NavBar: NavBar, Avatar: Avatar, OnboardingProgress: OnboardingProgress, TabBar: TabBar,
    BottomAccessory: BottomAccessory, RecipeHero: RecipeHero, PhoneFrame: PhoneFrame,
    AppShell: AppShell, SideNav: SideNav, TopBar: TopBar, Dialog: Dialog, Sheet: Sheet, Toast: Toast, ToastRegion: ToastRegion,
    TextField: TextField, Select: Select, WeekTable: WeekTable, OfflineBanner: OfflineBanner, InstallPrompt: InstallPrompt,
    ProfileFileCard: ProfileFileCard, Tooltip: Tooltip
  });
})();
