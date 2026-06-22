<script>
  // A single editable word: text input (Enter adds a new word) + remove button.
  let { word, oninput, onremove, onenter, autofocus = false } = $props()

  let el
  $effect(() => {
    if (autofocus && el) el.focus()
  })
</script>

<div class="row">
  <input
    bind:this={el}
    class="text"
    type="text"
    placeholder="Un mot…"
    value={word.text}
    oninput={(e) => oninput(e.target.value)}
    onkeydown={(e) => {
      if (e.key === 'Enter') {
        e.preventDefault()
        onenter()
      }
    }}
  />
  <button class="remove" title="Supprimer" aria-label="Supprimer" onclick={onremove}>
    ×
  </button>
</div>

<style>
  .row {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .text {
    flex: 1;
    min-width: 0;
    padding: 9px 12px;
    border: 1px solid var(--line);
    border-radius: 9px;
    background: var(--surface);
    color: var(--ink);
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .text:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-soft);
  }
  .remove {
    width: 36px;
    height: 38px;
    border: 1px solid var(--line);
    border-radius: 9px;
    background: var(--surface);
    color: var(--muted);
    font-size: 20px;
    line-height: 1;
    transition: background 0.12s, color 0.12s, border-color 0.12s;
  }
  .remove:hover {
    background: var(--accent-soft);
    color: var(--accent);
    border-color: var(--accent-soft);
  }
</style>
