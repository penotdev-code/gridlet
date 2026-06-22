<script>
  import { generateGrid } from './engine/index.js'
  import { annotate, SORTERS, SORT_OPTIONS } from './lib/metrics.js'
  import WordRow from './lib/WordRow.svelte'
  import GridCard from './lib/GridCard.svelte'

  let nextId = 0
  const makeWord = (text = '') => ({ id: nextId++, text })

  let words = $state([makeWord('Paul'), makeWord('Camille'), makeWord('Arthur')])
  let directions = $state('both')
  let gap = $state(1)

  let sortKey = $state('esthetique')
  let page = $state(0)
  const PAGE_SIZE = 6

  let grids = $state([]) // annotated
  let stats = $state(null) // { count, timeMs, truncated, pivots }
  let busy = $state(false)
  let error = $state('')
  let focusId = $state(null)

  const directionOptions = [
    { value: 'both', label: 'Les deux', icon: '✛' },
    { value: 'horizontal', label: 'Horizontal', icon: '→' },
    { value: 'vertical', label: 'Vertical', icon: '↓' },
  ]

  const validWords = $derived(words.filter((w) => w.text.trim().length > 0))

  const sorted = $derived([...grids].sort(SORTERS[sortKey]))
  const pageCount = $derived(Math.max(1, Math.ceil(sorted.length / PAGE_SIZE)))
  const pageGrids = $derived(sorted.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE))

  function addWord() {
    const w = makeWord()
    words = [...words, w]
    focusId = w.id
  }
  function updateWord(id, text) {
    words = words.map((w) => (w.id === id ? { ...w, text } : w))
  }
  function removeWord(id) {
    words = words.filter((w) => w.id !== id)
  }

  async function generate() {
    if (validWords.length === 0) {
      error = 'Ajoutez au moins un mot.'
      grids = []
      stats = null
      return
    }
    busy = true
    error = ''
    // Let the button repaint to "Calcul…" before the synchronous WASM call.
    await new Promise((r) => setTimeout(r, 0))
    const t0 = performance.now()
    try {
      const out = await generateGrid({
        words: validWords.map((w) => w.text.trim()),
        directions,
        gap,
      })
      const timeMs = performance.now() - t0
      grids = annotate(out.grids)
      stats = {
        count: out.count,
        timeMs,
        truncated: out.truncated,
        pivots: out.pivots_tested,
      }
      page = 0
    } catch (e) {
      error = String(e)
      grids = []
      stats = null
    } finally {
      busy = false
    }
  }

  const allNoCrossing = $derived(grids.length > 0 && grids.every((g) => g.crossings === 0))
</script>

