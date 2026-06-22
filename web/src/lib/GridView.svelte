<script>
  // Renders a grid, auto-scaling the cell size so the whole grid always fits the
  // available width (long words like "Marie-Claire" never get clipped).
  let { grid, max = 26, min = 10 } = $props()

  const GAP = 3
  let avail = $state(0)

  const size = $derived.by(() => {
    if (!avail || !grid?.cols) return max
    const s = Math.floor((avail - (grid.cols - 1) * GAP) / grid.cols)
    return Math.max(min, Math.min(max, s))
  })

  const cellMap = $derived(
    new Map((grid?.cells ?? []).map((c) => [`${c.row},${c.col}`, c]))
  )
</script>

<div class="wrap" bind:clientWidth={avail}>
  <div class="grid" style="--cols: {grid.cols}; --cell: {size}px; --gap: {GAP}px;">
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
</div>

<style>
  .wrap {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(var(--cols), var(--cell));
    gap: var(--gap);
  }
  .tile,
  .empty {
    width: var(--cell);
    height: var(--cell);
    border-radius: 5px;
  }
  .tile {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 650;
    font-size: calc(var(--cell) * 0.5);
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
