<script>
  // A result card: a grid preview plus its key stats.
  import GridView from './GridView.svelte'

  let { grid, rank } = $props()
</script>

<div class="card">
  <div class="rank">#{rank}</div>
  <div class="preview">
    <GridView {grid} size={24} />
  </div>
  <div class="stats">
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
  .preview {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    overflow: auto;
    min-height: 120px;
  }
  .stats {
    display: flex;
    gap: 14px;
    font-size: 13px;
    color: var(--muted);
  }
  .stats span {
    white-space: nowrap;
  }
</style>
