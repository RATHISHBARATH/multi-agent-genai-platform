import axios from 'axios'
import { useState } from 'react'

export default function Research() {
  const [q, setQ] = useState('deep learning optimization')
  const [res, setRes] = useState(null)

  async function run() {
    const r = await axios.post('/api/proxy/research', { q })
    setRes(r.data)
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Research Ingest</h1>
      <input value={q} onChange={e=>setQ(e.target.value)} style={{ width: '60%' }} />
      <button onClick={run}>Ingest & Orchestrate</button>
      <pre>{res ? JSON.stringify(res, null, 2) : 'no result'}</pre>
    </div>
  )
}
