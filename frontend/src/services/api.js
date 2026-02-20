import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
}

export const inventoryAPI = {
  getAll: (params) => api.get('/inventory/all', { params }),
  getById: (id) => api.get(`/inventory/${id}`),
  create: (data) => api.post('/inventory/add', data),
  update: (id, data) => api.put(`/inventory/update/${id}`, data),
  delete: (id) => api.delete(`/inventory/delete/${id}`),
}

export const salesAPI = {
  create: (data) => api.post('/sales/create', data),
  getHistory: (params) => api.get('/sales/history', { params }),
  getById: (id) => api.get(`/sales/${id}`),
}

export const purchaseAPI = {
  getAll: (params) => api.get('/purchase/all', { params }),
  getById: (id) => api.get(`/purchase/${id}`),
  create: (data) => api.post('/purchase/add', data),
  update: (id, data) => api.put(`/purchase/update/${id}`, data),
  delete: (id) => api.delete(`/purchase/delete/${id}`),
}

export const invoiceAPI = {
  generate: (saleId) => api.get(`/invoice/generate/${saleId}`, { responseType: 'blob' }),
  sendWhatsApp: (saleId, mobile) => api.post(`/invoice/send-whatsapp/${saleId}`, null, { params: { customer_mobile: mobile } }),
}

export const profitAPI = {
  getSummary: () => api.get('/profit/summary'),
  getDetails: (params) => api.get('/profit/details', { params }),
  getDailyClosing: (date) => api.get('/profit/daily-closing', { params: { report_date: date } }),
}

export const dashboardAPI = {
  getSummary: () => api.get('/dashboard/summary'),
}

export const reportsAPI = {
  getSalesReport: (params) => api.get('/reports/sales', { params }),
  getInventoryReport: () => api.get('/reports/inventory'),
}

export default api
