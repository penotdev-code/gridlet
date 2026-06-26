// Reactive auth store (Svelte 5 runes in a module).
import { apiFetch } from './api.js'

const KEY = 'gridlet_token'

let token = $state(localStorage.getItem(KEY))
let user = $state(null)
let ready = $state(false)

function setToken(value) {
  token = value
  if (value) localStorage.setItem(KEY, value)
  else localStorage.removeItem(KEY)
}

async function refreshMe() {
  if (!token) {
    ready = true
    return
  }
  try {
    user = await apiFetch('/auth/me', { token })
  } catch (e) {
    // Only drop the session on an explicit auth failure, not transient errors.
    if (e.status === 401) {
      setToken(null)
      user = null
    }
  } finally {
    ready = true
  }
}

// Try to restore the session on load.
refreshMe()

export const auth = {
  get token() {
    return token
  },
  get user() {
    return user
  },
  get isAuthed() {
    return !!token && !!user
  },
  get ready() {
    return ready
  },

  async register(email, password) {
    const { access_token } = await apiFetch('/auth/register', {
      method: 'POST',
      body: { email, password },
    })
    setToken(access_token)
    user = await apiFetch('/auth/me', { token })
  },

  async login(email, password) {
    const { access_token } = await apiFetch('/auth/login', {
      method: 'POST',
      body: { email, password },
    })
    setToken(access_token)
    user = await apiFetch('/auth/me', { token })
  },

  logout() {
    setToken(null)
    user = null
  },
}
