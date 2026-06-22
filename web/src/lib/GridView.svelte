<script>
  // Compact renderer for a single grid. `size` is the cell side in px.
  let { grid, size = 26 } = $props()

  const cellMap = $derived(
    new Map((grid?.cells ?? []).map((c) => [`${c.row},${c.col}`, c]))
  )
</script>

<div class="grid" style="--cols: {grid.cols}; --cell: {size}px;">
  {#each Array(grid.rows) as _, r}
    {#each Array(grid.cols) as _, c}
      {@const cell = cellMap.get(`${r},${c}`)}
      {#if cell}
        <div class="tile" class:cross={cell.crossing}>{cell.ch}</div>
      {:else}
        <div class="empty"></div>
      {/if}
    {/each}
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(var(--cols), var(--cell));
    gap: 3px;
    justify-content: center;
  }
  .tile,
  .empty {
    width: var(--cell);
    height: var(--cell);
    border-radius: 6px;
  }
  .tile {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 650;
    font-size: calc(var(--cell) * 0.46);
    text-transform: uppercase;
    color: var(--ink);
    background: var(--tile);
    border: 1px solid var(--line);
  }
  .tile.cross {
    background: var(--tile-cross);
    border-color: var(--accent);
    color: var(--accent);
  }
  .empty {
    background: transparent;
  }
</style>
