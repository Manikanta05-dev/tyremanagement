import { Outlet, Link, useLocation } from 'react-router-dom'
import { useState } from 'react'

const Layout = () => {
  const location = useLocation()
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
              T
            </div>
            <div className="user-details">
              <p className="user-name">Tire Shop</p>
              <p className="user-role">Admin</p>
            </div>
          </div>
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
        <div className="topbar-user">
          <div className="user-avatar-small">
            T
          </div>
        </div>
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
