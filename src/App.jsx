import { useMemo, useState, useEffect } from 'react'
import apiClient from './api'

const palette = {
  forest: '#1F3D2B',
  forestLight: '#2E5540',
  sage: '#7C9473',
  sageSoft: '#DCE4D4',
  harvest: '#E2A23B',
  tomato: '#D14D2A',
  freshGreen: '#4C8C4A',
  bg: '#F6F2E4',
  paper: '#FFFDF8',
}

const products = [
  {
    id: 1,
    name: 'Cabai Rawit',
    farmer: 'Pak Budi',
    location: 'Cirebon',
    distance: '2.3 km',
    quantity: 68,
    unit: 'kg',
    harvestAge: 3,
    freshness: 82,
    price: 42000,
    marketPrice: 51000,
    status: 'Segar',
    discount: 0,
    note: 'AI: jual dalam 2 hari untuk hasil optimal',
    image: '🌶️',
    trend: [42, 44, 46, 49, 52, 48],
  },
  {
    id: 2,
    name: 'Tomat',
    farmer: 'Ibu Sari',
    location: 'Bandung',
    distance: '4.1 km',
    quantity: 140,
    unit: 'kg',
    harvestAge: 5,
    freshness: 58,
    price: 34000,
    marketPrice: 42000,
    status: '2 hr lagi',
    discount: 18,
    note: 'AI: potensi kerugian naik 12%',
    image: '🍅',
    trend: [36, 39, 41, 38, 35, 31],
  },
  {
    id: 3,
    name: 'Jagung Manis',
    farmer: 'Pak Damar',
    location: 'Bogor',
    distance: '5.6 km',
    quantity: 90,
    unit: 'kg',
    harvestAge: 2,
    freshness: 88,
    price: 16000,
    marketPrice: 20000,
    status: 'Segar',
    discount: 0,
    note: 'AI: permintaan naik akhir pekan',
    image: '🌽',
    trend: [29, 34, 33, 37, 40, 44],
  },
  {
    id: 4,
    name: 'Sawi Hijau',
    farmer: 'Pak Rudi',
    location: 'Depok',
    distance: '7.8 km',
    quantity: 52,
    unit: 'kg',
    harvestAge: 4,
    freshness: 49,
    price: 12000,
    marketPrice: 15500,
    status: '-30% diskon',
    discount: 30,
    note: 'AI: jual cepat untuk hindari pembusukan',
    image: '🥬',
    trend: [22, 27, 31, 30, 28, 25],
  },
  {
    id: 5,
    name: 'Kentang',
    farmer: 'Ibu Lina',
    location: 'Tasikmalaya',
    distance: '9.2 km',
    quantity: 120,
    unit: 'kg',
    harvestAge: 6,
    freshness: 41,
    price: 21000,
    marketPrice: 26000,
    status: 'Risiko tinggi',
    discount: 25,
    note: 'AI: pasar butuh proses cepat',
    image: '🥔',
    trend: [28, 31, 30, 29, 25, 20],
  },
  {
    id: 6,
    name: 'Buncis',
    farmer: 'Pak Joko',
    location: 'Garut',
    distance: '11.1 km',
    quantity: 78,
    unit: 'kg',
    harvestAge: 2,
    freshness: 76,
    price: 18000,
    marketPrice: 22000,
    status: 'Segar',
    discount: 0,
    note: 'AI: kualitas stabil minggu ini',
    image: '🫘',
    trend: [39, 42, 43, 46, 49, 52],
  },
  {
    id: 7,
    name: 'Timun',
    farmer: 'Bu Tati',
    location: 'Sukabumi',
    distance: '6.7 km',
    quantity: 62,
    unit: 'kg',
    harvestAge: 3,
    freshness: 68,
    price: 13800,
    marketPrice: 17500,
    status: 'Segar',
    discount: 12,
    note: 'AI: pelanggan suka untuk toko sayur',
    image: '🥒',
    trend: [31, 33, 36, 40, 39, 41],
  },
]

