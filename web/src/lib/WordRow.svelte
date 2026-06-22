<script>
  // A single word: text input (Enter adds a new word), per-word orientation, remove.
  let { word, oninput, onorient, onremove, onenter, autofocus = false } = $props()

  let el
  $effect(() => {
    if (autofocus && el) el.focus()
  })

  const options = [
    { value: 'both', label: 'Les deux', icon: '✛' },
    { value: 'horizontal', label: 'Horizontal', icon: '→' },
    { value: 'vertical', label: 'Vertical', icon: '↓' },
  ]
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

  <div class="orient" role="group" aria-label="Orientation">
    {#each options as opt}
      <button
        type="button"
        class:active={word.orientation === opt.value}
        title={opt.label}
        aria-pressed={word.orientation === opt.value}
        onclick={() => onorient(opt.value)}
      >
        {opt.icon}
      </button>
    {/each}
  </div>

  <button class="remove" title="Supprimer" aria-label="Supprimer" onclick={onremove}>×</button>
</div>

<style>
  .row {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .text {
    flex: 1;
    min-width: 0;
    padding: 9px 11px;
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
  .orient {
    display: inline-flex;
    border: 1px solid var(--line);
    border-radius: 9px;
    overflow: hidden;
    background: var(--surface);
    flex: none;
  }
  .orient button {
    width: 28px;
    height: 38px;
    border: none;
    background: transparent;
    color: var(--muted);
    font-size: 14px;
    transition: background 0.12s, color 0.12s;
  }
  .orient button + button {
    border-left: 1px solid var(--line);
  }
  .orient button:hover {
    background: var(--tile);
  }
  .orient button.active {
    background: var(--accent);
    color: #fff;
  }
  .remove {
    flex: none;
    width: 30px;
    height: 38px;
    border: 1px solid var(--line);
    border-radius: 9px;
    background: var(--surface);
    color: var(--muted);
    font-size: 18px;
    line-height: 1;
    transition: background 0.12s, color 0.12s, border-color 0.12s;
  }
  .remove:hover {
    background: var(--accent-soft);
    color: var(--accent);
    border-color: var(--accent-soft);
  }
</style>
