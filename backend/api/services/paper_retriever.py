"""Async paper retriever using Semantic Scholar + arXiv fallback.
Uses httpx async client and async cache.
"""
import os, time, logging, xml.etree.ElementTree as ET
from urllib.parse import urlencode
import httpx
from api.utils.cache import cache

logger = logging.getLogger('autoscillab.paper_retriever')
SEMANTIC_SCHOLAR_URL = 'https://api.semanticscholar.org/graph/v1/paper/search'
ARXIV_SEARCH_URL = 'http://export.arxiv.org/api/query'

async def _backoff_request(client, url, params=None, headers=None, method='get', max_retries=3):
    delay = 1.0
    for attempt in range(max_retries):
        try:
            if method == 'get':
                r = await client.get(url, params=params, headers=headers, timeout=10.0)
            else:
                r = await client.post(url, json=params, headers=headers, timeout=10.0)
            if r.status_code == 429:
                logger.warning('Rate limited, sleeping %s', delay)
                await asyncio.sleep(delay)
                delay *= 2
                continue
            r.raise_for_status()
            return r
        except httpx.HTTPStatusError as e:
            logger.exception('HTTP error: %s', e)
            raise
        except Exception as e:
            logger.exception('Request failed: %s', e)
            await asyncio.sleep(delay)
            delay *= 2
    raise RuntimeError('Max retries exceeded')

def _parse_semanticscholar_json(j):
    papers = []
    for item in j.get('data', []):
        papers.append({
            'title': item.get('title'),
            'abstract': item.get('abstract'),
            'url': 'https://www.semanticscholar.org/paper/' + item.get('paperId', '') if item.get('paperId') else item.get('url'),
            'pdf_url': None,
            'doi': item.get('externalIds', {}).get('DOI'),
            'year': item.get('year'),
            'authors': [a.get('name') for a in item.get('authors', [])[:5]]
        })
    return papers

def _parse_arxiv_xml(xml_text):
    root = ET.fromstring(xml_text)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        summary = entry.find('atom:summary', ns).text.strip()
        pdf = None
        for link in entry.findall('atom:link', ns):
            if link.get('type') == 'application/pdf':
                pdf = link.get('href')
        authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
        papers.append({
            'title': title,
            'abstract': summary,
            'url': entry.find('atom:id', ns).text,
            'pdf_url': pdf,
            'doi': None,
            'year': entry.find('atom:published', ns).text[:4] if entry.find('atom:published', ns) is not None else None,
            'authors': authors[:5]
        })
    return papers

async def search(query: str, top_k: int = 10):
    key = f"paper_search:{query.lower()}:{top_k}"
    try:
        cached = await cache.get(key)
        if cached:
            return cached
    except Exception:
        pass

    results = []
    async with httpx.AsyncClient() as client:
        try:
            params = {'query': query, 'limit': top_k, 'fields': 'title,abstract,authors,year,externalIds,url'}
            headers = {}
            ss_key = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
            if ss_key:
                headers['x-api-key'] = ss_key
            r = await _backoff_request(client, SEMANTIC_SCHOLAR_URL, params=params, headers=headers)
            j = r.json()
            results = _parse_semanticscholar_json(j)
        except Exception as e:
            logger.warning('Semantic Scholar failed: %s', e)

        if len(results) < top_k:
            try:
                arxiv_q = urlencode({'search_query': f'all:{query}', 'start': 0, 'max_results': top_k})
                r2 = await _backoff_request(client, ARXIV_SEARCH_URL, params=arxiv_q)
                papers = _parse_arxiv_xml(r2.text)
                seen = set(p['title'].lower() for p in results)
                for p in papers:
                    if p['title'].lower() not in seen:
                        results.append(p)
                        seen.add(p['title'].lower())
                        if len(results) >= top_k:
                            break
            except Exception as e:
                logger.warning('arXiv fallback failed: %s', e)
    try:
        await cache.set(key, results, ttl=3600)
    except Exception:
        pass
    return results
