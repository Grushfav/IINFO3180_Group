import axios from 'axios'

/** Session cookie fallback for split frontend/API hosts (cross-site cookies often blocked). */
export const AUTH_TOKEN_STORAGE_KEY = 'dd_auth_token'

// Dev: point at Flask (e.g. http://localhost:8080).
// Prod (Render split deploy): set VITE_API_BASE_URL to your backend service URL, e.g.
// https://your-api.onrender.com
const envBase = import.meta.env.VITE_API_BASE_URL
const baseURL =
  typeof envBase === 'string' && envBase.length > 0
    ? envBase
    : import.meta.env.PROD
      ? ''
      : 'http://localhost:8080'

if (import.meta.env.PROD && (!envBase || String(envBase).trim().length === 0)) {
  // In production, an empty baseURL means "same-origin". That's only correct if the API is served
  // from the same host as the SPA. If you're deploying the API separately, set VITE_API_BASE_URL
  // in your frontend build environment.
  console.warn(
    '[api] VITE_API_BASE_URL is not set in production; requests will go to same-origin (/api/*).'
  )
}

const api = axios.create({
  baseURL,
  withCredentials: true, // Required for Flask-Login session cookies
})

api.interceptors.request.use((config) => {
  try {
    const t = sessionStorage.getItem(AUTH_TOKEN_STORAGE_KEY)
    if (t) {
      config.headers.Authorization = `Bearer ${t}`
    }
  } catch {
    /* ignore */
  }
  return config
})

export function buildMediaUrl(path) {
  if (!path) return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  const cleanBase = baseURL.replace(/\/$/, '')
  const cleanPath = path.startsWith('/') ? path : `/${path}`
  return `${cleanBase}${cleanPath}`
}

/** Turn stored profile_photo (filename or messy path) into a full URL under /static/uploads/. */
export function profilePhotoUrl(profilePhoto) {
  if (!profilePhoto) return null
  let p = String(profilePhoto).replace(/\\/g, '/').trim()
  if (p.startsWith('http://') || p.startsWith('https://')) return p
  const marker = 'static/uploads/'
  const idx = p.indexOf(marker)
  if (idx !== -1) {
    p = p.slice(idx + marker.length)
  } else {
    const slash = p.lastIndexOf('/')
    if (slash !== -1) p = p.slice(slash + 1)
  }
  if (!p) return null
  return buildMediaUrl(`/static/uploads/${p}`)
}

// Add response interceptor to handle 401s gracefully
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Session expired — clear local storage but don't redirect here
      // Let the router guard handle the redirect
      sessionStorage.removeItem('dd_user')
      sessionStorage.removeItem(AUTH_TOKEN_STORAGE_KEY)
    }
    return Promise.reject(error)
  }
)

export default api