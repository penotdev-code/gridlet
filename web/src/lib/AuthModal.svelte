<script>
  import Modal from './Modal.svelte'
  import { auth } from './auth.svelte.js'

  let { onclose } = $props()

  let mode = $state('login') // 'login' | 'register'
  let email = $state('')
  let password = $state('')
  let busy = $state(false)
  let error = $state('')

  async function submit(e) {
    e.preventDefault()
    busy = true
    error = ''
    try {
      if (mode === 'login') await auth.login(email, password)
      else await auth.register(email, password)
      onclose()
    } catch (err) {
      error = err.message ?? String(err)
    } finally {
      busy = false
    }
  }
</script>

<Modal title={mode === 'login' ? 'Connexion' : 'Créer un compte'} {onclose}>
  <form onsubmit={submit}>
    <label>
      Email
      <input type="email" bind:value={email} required autocomplete="email" />
    </label>
    <label>
      Mot de passe
      <input
        type="password"
        bind:value={password}
        required
        minlength={mode === 'register' ? 8 : undefined}
        autocomplete={mode === 'login' ? 'current-password' : 'new-password'}
      />
    </label>
    {#if mode === 'register'}
      <p class="hint">8 caractères minimum.</p>
    {/if}

    {#if error}<p class="error">{error}</p>{/if}

    <button class="primary" type="submit" disabled={busy}>
      {busy ? '…' : mode === 'login' ? 'Se connecter' : "S'inscrire"}
    </button>

    <p class="switch">
      {#if mode === 'login'}
        Pas de compte ?
        <button type="button" onclick={() => ((mode = 'register'), (error = ''))}>Créer un compte</button>
      {:else}
        Déjà un compte ?
        <button type="button" onclick={() => ((mode = 'login'), (error = ''))}>Se connecter</button>
      {/if}
    </p>
  </form>
</Modal>

<style>
  form {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  label {
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 13px;
    color: var(--muted);
  }
  input {
    padding: 10px 12px;
    border: 1px solid var(--line);
    border-radius: 9px;
    background: var(--surface);
    color: var(--ink);
    font: inherit;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-soft);
  }
  .hint {
    margin: -6px 0 0;
    font-size: 12px;
    color: var(--muted);
  }
  .error {
    margin: 0;
    color: #b5453a;
    font-size: 14px;
  }
  .primary {
    margin-top: 4px;
    padding: 11px;
    border: none;
    border-radius: 10px;
    background: var(--accent);
    color: #fff;
    font-weight: 650;
  }
  .primary:disabled {
    opacity: 0.6;
  }
  .switch {
    margin: 4px 0 0;
    text-align: center;
    font-size: 13px;
    color: var(--muted);
  }
  .switch button {
    border: none;
    background: transparent;
    color: var(--accent);
    text-decoration: underline;
    cursor: pointer;
    font: inherit;
  }
</style>
