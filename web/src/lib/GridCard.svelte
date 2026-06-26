<script>
  // A result card: a grid preview plus its key stats.
  import GridView from './GridView.svelte'

  let { grid, rank, onfavorite, saved = false } = $props()
</script>

<div class="card">
  <div class="rank">#{rank}</div>
  {#if onfavorite}
    <button
      class="fav"
      class:saved
      title={saved ? 'Enregistré dans vos favoris' : 'Mettre en favori'}
      aria-label="Mettre en favori"
      disabled={saved}
      onclick={() => onfavorite(grid)}
    >
      {saved ? '♥' : '♡'}
    </button>
  {/if}
  <div class="preview">
    <GridView {grid} max={24} />
  </div>
  <div class="stats">
    <span title="Mots placés">{grid.words} mots</span>
    <span title="Dimensions">{grid.cols}×{grid.rows}</span>
    <span title="Croisements">⛓ {grid.crossings}</span>
    <span title="Densité de remplissage">{Math.round(grid.m.fill * 100)}%</span>
  </div>
</div>

<style>
  .card {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
    padding: 18px 16px 14px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: var(--shadow);
    transition: transform 0.12s, box-shadow 0.12s;
  }
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(44, 42, 38, 0.08), 0 12px 28px rgba(44, 42, 38, 0.1);
  }
  .rank {
    position: absolute;
    top: 10px;
    left: 12px;
    font-size: 12px;
    font-weight: 700;
    color: var(--muted);
  }
  .fav {
    position: absolute;
    top: 6px;
    right: 8px;
    border: none;
    background: transparent;
    color: var(--accent);
    font-size: 18px;
    line-height: 1;
    cursor: pointer;
    padding: 2px 4px;
    border-radius: 6px;
    transition: background 0.12s, transform 0.05s;
  }
  .fav:hover:not(:disabled) {
    background: var(--accent-soft);
  }
  .fav:active:not(:disabled) {
    transform: scale(0.92);
  }
  .fav.saved {
    cursor: default;
  }
  .preview {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 120px;
  }
  .stats {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6px 12px;
    font-size: 12.5px;
    color: var(--muted);
  }
  .stats span {
    white-space: nowrap;
  }
</style>
