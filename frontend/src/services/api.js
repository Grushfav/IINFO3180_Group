import axios from 'axios'

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

const api = axios.create({
  baseURL,
  withCredentials: true, // Required for Flask-Login session cookies
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
    }
    return Promise.reject(error)
  }
)

export default api