<div class="app">
  <header>
    <h1>Gridlet</h1>
    <p>Générez et comparez des grilles de mots croisés à partir de votre liste.</p>
  </header>

  <main>
    <aside class="panel controls">
      <div class="block">
        <div class="block-head">
          <h2>Vos mots</h2>
          <span class="count">{validWords.length}</span>
        </div>
        <div class="words">
          {#each words as word (word.id)}
            <WordRow
              {word}
              autofocus={focusId === word.id}
              oninput={(t) => updateWord(word.id, t)}
              onremove={() => removeWord(word.id)}
              onenter={addWord}
            />
          {/each}
        </div>
        <button class="add" onclick={addWord}>+ Ajouter un mot</button>
      </div>

      <div class="block">
        <h2>Sens autorisés</h2>
        <div class="segment" role="group" aria-label="Sens autorisés">
          {#each directionOptions as opt}
            <button
              type="button"
              class:active={directions === opt.value}
              aria-pressed={directions === opt.value}
              onclick={() => (directions = opt.value)}
            >
              <span class="ico">{opt.icon}</span>{opt.label}
            </button>
          {/each}
        </div>
      </div>

      <div class="block">
        <div class="block-head">
          <h2>Écart minimum</h2>
          <span class="count">{gap}</span>
        </div>
        <input type="range" min="0" max="5" step="1" bind:value={gap} />
        <p class="hint">Cases vides minimum entre deux mots parallèles.</p>
      </div>

      <button class="primary" onclick={generate} disabled={busy}>
        {busy ? 'Calcul…' : 'Générer les grilles'}
      </button>
      {#if error}<p class="error">{error}</p>{/if}
    </aside>

    <section class="results">
      {#if stats}
        <div class="toolbar">
          <div class="stats">
            <strong>{stats.count}</strong> grille{stats.count > 1 ? 's' : ''}
            <span class="dot">·</span>
            {stats.timeMs.toFixed(0)} ms
            <span class="dot">·</span>
            {stats.pivots} pivot{stats.pivots > 1 ? 's' : ''}
            {#if stats.truncated}<span class="trunc">(limité à {grids.length})</span>{/if}
          </div>
          <label class="sort">
            Trier&nbsp;:
            <select bind:value={sortKey}>
              {#each SORT_OPTIONS as o}
                <option value={o.value}>{o.label} — {o.hint}</option>
              {/each}
            </select>
          </label>
        </div>
      {/if}

      {#if allNoCrossing}
        <p class="warn">
          Aucun croisement possible avec ces contraintes — autorisez « Les deux »
          sens, ou ajoutez des mots qui partagent des lettres.
        </p>
      {/if}

      {#if pageGrids.length > 0}
        <div class="cards">
          {#each pageGrids as grid, i (grid.cells.map((c) => c.row + ',' + c.col + c.ch).join('|'))}
            <GridCard {grid} rank={page * PAGE_SIZE + i + 1} />
          {/each}
        </div>

        {#if pageCount > 1}
          <div class="pager">
            <button onclick={() => (page = Math.max(0, page - 1))} disabled={page === 0}>
              ← Précédent
            </button>
            <span>Page {page + 1} / {pageCount}</span>
            <button
              onclick={() => (page = Math.min(pageCount - 1, page + 1))}
              disabled={page >= pageCount - 1}
            >
              Suivant →
            </button>
          </div>
        {/if}
      {:else if !stats}
        <div class="placeholder">
          <p>Vos grilles apparaîtront ici.</p>
          <span>Saisissez des mots puis cliquez sur « Générer les grilles ».</span>
        </div>
      {/if}
    </section>
  </main>
</div>

<style>
  .app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 24px 64px;
  }
  header h1 {
    margin: 0;
    font-size: 32px;
  }
  header p {
    margin: 6px 0 0;
    color: var(--muted);
  }

  main {
    display: grid;
    grid-template-columns: 340px 1fr;
    gap: 24px;
    margin-top: 28px;
    align-items: start;
  }

  .panel {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 22px;
    box-shadow: var(--shadow);
    position: sticky;
    top: 24px;
  }
  .block + .block {
    margin-top: 22px;
  }
  .block h2,
  .block-head h2 {
    margin: 0 0 12px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--muted);
  }
  .block-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .block-head h2 {
    margin-bottom: 0;
  }
  .block-head {
    margin-bottom: 12px;
  }
  .count {
    min-width: 24px;
    height: 24px;
    padding: 0 7px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    background: var(--accent-soft);
    color: var(--accent);
    font-size: 13px;
    font-weight: 700;
  }

  .words {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .add {
    margin-top: 12px;
    width: 100%;
    padding: 9px;
    border: 1px dashed var(--line);
    border-radius: 9px;
    background: transparent;
    color: var(--muted);
    transition: border-color 0.15s, color 0.15s, background 0.15s;
  }
  .add:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--tile);
  }

  .segment {
    display: flex;
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
  }
  .segment button {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 9px 4px;
    border: none;
    background: var(--surface);
    color: var(--muted);
    font-size: 13px;
    transition: background 0.12s, color 0.12s;
  }
  .segment button + button {
    border-left: 1px solid var(--line);
  }
  .segment button:hover {
    background: var(--tile);
  }
  .segment button.active {
    background: var(--accent);
    color: #fff;
  }
  .ico {
    font-size: 14px;
  }

  input[type='range'] {
    width: 100%;
    accent-color: var(--accent);
  }
  .hint {
    margin: 10px 0 0;
    font-size: 13px;
    line-height: 1.5;
    color: var(--muted);
  }

  .primary {
    margin-top: 24px;
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 10px;
    background: var(--accent);
    color: #fff;
    font-weight: 650;
    transition: filter 0.15s, transform 0.05s;
  }
  .primary:hover:not(:disabled) {
    filter: brightness(1.05);
  }
  .primary:active:not(:disabled) {
    transform: translateY(1px);
  }
  .primary:disabled {
    opacity: 0.6;
    cursor: default;
  }
  .error {
    margin: 12px 0 0;
    color: #b5453a;
    font-size: 14px;
  }

  .results {
    min-height: 360px;
  }
  .toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 18px;
  }
  .stats {
    color: var(--muted);
    font-size: 14px;
  }
  .stats strong {
    color: var(--ink);
  }
  .dot {
    margin: 0 6px;
    opacity: 0.5;
  }
  .trunc {
    margin-left: 6px;
    color: var(--accent);
  }
  .sort {
    font-size: 14px;
    color: var(--muted);
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .sort select {
    font: inherit;
    padding: 7px 10px;
    border: 1px solid var(--line);
    border-radius: 9px;
    background: var(--surface);
    color: var(--ink);
    cursor: pointer;
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 18px;
  }

  .pager {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-top: 24px;
    color: var(--muted);
    font-size: 14px;
  }
  .pager button {
    padding: 8px 14px;
    border: 1px solid var(--line);
    border-radius: 9px;
    background: var(--surface);
    color: var(--ink);
    transition: background 0.12s;
  }
  .pager button:hover:not(:disabled) {
    background: var(--tile);
  }
  .pager button:disabled {
    opacity: 0.5;
    cursor: default;
  }

  .placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    min-height: 320px;
    color: var(--muted);
    text-align: center;
  }
  .placeholder p {
    margin: 0;
    font-size: 17px;
    font-weight: 600;
  }
  .placeholder span {
    font-size: 14px;
  }

  .warn {
    margin: 0 0 18px;
    font-size: 14px;
    color: #9a6b2f;
    background: #fbf1de;
    border: 1px solid #f0dcae;
    padding: 12px 14px;
    border-radius: 10px;
  }

  @media (max-width: 860px) {
    main {
      grid-template-columns: 1fr;
    }
    .panel {
      position: static;
    }
  }
</style>
