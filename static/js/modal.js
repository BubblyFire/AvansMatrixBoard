/**
 * Lightweight modal dialogs to replace browser prompt() / confirm().
 */

function buildOverlay() {
  const overlay = document.createElement('div');
  overlay.style.cssText = [
    'position:fixed', 'inset:0', 'z-index:10000',
    'background:rgba(15,23,42,0.55)',
    'display:flex', 'align-items:center', 'justify-content:center',
    'padding:1rem',
  ].join(';');
  return overlay;
}

function buildBox() {
  const box = document.createElement('div');
  box.style.cssText = [
    'background:#fff', 'border-radius:12px', 'padding:1.5rem',
    'width:100%', 'max-width:360px',
    'box-shadow:0 20px 60px rgba(0,0,0,0.25)',
  ].join(';');
  box.addEventListener('click', e => e.stopPropagation());
  return box;
}

function makeButton(label, variant) {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.textContent = label;
  btn.className = `btn btn-sm ${variant}`;
  return btn;
}

function makeHeading(text) {
  const h = document.createElement('h6');
  h.textContent = text;
  h.style.cssText = 'font-weight:600;margin:0 0 1rem;font-size:1rem;';
  return h;
}

function makeFooter() {
  const f = document.createElement('div');
  f.style.cssText = 'display:flex;gap:8px;justify-content:flex-end;margin-top:1rem;';
  return f;
}

/**
 * Show a modal with a text input.
 * @returns {Promise<string|null>} Trimmed input value, or null if cancelled.
 */
export function showInputModal({ title, placeholder = '', defaultValue = '', confirmLabel = 'OK' }) {
  return new Promise(resolve => {
    const overlay = buildOverlay();
    const box     = buildBox();

    const input = document.createElement('input');
    input.type        = 'text';
    input.value       = defaultValue;
    input.placeholder = placeholder;
    input.className   = 'form-control';
    input.style.cssText = 'border-radius:8px;';

    const footer  = makeFooter();
    const cancel  = makeButton('Cancel', 'btn-outline-secondary');
    const confirm = makeButton(confirmLabel, 'btn-primary');
    footer.append(cancel, confirm);

    box.append(makeHeading(title), input, footer);
    overlay.appendChild(box);
    document.body.appendChild(overlay);

    setTimeout(() => {
      input.focus();
      input.select();
    }, 30);

    const done = (value) => { overlay.remove(); resolve(value); };

    cancel.onclick       = () => done(null);
    confirm.onclick      = () => done(input.value.trim() || null);
    overlay.onclick      = () => done(null);
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter')  done(input.value.trim() || null);
      if (e.key === 'Escape') done(null);
    });
  });
}

/**
 * Show a confirmation modal.
 * @returns {Promise<boolean>}
 */
export function showConfirmModal({ title, body = '', confirmLabel = 'Confirm', danger = false }) {
  return new Promise(resolve => {
    const overlay = buildOverlay();
    const box     = buildBox();

    const footer  = makeFooter();
    const cancel  = makeButton('Cancel', 'btn-outline-secondary');
    const confirm = makeButton(confirmLabel, danger ? 'btn-danger' : 'btn-primary');
    footer.append(cancel, confirm);

    box.append(makeHeading(title));

    if (body) {
      const p = document.createElement('p');
      p.textContent = body;
      p.style.cssText = 'color:#64748b;font-size:0.875rem;margin:0;word-break:break-all;';
      box.appendChild(p);
    }

    box.appendChild(footer);
    overlay.appendChild(box);
    document.body.appendChild(overlay);

    setTimeout(() => confirm.focus(), 30);

    const done = (value) => { overlay.remove(); resolve(value); };

    cancel.onclick  = () => done(false);
    confirm.onclick = () => done(true);
    overlay.onclick = () => done(false);
    document.addEventListener('keydown', function handler(e) {
      if (e.key === 'Escape') { done(false); document.removeEventListener('keydown', handler); }
      if (e.key === 'Enter')  { done(true);  document.removeEventListener('keydown', handler); }
    });
  });
}
