/* @ds-bundle: {"format":4,"namespace":"FitMeal","components":[{"name":"Icon"},{"name":"Button"},{"name":"IconButton"},{"name":"Chip"},{"name":"SegmentedControl"},{"name":"SelectCard"},{"name":"Toggle"},{"name":"Checkbox"},{"name":"NumberField"},{"name":"ExclusionRow"},{"name":"DistributionEditor"},{"name":"MacroRing"},{"name":"MacroBar"},{"name":"MacroLine"},{"name":"Delta"},{"name":"Badge"},{"name":"Notice"},{"name":"MealCard"},{"name":"DayStrip"},{"name":"RebalanceProposal"},{"name":"IngredientRow"},{"name":"SwapOption"},{"name":"ChangeItem"},{"name":"CompareCard"},{"name":"ConfidencePrompt"},{"name":"ShoppingItem"},{"name":"StatTile"},{"name":"PlanCard"},{"name":"LockedPreview"},{"name":"SectionHeader"},{"name":"NavBar"},{"name":"Avatar"},{"name":"OnboardingProgress"},{"name":"TabBar"},{"name":"BottomAccessory"},{"name":"RecipeHero"},{"name":"PhoneFrame"}]} */
(function () {
  var React = window.React;
  var h = React.createElement;
  var useState = React.useState;

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
    shield: 'M12 3l7 3v5c0 4.6-3 8.3-7 10-4-1.7-7-5.4-7-10V6z'
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
      'aria-label': p.label, onClick: p.onClick, disabled: p.disabled
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
    return h('label', { className: cx('fm-field', p.large && 'fm-field-lg', p.error && 'is-error', p.className) },
      p.label && h('span', { className: 'fm-field-label' }, p.label),
      h('span', { className: 'fm-field-box' },
        h('input', {
          className: 'fm-field-input', inputMode: 'numeric', defaultValue: p.value, placeholder: p.placeholder,
          'aria-invalid': p.error ? 'true' : undefined
        }),
        p.unit && h('span', { className: 'fm-field-unit' }, p.unit)),
      (p.error || p.hint) && h('span', { className: cx('fm-field-hint', p.error && 'is-error') },
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
        h('span', { className: 'fm-change-effect' }, kept ? p.effect : 'Rejected. FitMeal re-solves without it.')),
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
      p.sourceKcal != null && h('p', { className: 'fm-cmp-target' }, 'FitMeal calculates every number itself. The source\u2019s figure is shown for comparison only.'));
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
    var tabs = min ? TABS.filter(function (t) { return t.id === active; }) : TABS;
    var bar = h('nav', { className: cx('fm-glass', 'fm-tabbar', min && 'is-min'), 'aria-label': 'Main' },
      tabs.map(function (t) {
        var on = t.id === active;
        return h('button', { key: t.id, type: 'button', className: cx('fm-tab', on && 'is-active'), 'aria-current': on ? 'page' : undefined, 'aria-label': t.label },
          h(Icon, { name: t.icon, size: min ? 24 : 23, weight: on ? 2.1 : 1.7 }), !min && h('span', null, t.label));
      }));
    var add = h('button', { type: 'button', className: 'fm-glass fm-glass-accent fm-tab-add', 'aria-label': 'Add recipe' },
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

  var C = window;
  C.FitMeal = C.FitMeal || {};
  Object.assign(C.FitMeal, {
    Icon: Icon, Button: Button, IconButton: IconButton, Chip: Chip, SegmentedControl: SegmentedControl,
    SelectCard: SelectCard, Toggle: Toggle, Checkbox: Checkbox, NumberField: NumberField, ExclusionRow: ExclusionRow,
    DistributionEditor: DistributionEditor, MacroRing: MacroRing, MacroBar: MacroBar, MacroLine: MacroLine, Delta: Delta,
    Badge: Badge, Notice: Notice, MealCard: MealCard, DayStrip: DayStrip, RebalanceProposal: RebalanceProposal, IngredientRow: IngredientRow,
    SwapOption: SwapOption, ChangeItem: ChangeItem, CompareCard: CompareCard, ConfidencePrompt: ConfidencePrompt,
    ShoppingItem: ShoppingItem, StatTile: StatTile, PlanCard: PlanCard, LockedPreview: LockedPreview,
    SectionHeader: SectionHeader, NavBar: NavBar, Avatar: Avatar, OnboardingProgress: OnboardingProgress, TabBar: TabBar,
    BottomAccessory: BottomAccessory, RecipeHero: RecipeHero, PhoneFrame: PhoneFrame
  });
})();
