
import axios from 'axios'

export default async function handler(req, res) {
  try {
    const apiRes = await axios.post(process.env.BACKEND_URL + '/research/summarize', req.body, {
      headers: { 'Content-Type': 'application/json' }
    })
    res.status(200).json(apiRes.data)
  } catch (err) {
    res.status(500).json({ error: err.message })
  }
}
