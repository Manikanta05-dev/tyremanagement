export const getToken = () => localStorage.getItem('token')

export const setToken = (token) => localStorage.setItem('token', token)

export const removeToken = () => localStorage.removeItem('token')

export const getUser = () => {
  try {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  } catch (error) {
    console.error('Error parsing user data:', error)
    return null
  }
}

export const setUser = (user) => localStorage.setItem('user', JSON.stringify(user))

export const removeUser = () => localStorage.removeItem('user')

export const isAuthenticated = () => {
  const token = getToken()
  const user = getUser()
  
  if (!token || !user) {
    return false
  }
  
  // Check if token is expired (basic check)
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const currentTime = Date.now() / 1000
    
    if (payload.exp < currentTime) {
      // Token expired, clear storage
      removeToken()
      removeUser()
      return false
    }
    
    return true
  } catch (error) {
    console.error('Token validation error:', error)
    // Invalid token format, clear storage
    removeToken()
    removeUser()
    return false
  }
}

export const logout = () => {
  removeToken()
  removeUser()
  window.location.href = '/login'
}

export const login = async (credentials) => {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }
    
    const data = await response.json()
    
    // Store token and user data
    setToken(data.access_token)
    setUser(data.user)
    
    return data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}
