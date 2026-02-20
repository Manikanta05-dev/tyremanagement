import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { purchaseAPI, inventoryAPI } from '../services/api'
import Loader from '../components/Loader'

const Purchase = () => {
  const [purchases, setPurchases] = useState([])
  const [inventory, setInventory] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({
    supplier_name: '',
    purchase_date: new Date().toISOString().split('T')[0],
    payment_status: 'pending',
    items: []
  })
  const [currentItem, setCurrentItem] = useState({
    tire_id: '',
    quantity: 1,
    purchase_price: 0
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [purchaseRes, invRes] = await Promise.all([
        purchaseAPI.getAll(),
        inventoryAPI.getAll({ limit: 1000 })
      ])
      setPurchases(purchaseRes.data)
      setInventory(invRes.data)
    } catch (error) {
      toast.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const addItemToList = () => {
    if (!currentItem.tire_id || currentItem.quantity < 1 || currentItem.purchase_price <= 0) {
      toast.error('Please fill all item details')
      return
    }

    const tire = inventory.find(t => t.id === parseInt(currentItem.tire_id))
    if (!tire) return

    // Check if tire already added
    const existingItem = formData.items.find(item => item.tire_id === parseInt(currentItem.tire_id))
    if (existingItem) {
      toast.error('This tire is already added. Remove it first to add again.')
      return
    }

    const newItem = {
      tire_id: parseInt(currentItem.tire_id),
      quantity: parseInt(currentItem.quantity),
      purchase_price: parseFloat(currentItem.purchase_price),
      tire_brand: tire.brand,
      tire_size: tire.tire_size,
      total: parseInt(currentItem.quantity) * parseFloat(currentItem.purchase_price)
    }

    setFormData({
      ...formData,
      items: [...formData.items, newItem]
    })

    // Reset current item
    setCurrentItem({
      tire_id: '',
      quantity: 1,
      purchase_price: 0
    })

    toast.success('Item added to purchase')
  }

  const removeItem = (index) => {
    const newItems = formData.items.filter((_, i) => i !== index)
    setFormData({
      ...formData,
      items: newItems
    })
    toast.success('Item removed')
  }

  const calculateTotal = () => {
    return formData.items.reduce((sum, item) => sum + item.total, 0)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (formData.items.length === 0) {
      toast.error('Please add at least one item to the purchase')
      return
    }

    if (!formData.supplier_name.trim()) {
      toast.error('Please enter supplier name')
      return
    }

    try {
      const purchaseData = {
        supplier_name: formData.supplier_name,
        purchase_date: formData.purchase_date,
        payment_status: formData.payment_status,
        items: formData.items.map(item => ({
          tire_id: item.tire_id,
          quantity: item.quantity,
          purchase_price: item.purchase_price
        }))
      }
      
      await purchaseAPI.create(purchaseData)
      toast.success('Purchase created successfully!')
      setShowModal(false)
      resetForm()
      fetchData()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create purchase')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this purchase?')) return
    try {
      await purchaseAPI.delete(id)
      toast.success('Purchase deleted successfully')
      fetchData()
    } catch (error) {
      toast.error('Failed to delete purchase')
    }
  }

  const resetForm = () => {
    setFormData({
      supplier_name: '',
      purchase_date: new Date().toISOString().split('T')[0],
      payment_status: 'pending',
      items: []
    })
    setCurrentItem({
      tire_id: '',
      quantity: 1,
      purchase_price: 0
    })
  }

  if (loading) return <Loader />

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Purchase Management</h1>
        <button
          onClick={() => { resetForm(); setShowModal(true) }}
          className="btn btn-primary"
        >
          + Add Purchase
        </button>
      </div>

      {/* Purchase History - Desktop Table */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Purchase History</h2>
        </div>
        
        <table className="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Supplier</th>
              <th>Items</th>
              <th>Total Amount</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {purchases.map((purchase) => (
              <tr key={purchase.id}>
                <td>{purchase.purchase_date}</td>
                <td className="font-semibold">{purchase.supplier_name}</td>
                <td>{purchase.items?.length || 0} item(s)</td>
                <td className="font-semibold">₹{purchase.total_amount.toFixed(2)}</td>
                <td>
                  <span className={`badge ${
                    purchase.payment_status === 'paid' ? 'badge-success' : 'badge-warning'
                  }`}>
                    {purchase.payment_status}
                  </span>
                </td>
                <td>
                  <button
                    onClick={() => handleDelete(purchase.id)}
                    className="btn btn-danger btn-icon"
                    style={{padding: '0.5rem 0.75rem', minHeight: 'auto'}}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Mobile Cards */}
        <div className="data-cards">
          {purchases.map((purchase) => (
            <div key={purchase.id} className="data-card">
              <div className="data-card-row">
                <span className="data-card-label">Date</span>
                <span className="data-card-value">{purchase.purchase_date}</span>
              </div>
              <div className="data-card-row">
                <span className="data-card-label">Supplier</span>
                <span className="data-card-value font-semibold">{purchase.supplier_name}</span>
              </div>
              <div className="data-card-row">
                <span className="data-card-label">Items</span>
                <span className="data-card-value">{purchase.items?.length || 0} item(s)</span>
              </div>
              <div className="data-card-row">
                <span className="data-card-label">Total</span>
                <span className="data-card-value font-semibold">₹{purchase.total_amount.toFixed(2)}</span>
              </div>
              <div className="data-card-row">
                <span className="data-card-label">Status</span>
                <span className="data-card-value">
                  <span className={`badge ${
                    purchase.payment_status === 'paid' ? 'badge-success' : 'badge-warning'
                  }`}>
                    {purchase.payment_status}
                  </span>
                </span>
              </div>
              <div className="data-card-actions">
                <button
                  onClick={() => handleDelete(purchase.id)}
                  className="btn btn-danger btn-full"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>

        {purchases.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">🛒</div>
            <p className="empty-state-text">No purchases found</p>
          </div>
        )}
      </div>

      {/* Multi-Item Purchase Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => { setShowModal(false); resetForm() }}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">Add Multi-Item Purchase</h2>
              <button className="modal-close" onClick={() => { setShowModal(false); resetForm() }}>
                <svg width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <form onSubmit={handleSubmit} id="purchaseForm">
                <div className="form-group">
                  <label className="form-label">Supplier Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.supplier_name}
                    onChange={(e) => setFormData({ ...formData, supplier_name: e.target.value })}
                    className="form-input"
                    placeholder="Enter supplier name"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Purchase Date *</label>
                  <input
                    type="date"
                    required
                    value={formData.purchase_date}
                    onChange={(e) => setFormData({ ...formData, purchase_date: e.target.value })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Payment Status *</label>
                  <select
                    value={formData.payment_status}
                    onChange={(e) => setFormData({ ...formData, payment_status: e.target.value })}
                    className="form-select"
                  >
                    <option value="pending">Pending</option>
                    <option value="paid">Paid</option>
                  </select>
                </div>

                <div style={{borderTop: '1px solid var(--border)', paddingTop: 'var(--spacing-md)', marginTop: 'var(--spacing-md)', backgroundColor: 'var(--primary-light)', padding: 'var(--spacing-md)', borderRadius: 'var(--radius)'}}>
                  <h3 className="font-semibold mb-2">Add Tire Item</h3>
                  <div className="form-group">
                    <label className="form-label">Select Tire</label>
                    <select
                      value={currentItem.tire_id}
                      onChange={(e) => setCurrentItem({ ...currentItem, tire_id: e.target.value })}
                      className="form-select"
                    >
                      <option value="">Choose tire...</option>
                      {inventory.map(tire => (
                        <option key={tire.id} value={tire.id}>
                          {tire.brand} - {tire.tire_size} ({tire.tire_type})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Quantity</label>
                    <input
                      type="number"
                      min="1"
                      value={currentItem.quantity}
                      onChange={(e) => setCurrentItem({ ...currentItem, quantity: e.target.value })}
                      className="form-input"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Price/Unit</label>
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={currentItem.purchase_price}
                      onChange={(e) => setCurrentItem({ ...currentItem, purchase_price: e.target.value })}
                      className="form-input"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={addItemToList}
                    className="btn btn-primary btn-full"
                  >
                    + Add Item to List
                  </button>
                </div>

                {formData.items.length > 0 && (
                  <div style={{marginTop: 'var(--spacing-md)', padding: 'var(--spacing-md)', backgroundColor: 'var(--bg-primary)', borderRadius: 'var(--radius)'}}>
                    <h3 className="font-semibold mb-2">Purchase Items ({formData.items.length})</h3>
                    <div style={{display: 'flex', flexDirection: 'column', gap: 'var(--spacing-sm)'}}>
                      {formData.items.map((item, index) => (
                        <div key={index} style={{padding: 'var(--spacing-sm)', backgroundColor: 'white', borderRadius: 'var(--radius)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', border: '1px solid var(--border)'}}>
                          <div>
                            <p className="font-semibold">{item.tire_brand} - {item.tire_size}</p>
                            <p className="text-sm" style={{color: 'var(--text-secondary)'}}>
                              Qty: {item.quantity} × ₹{item.purchase_price.toFixed(2)} = ₹{item.total.toFixed(2)}
                            </p>
                          </div>
                          <button
                            type="button"
                            onClick={() => removeItem(index)}
                            className="btn btn-danger btn-icon"
                            style={{padding: '0.5rem', minHeight: 'auto'}}
                          >
                            ✕
                          </button>
                        </div>
                      ))}
                    </div>
                    
                    <div style={{marginTop: 'var(--spacing-md)', paddingTop: 'var(--spacing-md)', borderTop: '2px solid var(--border)'}}>
                      <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '1.25rem', fontWeight: 700}}>
                        <span>Total Purchase Amount:</span>
                        <span style={{color: 'var(--primary)'}}>₹{calculateTotal().toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                )}
              </form>
            </div>
            <div className="modal-footer">
              <button
                type="submit"
                form="purchaseForm"
                disabled={formData.items.length === 0}
                className="btn btn-success btn-full"
              >
                Create Purchase ({formData.items.length} items)
              </button>
              <button
                type="button"
                onClick={() => { setShowModal(false); resetForm() }}
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

export default Purchase
