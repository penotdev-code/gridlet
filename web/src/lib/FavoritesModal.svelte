<script>
  import Modal from './Modal.svelte'
  import GridView from './GridView.svelte'
  import { auth } from './auth.svelte.js'
  import { apiFetch } from './api.js'

  let { onclose } = $props()

  let items = $state([])
  let loading = $state(true)
  let error = $state('')

  async function refresh() {
    loading = true
    error = ''
    try {
      items = await apiFetch('/favorites', { token: auth.token })
    } catch (e) {
      error = e.message ?? String(e)
    } finally {
      loading = false
    }
  }
  refresh()

  async function remove(id) {
    try {
      await apiFetch(`/favorites/${id}`, { method: 'DELETE', token: auth.token })
      items = items.filter((i) => i.id !== id)
    } catch (e) {
      error = e.message ?? String(e)
    }
  }
</script>

<Modal title="Mes grilles favorites" {onclose}>
  {#if loading}
    <p class="muted">Chargement…</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if items.length === 0}
    <p class="muted">Aucune grille favorite. Générez une grille puis cliquez sur ♥.</p>
  {:else}
    <div class="grid-list">
      {#each items as fav (fav.id)}
        <div class="fav">
          <button class="del" onclick={() => remove(fav.id)} aria-label="Supprimer">×</button>
          <div class="preview">
            <GridView grid={fav.grid} max={22} />
          </div>
          <div class="meta">
            {fav.grid.cols}×{fav.grid.rows} · ⛓ {fav.grid.crossings}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</Modal>

<style>
  .muted {
    color: var(--muted);
    margin: 0;
  }
  .error {
    color: #b5453a;
    margin: 0;
  }
  .grid-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 14px;
  }
  .fav {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 14px 10px 10px;
    border: 1px solid var(--line);
    border-radius: 12px;
  }
  .preview {
    width: 100%;
    display: flex;
    justify-content: center;
  }
  .meta {
    font-size: 12px;
    color: var(--muted);
  }
  .del {
    position: absolute;
    top: 6px;
    right: 6px;
    width: 24px;
    height: 24px;
    border: none;
    background: var(--surface);
    color: var(--muted);
    font-size: 16px;
    border-radius: 6px;
    cursor: pointer;
  }
  .del:hover {
    background: var(--accent-soft);
    color: var(--accent);
  }
</style>
