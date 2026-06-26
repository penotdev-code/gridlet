<script>
  import Modal from './Modal.svelte'
  import { auth } from './auth.svelte.js'
  import { apiFetch } from './api.js'

  let { onclose, onload } = $props()

  let items = $state([])
  let loading = $state(true)
  let error = $state('')

  async function refresh() {
    loading = true
    error = ''
    try {
      items = await apiFetch('/lists', { token: auth.token })
    } catch (e) {
      error = e.message ?? String(e)
    } finally {
      loading = false
    }
  }
  refresh()

  async function remove(id) {
    try {
      await apiFetch(`/lists/${id}`, { method: 'DELETE', token: auth.token })
      items = items.filter((i) => i.id !== id)
    } catch (e) {
      error = e.message ?? String(e)
    }
  }

  function load(item) {
    onload(item)
    onclose()
  }
</script>

<Modal title="Mes listes & modèles" {onclose}>
  {#if loading}
    <p class="muted">Chargement…</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if items.length === 0}
    <p class="muted">Aucune liste enregistrée pour l'instant.</p>
  {:else}
    <ul class="list">
      {#each items as item (item.id)}
        <li>
          <div class="info">
            <span class="name">{item.name}</span>
            {#if item.is_template}<span class="badge">modèle</span>{/if}
            <span class="meta">{item.items.length} mot{item.items.length > 1 ? 's' : ''} · écart {item.gap}</span>
          </div>
          <div class="actions">
            <button class="load" onclick={() => load(item)}>Charger</button>
            <button class="del" onclick={() => remove(item.id)} aria-label="Supprimer">×</button>
          </div>
        </li>
      {/each}
    </ul>
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
  .list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 10px 12px;
    border: 1px solid var(--line);
    border-radius: 10px;
  }
  .info {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    min-width: 0;
  }
  .name {
    font-weight: 600;
  }
  .badge {
    font-size: 11px;
    font-weight: 700;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 2px 7px;
    border-radius: 999px;
  }
  .meta {
    font-size: 12px;
    color: var(--muted);
  }
  .actions {
    display: flex;
    align-items: center;
    gap: 6px;
    flex: none;
  }
  .load {
    padding: 6px 12px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--surface);
    color: var(--ink);
    cursor: pointer;
  }
  .load:hover {
    background: var(--tile);
    border-color: var(--accent);
  }
  .del {
    width: 28px;
    height: 30px;
    border: none;
    background: transparent;
    color: var(--muted);
    font-size: 18px;
    border-radius: 8px;
    cursor: pointer;
  }
  .del:hover {
    background: var(--accent-soft);
    color: var(--accent);
  }
</style>
