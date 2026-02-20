import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { inventoryAPI } from '../services/api'
import Loader from '../components/Loader'

const Inventory = () => {
  const [inventory, setInventory] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [formData, setFormData] = useState({
    brand: '',
    tire_size: '',
    tire_type: 'tubeless',
    quantity: 0,
    purchase_price: 0,
    selling_price: 0,
    purchase_date: new Date().toISOString().split('T')[0]
  })

  useEffect(() => {
    fetchInventory()
  }, [search])

  const fetchInventory = async () => {
    try {
      const response = await inventoryAPI.getAll({ search })
      setInventory(response.data)
    } catch (error) {
      toast.error('Failed to load inventory')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (editItem) {
        await inventoryAPI.update(editItem.id, formData)
        toast.success('Inventory updated successfully')
      } else {
        await inventoryAPI.create(formData)
        toast.success('Inventory added successfully')
      }
      setShowModal(false)
      resetForm()
      fetchInventory()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Operation failed')
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this item?')) return
    try {
      await inventoryAPI.delete(id)
      toast.success('Item deleted successfully')
      fetchInventory()
    } catch (error) {
      toast.error('Failed to delete item')
    }
  }

  const handleEdit = (item) => {
    setEditItem(item)
    setFormData({
      brand: item.brand,
      tire_size: item.tire_size,
      tire_type: item.tire_type,
      quantity: item.quantity,
      purchase_price: item.purchase_price,
      selling_price: item.selling_price,
      purchase_date: item.purchase_date
    })
    setShowModal(true)
  }

  const resetForm = () => {
    setFormData({
      brand: '',
      tire_size: '',
      tire_type: 'tubeless',
      quantity: 0,
      purchase_price: 0,
      selling_price: 0,
      purchase_date: new Date().toISOString().split('T')[0]
    })
    setEditItem(null)
  }

  if (loading) return <Loader />

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Tire Inventory</h1>
        <button
          onClick={() => { resetForm(); setShowModal(true) }}
          className="btn btn-primary"
        >
          + Add New Tire
        </button>
      </div>

      {/* Search */}
      <div className="search-bar">
        <svg className="search-icon" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          placeholder="Search by brand or size..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
      </div>

      {/* Desktop Table */}
      <table className="data-table">
        <thead>
          <tr>
            <th>Brand</th>
            <th>Size</th>
            <th>Type</th>
            <th>Quantity</th>
            <th>Purchase Price</th>
            <th>Selling Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {inventory.map((item) => (
            <tr key={item.id}>
              <td className="font-semibold">{item.brand}</td>
              <td>{item.tire_size}</td>
              <td>
                <span className="badge badge-primary">
                  {item.tire_type}
                </span>
              </td>
              <td>
                <span className={item.quantity < 5 ? 'font-semibold' : ''} style={{color: item.quantity < 5 ? 'var(--error)' : 'inherit'}}>
                  {item.quantity}
                  {item.quantity < 5 && ' ⚠️'}
                </span>
              </td>
              <td>₹{item.purchase_price}</td>
              <td>₹{item.selling_price}</td>
              <td>
                <div style={{display: 'flex', gap: 'var(--spacing-sm)'}}>
                  <button
                    onClick={() => handleEdit(item)}
                    className="btn btn-primary btn-icon"
                    style={{padding: '0.5rem 0.75rem', minHeight: 'auto'}}
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="btn btn-danger btn-icon"
                    style={{padding: '0.5rem 0.75rem', minHeight: 'auto'}}
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Mobile Cards */}
      <div className="data-cards">
        {inventory.map((item) => (
          <div key={item.id} className="data-card">
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
              <span className="data-card-value" style={{color: item.quantity < 5 ? 'var(--error)' : 'inherit', fontWeight: item.quantity < 5 ? 600 : 'normal'}}>
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
            <div className="data-card-actions">
              <button
                onClick={() => handleEdit(item)}
                className="btn btn-primary btn-full"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(item.id)}
                className="btn btn-danger btn-full"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {inventory.length === 0 && (
        <div className="empty-state">
          <div className="empty-state-icon">📦</div>
          <p className="empty-state-text">No inventory items found</p>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => { setShowModal(false); resetForm() }}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2 className="modal-title">{editItem ? 'Edit' : 'Add'} Tire</h2>
              <button className="modal-close" onClick={() => { setShowModal(false); resetForm() }}>
                <svg width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="modal-body">
              <form onSubmit={handleSubmit} id="inventoryForm">
                <div className="form-group">
                  <label className="form-label">Brand</label>
                  <input
                    type="text"
                    required
                    value={formData.brand}
                    onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Tire Size</label>
                  <input
                    type="text"
                    required
                    value={formData.tire_size}
                    onChange={(e) => setFormData({ ...formData, tire_size: e.target.value })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Type</label>
                  <select
                    value={formData.tire_type}
                    onChange={(e) => setFormData({ ...formData, tire_type: e.target.value })}
                    className="form-select"
                  >
                    <option value="tube">Tube</option>
                    <option value="tubeless">Tubeless</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Quantity</label>
                  <input
                    type="number"
                    required
                    min="0"
                    value={formData.quantity}
                    onChange={(e) => setFormData({ ...formData, quantity: parseInt(e.target.value) })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Purchase Price</label>
                  <input
                    type="number"
                    required
                    min="0"
                    step="0.01"
                    value={formData.purchase_price}
                    onChange={(e) => setFormData({ ...formData, purchase_price: parseFloat(e.target.value) })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Selling Price</label>
                  <input
                    type="number"
                    required
                    min="0"
                    step="0.01"
                    value={formData.selling_price}
                    onChange={(e) => setFormData({ ...formData, selling_price: parseFloat(e.target.value) })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Purchase Date</label>
                  <input
                    type="date"
                    required
                    value={formData.purchase_date}
                    onChange={(e) => setFormData({ ...formData, purchase_date: e.target.value })}
                    className="form-input"
                  />
                </div>
              </form>
            </div>
            <div className="modal-footer">
              <button
                type="submit"
                form="inventoryForm"
                className="btn btn-primary btn-full"
              >
                {editItem ? 'Update' : 'Add'}
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

export default Inventory
