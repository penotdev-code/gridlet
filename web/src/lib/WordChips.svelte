<script>
  // Tag-style input: words show as removable chips inside the box; a single
  // inline field adds words (Enter / comma) or imports a whole pasted list.
  // Each chip carries its own orientation, cycled by clicking its glyph.
  let { words, onadd, onremove, oncycle } = $props()

  let draft = $state('')
  let inputEl

  const ORIENT = {
    both: { icon: '✛', label: 'Les deux sens' },
    horizontal: { icon: '→', label: 'Horizontal' },
    vertical: { icon: '↓', label: 'Vertical' },
  }

  // Split a blob into tokens: line / comma / semicolon / whitespace separated,
  // with surrounding quotes stripped.
  function parseList(text) {
    return text
      .split(/[\s,;]+/)
      .map((t) => t.replace(/^["'«»]+|["'«»]+$/g, '').trim())
      .filter(Boolean)
  }

  function commitDraft() {
    const list = parseList(draft)
    if (list.length) onadd(list)
    draft = ''
  }

  function onKeydown(e) {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault()
      commitDraft()
    } else if (e.key === 'Backspace' && draft === '' && words.length) {
      onremove(words[words.length - 1].id)
    }
  }

  function onPaste(e) {
    const text = e.clipboardData?.getData('text') ?? ''
    const list = parseList(text)
    if (list.length > 1) {
      e.preventDefault()
      onadd(list)
      draft = ''
    }
  }

  function onBlur() {
    if (draft.trim()) commitDraft()
  }
</script>

<div
  class="chips"
  role="group"
  aria-label="Liste de mots"
  onclick={() => inputEl?.focus()}
  onkeydown={() => {}}
>
  {#each words as w (w.id)}
    <span class="chip">
      <button
        class="orient"
        title={ORIENT[w.orientation].label + ' — cliquez pour changer'}
        aria-label={'Orientation : ' + ORIENT[w.orientation].label}
        onclick={(e) => {
          e.stopPropagation()
          oncycle(w.id)
        }}
      >
        {ORIENT[w.orientation].icon}
      </button>
      <span class="label">{w.text}</span>
      <button
        class="x"
        title="Supprimer"
        aria-label={'Supprimer ' + w.text}
        onclick={(e) => {
          e.stopPropagation()
          onremove(w.id)
        }}
      >
        ×
      </button>
    </span>
  {/each}

  <input
    bind:this={inputEl}
    class="field"
    type="text"
    placeholder={words.length ? 'Ajouter…' : 'Tapez un mot puis Entrée, ou collez une liste…'}
    bind:value={draft}
    onkeydown={onKeydown}
    onpaste={onPaste}
    onblur={onBlur}
  />
</div>

<style>
  .chips {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 7px;
    min-height: 96px;
    align-content: flex-start;
    padding: 10px;
    border: 1px solid var(--line);
    border-radius: 11px;
    background: var(--surface);
    cursor: text;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .chips:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-soft);
  }

  .chip {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    height: 30px;
    padding: 0 4px 0 2px;
    background: var(--tile);
    border: 1px solid var(--line);
    border-radius: 8px;
    font-size: 14px;
  }
  .chip .label {
    padding: 0 2px;
    white-space: nowrap;
  }
  .chip .orient {
    width: 24px;
    height: 24px;
    border: none;
    border-radius: 6px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 13px;
    line-height: 1;
    cursor: pointer;
    transition: filter 0.12s;
  }
  .chip .orient:hover {
    filter: brightness(0.96);
  }
  .chip .x {
    width: 20px;
    height: 24px;
    border: none;
    background: transparent;
    color: var(--muted);
    font-size: 17px;
    line-height: 1;
    cursor: pointer;
    border-radius: 6px;
  }
  .chip .x:hover {
    background: var(--accent-soft);
    color: var(--accent);
  }

  .field {
    flex: 1;
    min-width: 110px;
    height: 30px;
    border: none;
    outline: none;
    background: transparent;
    color: var(--ink);
    font: inherit;
  }
</style>
