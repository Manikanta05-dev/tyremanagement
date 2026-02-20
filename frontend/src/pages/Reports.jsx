import { useState } from 'react'
import toast from 'react-hot-toast'
import { reportsAPI } from '../services/api'
import Loader from '../components/Loader'

const Reports = () => {
  const [reportType, setReportType] = useState('sales')
  const [loading, setLoading] = useState(false)
  const [reportData, setReportData] = useState(null)
  const [dateRange, setDateRange] = useState({
    start_date: new Date().toISOString().split('T')[0],
    end_date: new Date().toISOString().split('T')[0]
  })

  const generateReport = async () => {
    setLoading(true)
    try {
      let response
      if (reportType === 'sales') {
        response = await reportsAPI.getSalesReport(dateRange)
      } else {
        response = await reportsAPI.getInventoryReport()
      }
      setReportData(response.data)
      toast.success('Report generated successfully')
    } catch (error) {
      toast.error('Failed to generate report')
    } finally {
      setLoading(false)
    }
  }

  const calculateSalesTotal = () => {
    if (!reportData || reportType !== 'sales') return 0
    return reportData.reduce((sum, sale) => sum + sale.total_amount, 0)
  }

  const calculateInventoryValue = () => {
    if (!reportData || reportType !== 'inventory') return 0
    return reportData.reduce((sum, item) => sum + (item.selling_price * item.quantity), 0)
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Reports</h1>
      </div>

      {/* Report Controls */}
      <div className="card">
        <div className="form-group">
          <label className="form-label">Report Type</label>
          <select
            value={reportType}
            onChange={(e) => { setReportType(e.target.value); setReportData(null) }}
            className="form-select"
          >
            <option value="sales">Sales Report</option>
            <option value="inventory">Inventory Report</option>
          </select>
        </div>

        {reportType === 'sales' && (
          <>
            <div className="form-group">
              <label className="form-label">Start Date</label>
              <input
                type="date"
                value={dateRange.start_date}
                onChange={(e) => setDateRange({ ...dateRange, start_date: e.target.value })}
                className="form-input"
              />
            </div>
            <div className="form-group">
              <label className="form-label">End Date</label>
              <input
                type="date"
                value={dateRange.end_date}
                onChange={(e) => setDateRange({ ...dateRange, end_date: e.target.value })}
                className="form-input"
              />
            </div>
          </>
        )}

        <button
          onClick={generateReport}
          disabled={loading}
          className="btn btn-primary btn-full"
        >
          {loading ? 'Generating...' : 'Generate Report'}
        </button>
      </div>

      {/* Report Display */}
      {loading && <Loader />}

      {reportData && reportType === 'sales' && (
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Sales Report</h2>
            <p className="text-sm" style={{color: 'var(--text-secondary)'}}>
              {dateRange.start_date} to {dateRange.end_date}
            </p>
          </div>
          <div style={{padding: 'var(--spacing-md)', backgroundColor: 'var(--info-light)', borderRadius: 'var(--radius)', margin: 'var(--spacing-md)'}}>
            <p className="text-sm" style={{color: 'var(--text-secondary)'}}>Total Sales</p>
            <p style={{fontSize: '2rem', fontWeight: 700, color: 'var(--info)'}}>₹{calculateSalesTotal().toFixed(2)}</p>
          </div>

          {/* Desktop Table */}
          <table className="data-table">
            <thead>
              <tr>
                <th>Invoice ID</th>
                <th>Customer</th>
                <th>Mobile</th>
                <th>Items</th>
                <th>Amount</th>
                <th>Payment</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {reportData.map((sale) => (
                <tr key={sale.id}>
                  <td className="font-semibold">{sale.invoice_id}</td>
                  <td>{sale.customer_name}</td>
                  <td>{sale.customer_mobile}</td>
                  <td>{sale.items.length}</td>
                  <td className="font-semibold">₹{sale.total_amount.toFixed(2)}</td>
                  <td>
                    <span className="badge badge-success">
                      {sale.payment_mode}
                    </span>
                  </td>
                  <td>{new Date(sale.sale_date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Mobile Cards */}
          <div className="data-cards">
            {reportData.map((sale) => (
              <div key={sale.id} className="data-card">
                <div className="data-card-row">
                  <span className="data-card-label">Invoice</span>
                  <span className="data-card-value font-semibold">{sale.invoice_id}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Customer</span>
                  <span className="data-card-value">{sale.customer_name}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Mobile</span>
                  <span className="data-card-value">{sale.customer_mobile}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Items</span>
                  <span className="data-card-value">{sale.items.length}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Amount</span>
                  <span className="data-card-value font-semibold">₹{sale.total_amount.toFixed(2)}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Payment</span>
                  <span className="data-card-value">
                    <span className="badge badge-success">{sale.payment_mode}</span>
                  </span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Date</span>
                  <span className="data-card-value">{new Date(sale.sale_date).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>

          {reportData.length === 0 && (
            <div className="empty-state">
              <div className="empty-state-icon">📊</div>
              <p className="empty-state-text">No sales found for this period</p>
            </div>
          )}
        </div>
      )}

      {reportData && reportType === 'inventory' && (
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Inventory Report</h2>
          </div>
          <div className="stats-grid">
            <div style={{padding: 'var(--spacing-md)', backgroundColor: 'var(--info-light)', borderRadius: 'var(--radius)'}}>
              <p className="text-sm" style={{color: 'var(--text-secondary)'}}>Total Items</p>
              <p style={{fontSize: '1.5rem', fontWeight: 700, color: 'var(--info)'}}>{ reportData.length}</p>
            </div>
            <div style={{padding: 'var(--spacing-md)', backgroundColor: 'var(--success-light)', borderRadius: 'var(--radius)'}}>
              <p className="text-sm" style={{color: 'var(--text-secondary)'}}>Total Value</p>
              <p style={{fontSize: '1.5rem', fontWeight: 700, color: 'var(--success)'}}>₹{calculateInventoryValue().toFixed(2)}</p>
            </div>
            <div style={{padding: 'var(--spacing-md)', backgroundColor: 'var(--error-light)', borderRadius: 'var(--radius)'}}>
              <p className="text-sm" style={{color: 'var(--text-secondary)'}}>Low Stock</p>
              <p style={{fontSize: '1.5rem', fontWeight: 700, color: 'var(--error)'}}>
                {reportData.filter(item => item.quantity < 5).length}
              </p>
            </div>
          </div>

          {/* Desktop Table */}
          <table className="data-table">
            <thead>
              <tr>
                <th>Brand</th>
                <th>Size</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Purchase</th>
                <th>Selling</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {reportData.map((item) => (
                <tr key={item.id} style={item.quantity < 5 ? {backgroundColor: 'var(--error-light)'} : {}}>
                  <td className="font-semibold">{item.brand}</td>
                  <td>{item.tire_size}</td>
                  <td>
                    <span className="badge badge-primary">
                      {item.tire_type}
                    </span>
                  </td>
                  <td>
                    <span className={item.quantity < 5 ? 'font-semibold' : ''} style={item.quantity < 5 ? {color: 'var(--error)'} : {}}>
                      {item.quantity}
                      {item.quantity < 5 && ' ⚠️'}
                    </span>
                  </td>
                  <td>₹{item.purchase_price}</td>
                  <td>₹{item.selling_price}</td>
                  <td className="font-semibold">
                    ₹{(item.selling_price * item.quantity).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Mobile Cards */}
          <div className="data-cards">
            {reportData.map((item) => (
              <div key={item.id} className="data-card" style={item.quantity < 5 ? {backgroundColor: 'var(--error-light)', border: '1px solid var(--error)'} : {}}>
                <div className="data-card-row">
                  <span className="data-card-label">Brand</span>
                  <span className="data-card-value font-semibold">{item.brand}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Size</span>
                  <span className="data-card-value">{item.tire_size}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Type</span>
                  <span className="data-card-value">
                    <span className="badge badge-primary">{item.tire_type}</span>
                  </span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Quantity</span>
                  <span className="data-card-value" style={item.quantity < 5 ? {color: 'var(--error)', fontWeight: 600} : {}}>
                    {item.quantity}
                    {item.quantity < 5 && ' ⚠️'}
                  </span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Purchase</span>
                  <span className="data-card-value">₹{item.purchase_price}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Selling</span>
                  <span className="data-card-value">₹{item.selling_price}</span>
                </div>
                <div className="data-card-row">
                  <span className="data-card-label">Value</span>
                  <span className="data-card-value font-semibold">
                    ₹{(item.selling_price * item.quantity).toFixed(2)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Reports