const notifications = [
  { id: 1, type: 'urgent', text: 'Cabai rawit Pak Budi butuh penjualan hari ini agar tidak turun kualitas.', time: '2 menit lalu', dot: palette.tomato },
  { id: 2, type: 'success', text: 'Permintaan pasar baru cocok dengan stok tomat Ibu Sari.', time: '18 menit lalu', dot: palette.freshGreen },
  { id: 3, type: 'info', text: 'Harga sayur hijau naik 7% dalam 3 hari terakhir.', time: '1 jam lalu', dot: palette.harvest },
  { id: 4, type: 'sage', text: 'Distributor dari Bandung meminta 40 kg sawi hijau.', time: '2 jam lalu', dot: palette.sage },
]

const traceNodes = [
  { label: 'Petani', value: 'Rp 24.500', share: 57 },
  { label: 'Distributor', value: 'Rp 9.500', share: 22 },
  { label: 'Konsumen', value: 'Rp 42.000', share: 21 },
]

const productCategories = ['Cabai rawit', 'Tomat', 'Jagung manis', 'Sawi hijau', 'Kentang', 'Buncis', 'Timun']

function formatPrice(value) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(value)
}

function getFreshnessTone(value) {
  if (value >= 70) return 'fresh'
  if (value >= 45) return 'warn'
  return 'danger'
}

function FreshnessMeter({ value, compact = false }) {
  const tone = getFreshnessTone(value)
  const gradient = `linear-gradient(90deg, ${palette.freshGreen} 0%, ${palette.harvest} 52%, ${palette.tomato} 100%)`

  return (
    <div className={`freshness ${compact ? 'compact' : ''}`}>
      <div className="meter-labels">
        <span>Segar</span>
        <span className="muted">{value}%</span>
      </div>
      <div className="meter-track" aria-label={`Freshness ${value}%`}>
        <div className="meter-fill" style={{ width: `${value}%`, background: gradient }} />
      </div>
      <div className={`meter-status ${tone}`}>
        {tone === 'fresh' ? 'Segar' : tone === 'warn' ? 'Perlu dijual cepat' : 'Risiko busuk tinggi'}
      </div>
    </div>
  )
}

function Sparkline({ points }) {
  const max = Math.max(...points)
  const min = Math.min(...points)
  const values = points
    .map((point, index) => {
      const x = (index / (points.length - 1)) * 100
      const y = 100 - ((point - min) / (Math.max(max - min, 1) || 1)) * 100
      return `${x},${y}`
    })
    .join(' ')

  return (
    <svg viewBox="0 0 100 35" preserveAspectRatio="none" className="sparkline">
      <defs>
        <linearGradient id="sparkGradient" x1="0" x2="1">
          <stop offset="0%" stopColor={palette.freshGreen} />
          <stop offset="100%" stopColor={palette.forestLight} />
        </linearGradient>
      </defs>
      <polyline points={values} fill="none" stroke="url(#sparkGradient)" strokeWidth="2.2" strokeLinejoin="round" strokeLinecap="round" />
    </svg>
  )
}

