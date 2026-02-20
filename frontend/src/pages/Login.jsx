import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { authAPI } from '../services/api'
import { setToken, setUser } from '../utils/auth'

const Login = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({ username: '', password: '' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      console.log('Attempting login with:', { username: formData.username })
      const response = await authAPI.login(formData)
      console.log('Login response:', response)
      const { access_token, user } = response.data
      
      setToken(access_token)
      setUser(user)
      
      toast.success('Login successful!')
      navigate('/dashboard')
    } catch (error) {
      console.error('Login error:', error)
      console.error('Error response:', error.response)
      toast.error(error.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
      padding: 'var(--spacing-md)',
      position: 'relative',
      zIndex: 1
    }}>
      <div style={{
        backgroundColor: 'var(--bg-secondary)',
        padding: 'var(--spacing-xl)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-xl)',
        width: '100%',
        maxWidth: '400px',
        position: 'relative',
        zIndex: 2
      }}>
        <div style={{textAlign: 'center', marginBottom: 'var(--spacing-xl)'}}>
          <h1 style={{fontSize: '2rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: 'var(--spacing-sm)'}}>🚗 Tire Shop</h1>
          <p style={{color: 'var(--text-secondary)', marginTop: 'var(--spacing-sm)'}}>Inventory Management System</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              required
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              className="form-input"
              placeholder="Enter username"
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="form-input"
              placeholder="Enter password"
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary btn-full"
            style={{marginTop: 'var(--spacing-md)'}}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div style={{marginTop: 'var(--spacing-lg)', textAlign: 'center', fontSize: '0.875rem', color: 'var(--text-secondary)'}}>
          <p>Default credentials:</p>
          <p style={{fontFamily: 'monospace', marginTop: 'var(--spacing-xs)', fontWeight: 600, backgroundColor: 'var(--bg-primary)', padding: 'var(--spacing-sm)', borderRadius: 'var(--radius)'}}>admin / admin123</p>
        </div>
      </div>
    </div>
  )
}

export default Login
