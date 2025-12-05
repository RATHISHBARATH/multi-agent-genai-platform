import { useEffect, useState } from 'react'
import axios from 'axios'
import Router from 'next/router'

export default function Dashboard() {
  const [user, setUser] = useState(null)
  const [q, setQ] = useState('graph neural networks')
  const [res, setRes] = useState(null)

  useEffect(()=>{
    const token = localStorage.getItem('token')
    if (!token) Router.push('/login')
    else {
      axios.get(process.env.NEXT_PUBLIC_BACKEND_URL + '/auth/me', { headers: { Authorization: 'Bearer ' + token } })
        .then(r=>setUser(r.data.username))
        .catch(()=>Router.push('/login'))
    }
  },[])

  async function run() {
    const token = localStorage.getItem('token')
    const r = await axios.post('/api/proxy/research', { q }, { headers: { Authorization: 'Bearer ' + token } })
    setRes(r.data)
  }

  return (<div style={{padding:20}}>
    <h1>Dashboard</h1>
    <div>Welcome: {user}</div>
    <div>
      <input value={q} onChange={e=>setQ(e.target.value)} style={{width:'60%'}} />
      <button onClick={run}>Run Ingest</button>
    </div>
    <pre>{res ? JSON.stringify(res, null, 2) : 'No results'}</pre>
  </div>)
}