function App() {
  const [tab, setTab] = useState('farmer')
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('terdekat')
  const [allProducts, setAllProducts] = useState(products)
  const [freshness, setFreshness] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [matching, setMatching] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Get freshness for first product
        const freshRes = await apiClient.getFreshness(1)
        setFreshness(freshRes)

        // Get price prediction for Cabai rawit
        const predRes = await apiClient.getPricePrediction('Cabai rawit')
        setPrediction(predRes)

        // Get matching products for user 1
        const matchRes = await apiClient.getMatching(1)
        setMatching(matchRes)

        // Transform backend data to match UI format
        if (matchRes && matchRes.length > 0) {
          const transformed = matchRes.map((item) => ({
            id: item.produk_id,
            name: item.nama_produk,
            farmer: 'Petani', // Backend doesn't provide farmer name
            location: 'Indonesia',
            distance: `${item.jarak_km} km`,
            quantity: 100, // Fallback value
            unit: 'kg',
            harvestAge: 0,
            freshness: 70, // Fallback
            price: 20000,
            marketPrice: 25000,
            status: item.alasan,
            discount: 0,
            note: item.alasan,
            image: '🥬',
            trend: [20000, 21000, 22000, 23000, 24000, 25000],
          }))
          setAllProducts(transformed)
        }
      } catch (err) {
        console.error('API Error:', err)
        setError(err.message)
        // Keep using dummy data if API fails
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const filteredProducts = useMemo(() => {
    let items = allProducts.filter((product) => {
      const q = search.toLowerCase().trim()
      return !q || product.name.toLowerCase().includes(q) || product.farmer.toLowerCase().includes(q)
    })

    if (sortBy === 'terdekat') {
      items = [...items].sort((a, b) => Number.parseFloat(a.distance) - Number.parseFloat(b.distance))
    }
    if (sortBy === 'paling segar') {
      items = [...items].sort((a, b) => b.freshness - a.freshness)
    }
    if (sortBy === 'harga termurah') {
      items = [...items].sort((a, b) => a.price - b.price)
    }

    return items
  }, [search, sortBy, allProducts])

  const topProduct = allProducts[0] || products[0]

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <div className="eyebrow">SegarChain</div>
          <h1>Rantai pasok pangan yang lebih adil</h1>
        </div>
        <button className="primary-btn">+ Tambah</button>
      </header>

      <nav className="tab-bar" aria-label="Navigasi utama">
        <button className={tab === 'farmer' ? 'active' : ''} onClick={() => setTab('farmer')}>Petani</button>
        <button className={tab === 'market' ? 'active' : ''} onClick={() => setTab('market')}>Pasar</button>
        <button className={tab === 'alerts' ? 'active' : ''} onClick={() => setTab('alerts')}>Notifikasi</button>
        <button className={tab === 'trace' ? 'active' : ''} onClick={() => setTab('trace')}>Jejak</button>
      </nav>

      {tab === 'farmer' && (
        <main className="screen farmer-screen">
          <section className="hero-card card">
            <div>
              <p className="greeting">Selamat pagi, Pak Budi</p>
              <h2>Hasil panenmu siap masuk pasar.</h2>
            </div>
            <span className="badge badge-green">AI aktif</span>
          </section>

          <section className="stock-card card">
            <div className="card-header">
              <div>
                <p className="label">Stok aktif</p>
                <h3>{topProduct.name}</h3>
              </div>
              <span className="weight">{topProduct.quantity} {topProduct.unit}</span>
            </div>

            <div className="mini-product-row">
              <div className="emoji-wrap">{topProduct.image}</div>
              <div className="mini-info">
                <strong>{topProduct.farmer}</strong>
                <span>{topProduct.location}</span>
              </div>
              <div className="price-box">{formatPrice(topProduct.price)}</div>
            </div>

            <FreshnessMeter value={freshness ? freshness.skor : topProduct.freshness} />
            <p className="ai-note">{freshness ? freshness.penjelasan : topProduct.note}</p>
          </section>

          <section className="price-card card">
            <div className="card-header">
              <div>
                <p className="label">Prediksi harga hari ini</p>
                <h3>{prediction ? formatPrice(prediction.harga_rekomendasi) : formatPrice(topProduct.marketPrice)}</h3>
              </div>
              <span className="badge badge-soft">{prediction && prediction.tren === 'naik' ? '+' : '-'}5.2%</span>
            </div>
            <Sparkline points={prediction ? prediction.data_7_hari : topProduct.trend} />
            <div className="trend-meta">
              <span>6 hari lalu</span>
              <span>Hari ini</span>
            </div>
            {prediction && <p className="ai-note" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>{prediction.penjelasan}</p>}
          </section>

          <section className="add-form card">
            <div className="card-header">
              <div>
                <p className="label">Tambah hasil panen</p>
                <h3>Form cepat</h3>
              </div>
            </div>
            <div className="input-grid">
              <div className="field">
                <label>Jenis produk</label>
                <select defaultValue="Cabai rawit">
                  {productCategories.map((name) => (
                    <option key={name} value={name}>{name}</option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label>Jumlah</label>
                <input defaultValue="48 kg" />
              </div>
              <div className="field wide">
                <label>Tanggal panen</label>
                <input type="date" defaultValue="2026-08-17" />
              </div>
            </div>
            <button className="primary-btn wide-btn">+ Tambah Hasil Panen</button>
          </section>
        </main>
      )}

      {tab === 'market' && (
        <main className="screen market-screen">
          <section className="market-header">
            <div>
              <p className="label">Pasar Segar</p>
              <h2>Produk paling cepat laku</h2>
            </div>
          </section>

          <div className="search-row">
            <input
              type="text"
              placeholder="Cari produk atau petani"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="sort-row">
            <button className={sortBy === 'terdekat' ? 'chip active' : 'chip'} onClick={() => setSortBy('terdekat')}>Terdekat</button>
            <button className={sortBy === 'paling segar' ? 'chip active' : 'chip'} onClick={() => setSortBy('paling segar')}>Paling Segar</button>
            <button className={sortBy === 'harga termurah' ? 'chip active' : 'chip'} onClick={() => setSortBy('harga termurah')}>Harga Termurah</button>
          </div>

          <div className="product-list">
            {filteredProducts.map((item) => (
              <article key={item.id} className="product-card card">
                <div className="thumb">{item.image}</div>
                <div className="product-main">
                  <div className="product-topline">
                    <div>
                      <h3>{item.name}</h3>
                      <p>{item.farmer} • {item.location}</p>
                    </div>
                    <span className="distance">{item.distance}</span>
                  </div>

                  <FreshnessMeter value={item.freshness} compact />

                  <div className="product-footer">
                    <div>
                      <strong>{formatPrice(item.price)}</strong>
                      <span>{item.quantity} {item.unit}</span>
                    </div>
                    <span className={`status-pill ${item.discount ? 'urgent' : 'safe'}`}>
                      {item.discount ? (item.discount >= 25 ? 'Risiko tinggi' : item.status) : item.status}
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </main>
      )}

      {tab === 'alerts' && (
        <main className="screen alerts-screen">
          <section className="market-header">
            <div>
              <p className="label">Notifikasi Pintar</p>
              <h2>Update pasar hari ini</h2>
            </div>
          </section>

          <div className="notification-list">
            {notifications.map((note) => (
              <div key={note.id} className="notification-item card">
                <span className="notif-dot" style={{ background: note.dot }} />
                <div>
                  <p>{note.text}</p>
                  <small>{note.time}</small>
                </div>
              </div>
            ))}
          </div>
        </main>
      )}

      {tab === 'trace' && (
        <main className="screen trace-screen">
          <section className="market-header">
            <div>
              <p className="label">Jejak Transparansi</p>
              <h2>Nilai yang sampai ke semua pihak</h2>
            </div>
          </section>

          <div className="trace-card card">
            <div className="trace-flow">
              {traceNodes.map((node) => (
                <div key={node.label} className="trace-node">
                  <div className="trace-circle" />
                  <div>
                    <small>{node.label}</small>
                    <strong>{node.value}</strong>
                  </div>
                </div>
              ))}
            </div>

            <div className="value-bars">
              {traceNodes.map((node) => (
                <div key={node.label} className="value-bar-wrap">
                  <div className="value-bar-label">
                    <span>{node.label}</span>
                    <strong>{node.share}%</strong>
                  </div>
                  <div className="value-bar-track">
                    <div className="value-bar-fill" style={{ width: `${node.share}%` }} />
                  </div>
                </div>
              ))}
            </div>

            <p className="insight">Petani menerima <strong>57%</strong> dari harga akhir, mencerminkan distribusi yang lebih adil di rantai pasok.</p>
            <button className="primary-btn wide-btn">Lihat Riwayat Lengkap</button>
          </div>
        </main>
      )}
    </div>
  )
}

export default App
