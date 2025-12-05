
import Head from 'next/head'
import axios from 'axios'
import { useState } from 'react'

export default function Home() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)

  async function handleSummarize() {
    try {
      const res = await axios.post('/api/proxy/summarize', { title: 'demo', text })
      setResult(res.data)
    } catch (e) {
      setResult({ error: e.message })
    }
  }

  return (
    <div style={{ padding: 24, fontFamily: 'Inter, sans-serif' }}>
      <Head>
        <title>AutoSciLab Ultra</title>
      </Head>
      <h1>AutoSciLab Ultra — Demo Frontend</h1>
      <textarea rows={8} cols={80} placeholder="Paste research text..." value={text} onChange={e => setText(e.target.value)} />
      <br />
      <button onClick={handleSummarize}>Summarize (via proxy)</button>
      <pre>{result ? JSON.stringify(result, null, 2) : 'no results yet'}</pre>
    </div>
  )
}
