<script>
  let { title, onclose, children } = $props()

  function onKeydown(e) {
    if (e.key === 'Escape') onclose()
  }
</script>

<svelte:window onkeydown={onKeydown} />

<div class="backdrop" onclick={onclose} role="presentation">
  <div class="modal" role="dialog" aria-modal="true" aria-label={title} onclick={(e) => e.stopPropagation()}>
    <div class="head">
      <h3>{title}</h3>
      <button class="close" onclick={onclose} aria-label="Fermer">×</button>
    </div>
    <div class="body">
      {@render children()}
    </div>
  </div>
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(44, 42, 38, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    z-index: 50;
    animation: fade 0.12s ease-out;
  }
  .modal {
    width: 100%;
    max-width: 460px;
    max-height: 85vh;
    overflow: auto;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(44, 42, 38, 0.25);
    animation: pop 0.14s ease-out;
  }
  .head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 20px;
    border-bottom: 1px solid var(--line);
  }
  .head h3 {
    margin: 0;
    font-size: 18px;
  }
  .close {
    border: none;
    background: transparent;
    color: var(--muted);
    font-size: 24px;
    line-height: 1;
    cursor: pointer;
    border-radius: 8px;
    width: 32px;
    height: 32px;
  }
  .close:hover {
    background: var(--tile);
    color: var(--ink);
  }
  .body {
    padding: 20px;
  }
  @keyframes fade {
    from {
      opacity: 0;
    }
  }
  @keyframes pop {
    from {
      transform: translateY(8px) scale(0.98);
      opacity: 0;
    }
  }
</style>
