import { Outlet, Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { logout, getUser } from '../utils/auth'

const Layout = () => {
  const location = useLocation()
  const user = getUser()
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const mainNavItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊', mobileIcon: '🏠' },
    { path: '/inventory', label: 'Inventory', icon: '📦', mobileIcon: '📦' },
    { path: '/purchase', label: 'Purchase', icon: '🛒', mobileIcon: '🛒' },
    { path: '/sales', label: 'Sales', icon: '💰', mobileIcon: '💰' },
    { path: '/reports', label: 'Reports', icon: '📈', mobileIcon: '📊' },
  ]

  const secondaryNavItems = [
    { path: '/daily-closing', label: 'Daily Closing', icon: '📋' },
  ]

  return (
    <div className="app-container">
      {/* Desktop Sidebar */}
      <aside className={`desktop-sidebar ${isSidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="brand">
            <span className="brand-icon">🚗</span>
            <div className="brand-text">
              <h1>Tire Shop</h1>
              <p>Inventory System</p>
            </div>
          </div>
        </div>
        
        <nav className="sidebar-nav">
          <div className="nav-section">
            <p className="nav-section-title">Main Menu</p>
            {mainNavItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </Link>
            ))}
          </div>
          
          <div className="nav-section">
            <p className="nav-section-title">Other</p>
            {secondaryNavItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </Link>
            ))}
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              {(user?.full_name || user?.username || 'U').charAt(0).toUpperCase()}
            </div>
            <div className="user-details">
              <p className="user-name">{user?.full_name || user?.username}</p>
              <p className="user-role">{user?.role}</p>
            </div>
          </div>
          <button onClick={logout} className="logout-btn" title="Logout">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
            </svg>
          </button>
        </div>
      </aside>

      {/* Mobile Top Bar */}
      <header className="mobile-topbar">
        <button 
          className="menu-toggle"
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            setIsSidebarOpen(!isSidebarOpen)
          }}
          aria-label="Toggle menu"
          style={{
            zIndex: 101,
            position: 'relative',
            touchAction: 'manipulation'
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            {isSidebarOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            )}
          </svg>
        </button>
        <div className="topbar-brand">
          <span className="brand-icon">🚗</span>
          <h1>Tire Shop</h1>
        </div>
        <button 
          className="topbar-user"
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            logout()
          }}
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            touchAction: 'manipulation',
            padding: 0
          }}
          title="Logout"
        >
          <div className="user-avatar-small">
            {(user?.full_name || user?.username || 'U').charAt(0).toUpperCase()}
          </div>
        </button>
      </header>

      {/* Overlay for mobile sidebar */}
      {isSidebarOpen && (
        <div 
          className="sidebar-overlay"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="main-content">
        <Outlet />
      </main>

      {/* Mobile Bottom Navigation */}
      <nav className="mobile-bottom-nav">
        {mainNavItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`bottom-nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="bottom-nav-icon">{item.mobileIcon}</span>
            <span className="bottom-nav-label">{item.label}</span>
          </Link>
        ))}
      </nav>
    </div>
  )
}

export default Layout
