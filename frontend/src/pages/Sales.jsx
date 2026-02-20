import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { salesAPI, inventoryAPI, invoiceAPI } from '../services/api'
import Loader from '../components/Loader'

const Sales = () => {
  const [inventory, setInventory] = useState([])
  const [salesHistory, setSalesHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [showBillModal, setShowBillModal] = useState(false)
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_mobile: '',
    payment_mode: 'cash',
    discount_type: 'flat',
    discount_value: 0,
    notes: '',
    items: []
  })
  const [selectedTire, setSelectedTire] = useState('')
  const [quantity, setQuantity] = useState(1)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [invRes, salesRes] = await Promise.all([
        inventoryAPI.getAll({ limit: 1000 }),
        salesAPI.getHistory({ limit: 50 })
      ])
      setInventory(invRes.data)
      setSalesHistory(salesRes.data)
    } catch (error) {
      toast.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const downloadInvoice = async (saleId, invoiceId) => {
    try {
      const response = await invoiceAPI.generate(saleId)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `invoice_${invoiceId}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('Invoice downloaded successfully')
    } catch (error) {
      toast.error('Failed to download invoice')
    }
  }

  const sendWhatsApp = async (saleId, mobile) => {
    try {
      await invoiceAPI.sendWhatsApp(saleId, mobile)
      toast.success('Invoice sent via WhatsApp')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to send WhatsApp message')
    }
  }

  const addItemToBill = () => {
    if (!selectedTire || quantity < 1) {
      toast.error('Please select a tire and quantity')
      return
    }

    const tire = inventory.find(t => t.id === parseInt(selectedTire))
    if (!tire) return

    if (tire.quantity < quantity) {
      toast.error('Insufficient stock')
      return
    }

    const existingItem = formData.items.find(item => item.tire_id === tire.id)
    if (existingItem) {
      toast.error('Item already added. Remove it first to add again.')
      return
    }

    setFormData({
      ...formData,
      items: [...formData.items, { tire_id: tire.id, quantity, tire }]
    })
    setSelectedTire('')
    setQuantity(1)
  }

  const removeItem = (tireId) => {
    setFormData({
      ...formData,
      items: formData.items.filter(item => item.tire_id !== tireId)
    })
  }

  const calculateSubtotal = () => {
    return formData.items.reduce((sum, item) => sum + (item.tire.selling_price * item.quantity), 0)
  }

  const calculateDiscount = () => {
    const subtotal = calculateSubtotal()
    if (formData.discount_type === 'percent') {
      return (subtotal * formData.discount_value) / 100
    }
    return formData.discount_value
  }

  const calculateTotal = () => {
    return calculateSubtotal() - calculateDiscount()
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (formData.items.length === 0) {
      toast.error('Please add at least one item')
      return
    }

    try {
      const saleData = {
        customer_name: formData.customer_name,
        customer_mobile: formData.customer_mobile,
        payment_mode: formData.payment_mode,
        discount_type: formData.discount_type,
        discount_value: parseFloat(formData.discount_value) || 0,
        notes: formData.notes || '',
        items: formData.items.map(item => ({
          tire_id: item.tire_id,
          quantity: item.quantity
        }))
      }
      
      await salesAPI.create(saleData)
      toast.success('Sale created successfully!')
      setShowBillModal(false)
      resetForm()
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create sale')
    }
  }

  const resetForm = () => {
    setFormData({
      customer_name: '',
      customer_mobile: '',
      payment_mode: 'cash',
      discount_type: 'flat',
      discount_value: 0,
      notes: '',
      items: []
    })
    setSelectedTire('')
    setQuantity(1)
  }

  if (loading) return <Loader />

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Sales Management</h1>
        <button
          onClick={() => { resetForm(); setShowBillModal(true) }}
          className="btn btn-success"
        >
          + New Sale
        </button>
      </div>

      {/* Sales History - Desktop Table */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Sales History</h2>
        </div>
        
        <table className="data-table">
          <thead>
            <tr>
              <th>Invoice ID</th>
              <th>Customer</th>
              <th>Mobile</th>
              <th>Items</th>
              <th>Subtotal</th>
              <th>Discount</th>
              <th>Total</th>
              <th>Payment</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {salesHistory.map((sale) => (
              <tr key={sale.id}>
                <td className="font-semibold">{sale.invoice_id}</td>
                <td>{sale.customer_name}</td>
                <td>{sale.customer_mobile}</td>
                <td>{sale.items.length}</td>
                <td>₹{sale.subtotal?.toFixed(2) || '0.00'}</td>
                <td>₹{sale.discount_amount?.toFixed(2) || '0.00'}</td>
                <td className="font-semibold">₹{sale.total_amount.toFixed(2)}</td>
                <td>
                  <span className="badge badge-success">
                    {sale.payment_mode}
                  </span>
                </td>
                <td>{new Date(sale.sale_date).toLocaleDateString()}</td>
                <td>
                  <div style={{display: 'flex', gap: 'var(--spacing-sm)'}}>
                    <button
                      onClick={() => downloadInvoice(sale.id, sale.invoice_id)}
                      className="btn btn-primary btn-icon"
                      style={{padding: '0.5rem', minHeight: 'auto', fontSize: '0.75rem'}}
                      title="Download Invoice"
                    >
                      📄
                    </button>
                    <button
                      onClick={() => sendWhatsApp(sale.id, sale.customer_mobile)}
                      className="btn btn-success btn-icon"
                      style={{padding: '0.5rem', minHeight: 'auto', fontSize: '0.75rem'}}
                      title="Send via WhatsApp"
                    >
                      📱
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Mobile Cards */}
        <div className="data-cards">
          {salesHistory.map((sale) => (
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
                <span className="data-card-label">Subtotal</span>
                <span className="data-card-value">₹{sale.subtotal?.toFixed(2) || '0.00'}</span>
              </div>
              <div className="data-card-row">
                <span className="data-card-label">Discount</span>
                <span className="data-card-value">₹{sale.discount_amount?.toFixed(2) || '0.00'}</span>
              </div>
              <div className="data-card-row">
                <span className="data-card-label">Total</span>
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
              <div className="data-card-actions">
                <button
                  onClick={() => downloadInvoice(sale.id, sale.invoice_id)}
                  className="btn btn-primary btn-full"
                >
                  📄 Download PDF
                </button>
                <button
                  onClick={() => sendWhatsApp(sale.id, sale.customer_mobile)}
                  className="btn btn-success btn-full"
                >
                  📱 Send WhatsApp
                </button>
              </div>
            </div>
          ))}
        </div>

        {salesHistory.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">💰</div>
            <p className="empty-state-text">No sales history</p>
          </div>
        )}
      </div>

      {/* Bill Modal */}
      {showBillModal && (
        <div className="modal-overlay" onClick={() => { setShowBillModal(false); resetForm() }}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Create New Sale</h2>
              <button className="modal-close" onClick={() => { setShowBillModal(false); resetForm() }}>
                <svg width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <form onSubmit={handleSubmit} id="salesForm">
                <div className="form-group">
                  <label className="form-label">Customer Name</label>
                  <input
                    type="text"
                    required
                    value={formData.customer_name}
                    onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Mobile Number</label>
                  <input
                    type="tel"
                    required
                    value={formData.customer_mobile}
                    onChange={(e) => setFormData({ ...formData, customer_mobile: e.target.value })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Payment Mode</label>
                  <select
                    value={formData.payment_mode}
                    onChange={(e) => setFormData({ ...formData, payment_mode: e.target.value })}
                    className="form-select"
                  >
                    <option value="cash">Cash</option>
                    <option value="upi">UPI</option>
                    <option value="card">Card</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Notes (Optional)</label>
                  <textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    className="form-input"
                    rows="2"
                    placeholder="Add any notes..."
                  />
                </div>

                <div style={{borderTop: '1px solid var(--border)', paddingTop: 'var(--spacing-md)', marginTop: 'var(--spacing-md)'}}>
                  <h3 className="font-semibold mb-2">Add Items</h3>
                  <div className="form-group">
                    <select
                      value={selectedTire}
                      onChange={(e) => setSelectedTire(e.target.value)}
                      className="form-select"
                    >
                      <option value="">Select Tire</option>
                      {inventory.filter(t => t.quantity > 0).map(tire => (
                        <option key={tire.id} value={tire.id}>
                          {tire.brand} - {tire.tire_size} (Stock: {tire.quantity}) - ₹{tire.selling_price}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Quantity</label>
                    <input
                      type="number"
                      min="1"
                      value={quantity}
                      onChange={(e) => setQuantity(parseInt(e.target.value))}
                      className="form-input"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={addItemToBill}
                    className="btn btn-primary btn-full"
                  >
                    Add Item
                  </button>
                </div>

                {formData.items.length > 0 && (
                  <div style={{marginTop: 'var(--spacing-md)', padding: 'var(--spacing-md)', backgroundColor: 'var(--bg-primary)', borderRadius: 'var(--radius)'}}>
                    <h3 className="font-semibold mb-2">Bill Items</h3>
                    <div style={{display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)'}}>
                      {formData.items.map((item) => (
                        <div key={item.tire_id} style={{padding: 'var(--spacing-sm)', backgroundColor: 'white', borderRadius: 'var(--radius)', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                          <div>
                            <p className="font-semibold">{item.tire.brand} - {item.tire.tire_size}</p>
                            <p className="text-sm" style={{color: 'var(--text-secondary)'}}>
                              {item.quantity} × ₹{item.tire.selling_price} = ₹{(item.quantity * item.tire.selling_price).toFixed(2)}
                            </p>
                          </div>
                          <button
                            type="button"
                            onClick={() => removeItem(item.tire_id)}
                            className="btn btn-danger btn-icon"
                            style={{padding: '0.5rem', minHeight: 'auto'}}
                          >
                            ✕
                          </button>
                        </div>
                      ))}
                    </div>

                    {/* Discount Section */}
                    <div style={{marginTop: 'var(--spacing-md)', paddingTop: 'var(--spacing-md)', borderTop: '1px solid var(--border)'}}>
                      <h4 className="font-semibold mb-2">Discount</h4>
                      <div style={{display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 'var(--spacing-sm)'}}>
                        <select
                          value={formData.discount_type}
                          onChange={(e) => setFormData({ ...formData, discount_type: e.target.value })}
                          className="form-select"
                        >
                          <option value="flat">Flat ₹</option>
                          <option value="percent">Percent %</option>
                        </select>
                        <input
                          type="number"
                          min="0"
                          step="0.01"
                          value={formData.discount_value}
                          onChange={(e) => setFormData({ ...formData, discount_value: e.target.value })}
                          className="form-input"
                          placeholder={formData.discount_type === 'percent' ? 'Enter %' : 'Enter ₹'}
                        />
                      </div>
                    </div>

                    {/* Bill Summary */}
                    <div style={{marginTop: 'var(--spacing-md)', paddingTop: 'var(--spacing-md)', borderTop: '2px solid var(--border)'}}>
                      <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--spacing-sm)'}}>
                        <span>Subtotal:</span>
                        <span>₹{calculateSubtotal().toFixed(2)}</span>
                      </div>
                      <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--spacing-sm)', color: 'var(--danger)'}}>
                        <span>Discount ({formData.discount_type === 'percent' ? `${formData.discount_value}%` : '₹'}):</span>
                        <span>- ₹{calculateDiscount().toFixed(2)}</span>
                      </div>
                      <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '1.25rem', fontWeight: 700, paddingTop: 'var(--spacing-sm)', borderTop: '1px solid var(--border)'}}>
                        <span>Total Amount:</span>
                        <span>₹{calculateTotal().toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                )}
              </form>
            </div>
            <div className="modal-footer">
              <button
                type="submit"
                form="salesForm"
                className="btn btn-success btn-full"
              >
                Create Sale
              </button>
              <button
                type="button"
                onClick={() => { setShowBillModal(false); resetForm() }}
                className="btn btn-outline btn-full"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Sales
