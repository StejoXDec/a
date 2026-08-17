const API_BASE = 'http://localhost:8000'

export const apiClient = {
  // Freshness check
  getFreshness: async (produkId) => {
    const res = await fetch(`${API_BASE}/produk/${produkId}/freshness`)
    if (!res.ok) throw new Error(`Freshness failed: ${res.statusText}`)
    return res.json()
  },

  // Price prediction
  getPricePrediction: async (kategori) => {
    const res = await fetch(`${API_BASE}/produk/kategori/${encodeURIComponent(kategori)}/prediksi-harga`)
    if (!res.ok) throw new Error(`Prediction failed: ${res.statusText}`)
    return res.json()
  },

  // Matching products
  getMatching: async (userId) => {
    const res = await fetch(`${API_BASE}/produk/matching/${userId}`)
    if (!res.ok) throw new Error(`Matching failed: ${res.statusText}`)
    return res.json()
  },

  // Notifications
  getNotifications: async (userId) => {
    const res = await fetch(`${API_BASE}/users/${userId}/notifications`)
    if (!res.ok) throw new Error(`Notifications failed: ${res.statusText}`)
    return res.json()
  },

  // List products by category
  getProducts: async (kategori) => {
    const res = await fetch(`${API_BASE}/produk?kategori=${encodeURIComponent(kategori)}`)
    if (!res.ok) throw new Error(`Products failed: ${res.statusText}`)
    return res.json()
  },

  // Get product by ID
  getProductById: async (produkId) => {
    const res = await fetch(`${API_BASE}/produk/${produkId}`)
    if (!res.ok) throw new Error(`Product failed: ${res.statusText}`)
    return res.json()
  },

  // Trace transaction
  getTransactionTrace: async (transactionId) => {
    const res = await fetch(`${API_BASE}/transaksi/${transactionId}/trace`)
    if (!res.ok) throw new Error(`Trace failed: ${res.statusText}`)
    return res.json()
  },
}

export default apiClient
