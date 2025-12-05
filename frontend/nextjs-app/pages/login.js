import { useState } from 'react'
import axios from 'axios'
import Router from 'next/router'

export default function Login() {
  const [u, setU] = useState('admin')
  const [p, setP] = useState('secret')
  const [err, setErr] = useState(null)

  async function submit(e) {
    e.preventDefault()
    try {
      const form = new URLSearchParams()
      form.append('username', u)
      form.append('password', p)
      const res = await axios.post(process.env.NEXT_PUBLIC_BACKEND_URL + '/auth/token', form)
      localStorage.setItem('token', res.data.access_token)
      Router.push('/dashboard')
    } catch (e) {
      setErr(e.response?.data || e.message)
    }
  }

  return (<div style={{padding:20}}>
    <h1>Login</h1>
    <form onSubmit={submit}>
      <label>Username</label><br/>
      <input value={u} onChange={e=>setU(e.target.value)} /><br/>
      <label>Password</label><br/>
      <input type="password" value={p} onChange={e=>setP(e.target.value)} /><br/>
      <button type="submit">Login</button>
    </form>
    {err && <pre>{JSON.stringify(err)}</pre>}
  </div>)
}