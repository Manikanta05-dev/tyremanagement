import { useState } from 'react'
import toast from 'react-hot-toast'
import { profitAPI } from '../services/api'
import Loader from '../components/Loader'

const DailyClosing = () => {
  const [loading, setLoading] = useState(false)
  const [reportData, setReportData] = useState(null)
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0])

  const generateReport = async () => {
    setLoading(true)
    try {
      const response = await profitAPI.getDailyClosing(selectedDate)
      setReportData(response.data)
      toast.success('Report generated successfully')
    } catch (error) {
      toast.error('Failed to generate report')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Daily Closing Report</h1>
      </div>

      {/* Date Selection */}
      <div className="card">
        <div className="form-group">
          <label className="form-label">Select Date</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="form-input"
          />
        </div>
        <button
          onClick={generateReport}
          disabled={loading}
          className="btn btn-primary btn-full"
        >
          {loading ? 'Generating...' : 'Generate Report'}
        </button>
      </div>

      {loading && <Loader />}

      {reportData && (
        <div>
          {/* Summary Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-content">
                <p className="stat-label">Total Sales</p>
                <p className="stat-value" style={{color: 'var(--success)'}}>₹{reportData.total_sales.toFixed(2)}</p>
              </div>
              <div className="stat-icon">💰</div>
            </div>

            <div className="stat-card">
              <div className="stat-content">
                <p className="stat-label">Total Profit</p>
                <p className="stat-value" style={{color: 'var(--info)'}}>₹{reportData.total_profit.toFixed(2)}</p>
              </div>
              <div className="stat-icon">📈</div>
            </div>

            <div className="stat-card">
              <div className="stat-content">
                <p className="stat-label">Transactions</p>
                <p className="stat-value" style={{color: 'var(--accent-purple)'}}>{ reportData.total_transactions}</p>
              </div>
              <div className="stat-icon">🧾</div>
            </div>
          </div>

          {/* Payment Breakdown */}
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Payment Mode Breakdown</h2>
            </div>
            <div className="stats-grid">
              <div style={{padding: 'var(--spacing-md)', backgroundColor: 'var(--success-light)', borderRadius: 'var(--radius)', border: '1px solid var(--success)'}}>
                <p className="text-sm" style={{color: 'var(--text-secondary)', marginBottom: 'var(--spacing-xs)'}}>Cash Sales</p>
                <p style={{fontSize: '1.5rem', fontWeight: 700, color: 'var(--success)'}}>₹{reportData.cash_sales.toFixed(2)}</p>
              </div>
              <div style={{padding: 'var(--spacing-md)', backgroundColor: 'var(--info-light)', borderRadius: 'var(--radius)', border: '1px solid var(--info)'}}>
                <p className="text-sm" style={{color: 'var(--text-secondary)', marginBottom: 'var(--spacing-xs)'}}>UPI Sales</p>
                <p style={{fontSize: '1.5rem', fontWeight: 700, color: 'var(--info)'}}>₹{reportData.upi_sales.toFixed(2)}</p>
              </div>
              <div style={{padding: 'var(--spacing-md)', backgroundColor: 'var(--primary-light)', borderRadius: 'var(--radius)', border: '1px solid var(--primary)'}}>
                <p className="text-sm" style={{color: 'var(--text-secondary)', marginBottom: 'var(--spacing-xs)'}}>Card Sales</p>
                <p style={{fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary)'}}>₹{reportData.card_sales.toFixed(2)}</p>
              </div>
            </div>
          </div>

          {/* Additional Stats */}
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Additional Statistics</h2>
            </div>
            <div className="stats-grid">
              <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 'var(--spacing-md)', backgroundColor: 'var(--bg-primary)', borderRadius: 'var(--radius)'}}>
                <span className="font-semibold" style={{color: 'var(--text-primary)'}}>Total Items Sold</span>
                <span style={{fontSize: '1.5rem', fontWeight: 700}}>{reportData.total_items_sold}</span>
              </div>
              <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 'var(--spacing-md)', backgroundColor: 'var(--bg-primary)', borderRadius: 'var(--radius)'}}>
                <span className="font-semibold" style={{color: 'var(--text-primary)'}}>Avg Transaction</span>
                <span style={{fontSize: '1.5rem', fontWeight: 700}}>
                  ₹{reportData.total_transactions > 0 
                    ? (reportData.total_sales / reportData.total_transactions).toFixed(2) 
                    : '0.00'}
                </span>
              </div>
              <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 'var(--spacing-md)', backgroundColor: 'var(--bg-primary)', borderRadius: 'var(--radius)'}}>
                <span className="font-semibold" style={{color: 'var(--text-primary)'}}>Profit Margin</span>
                <span style={{fontSize: '1.5rem', fontWeight: 700}}>
                  {reportData.total_sales > 0 
                    ? ((reportData.total_profit / reportData.total_sales) * 100).toFixed(1) 
                    : '0.0'}%
                </span>
              </div>
            </div>
          </div>

          {/* Print Button */}
          <div style={{display: 'flex', justifyContent: 'flex-end'}}>
            <button
              onClick={() => window.print()}
              className="btn btn-outline"
            >
              🖨️ Print Report
            </button>
          </div>
        </div>
      )}

      {!reportData && !loading && (
        <div className="card">
          <div className="empty-state">
            <div className="empty-state-icon">📋</div>
            <p className="empty-state-text">Select a date and click "Generate Report" to view the daily closing report</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default DailyClosing
