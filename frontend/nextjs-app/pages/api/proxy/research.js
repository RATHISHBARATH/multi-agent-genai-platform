import axios from 'axios'
export default async function handler(req, res) {
  const token = req.headers.authorization || ''
  try {
    const apiRes = await axios.post(process.env.NEXT_PUBLIC_BACKEND_URL + '/ingest/papers', req.body, {
      headers: { Authorization: token, 'Content-Type': 'application/json' }
    })
    res.status(200).json(apiRes.data)
  } catch (err) {
    res.status(500).json({ error: err.message })
  }
}