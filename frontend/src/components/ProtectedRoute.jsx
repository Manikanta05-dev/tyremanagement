import { Navigate } from 'react-router-dom'
import { isAuthenticated } from '../utils/auth'

const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    // Clear any invalid tokens
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    return <Navigate to="/login" replace />
  }
  
  return children
}

export default ProtectedRoute
