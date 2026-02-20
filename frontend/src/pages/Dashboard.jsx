import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import toast from 'react-hot-toast'
import { dashboardAPI } from '../services/api'
import Loader from '../components/Loader'

const Dashboard = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const response = await dashboardAPI.getSummary()
      setData(response.data)
    } catch (error) {
      toast.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <Loader />

  const { summary, low_stock_items, sales_chart } = data || {}

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-content">
            <p className="stat-label">Today's Sales</p>
            <p className="stat-value">₹{summary?.total_sales_today?.toFixed(2) || 0}</p>
          </div>
          <div className="stat-icon">💰</div>
        </div>

        <div className="stat-card">
          <div className="stat-content">
            <p className="stat-label">Today's Profit</p>
            <p className="stat-value" style={{color: 'var(--success)'}}>₹{summary?.daily_profit?.toFixed(2) || 0}</p>
          </div>
          <div className="stat-icon">📈</div>
        </div>

        <div className="stat-card">
          <div className="stat-content">
            <p className="stat-label">Monthly Revenue</p>
            <p className="stat-value">₹{summary?.total_monthly_revenue?.toFixed(2) || 0}</p>
          </div>
          <div className="stat-icon">💵</div>
        </div>

        <div className="stat-card">
          <div className="stat-content">
            <p className="stat-label">Monthly Profit</p>
            <p className="stat-value" style={{color: 'var(--info)'}}>₹{summary?.monthly_profit?.toFixed(2) || 0}</p>
          </div>
          <div className="stat-icon">💎</div>
        </div>

        <div className="stat-card">
          <div className="stat-content">
            <p className="stat-label">Low Stock Alert</p>
            <p className="stat-value" style={{color: 'var(--error)'}}>{ summary?.low_stock_count || 0}</p>
          </div>
          <div className="stat-icon">⚠️</div>
        </div>
      </div>

      <div className="content-grid-2">
        {/* Sales Chart */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Sales Trend (Last 7 Days)</h2>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={sales_chart || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="amount" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Low Stock Items */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Low Stock Items</h2>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)'}}>
            {low_stock_items?.length > 0 ? (
              low_stock_items.map((item) => (
                <div key={item.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: 'var(--spacing-md)',
                  backgroundColor: 'var(--error-light)',
                  borderRadius: 'var(--radius)',
                  border: '1px solid var(--error)'
                }}>
                  <div>
                    <p className="font-semibold">{item.brand}</p>
                    <p className="text-sm" style={{color: 'var(--text-secondary)'}}>{item.tire_size}</p>
                  </div>
                  <span className="badge badge-error">
                    {item.quantity} left
                  </span>
                </div>
              ))
            ) : (
              <div className="empty-state">
                <p className="empty-state-text">No low stock items</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
