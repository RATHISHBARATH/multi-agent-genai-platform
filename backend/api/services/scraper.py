"""Async web scraper using httpx.AsyncClient and BeautifulSoup.
Respects robots.txt (sync check) and caches results (async cache).
"""
import os, logging, asyncio, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser as robotparser
from api.utils.cache import cache
import httpx

logger = logging.getLogger('autoscillab.scraper')
HEADERS = {'User-Agent': os.getenv('SCRAPER_USER_AGENT', 'AutoSciLabBot/1.0 (+https://example.org)')}

def _can_fetch(url: str) -> bool:
    try:
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = robotparser.RobotFileParser()
        rp.set_url(base)
        rp.read()
        return rp.can_fetch(HEADERS['User-Agent'], url)
    except Exception as e:
        logger.warning('robots.txt check failed for %s: %s', url, e)
        return True

def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for s in soup(['script', 'style', 'noscript']):
        s.decompose()
    texts = [t.get_text(separator=' ', strip=True) for t in soup.find_all(['p', 'h1','h2','h3','li'])]
    return '\n'.join(t for t in texts if t)[:20000]

async def fetch(url: str, use_cache: bool = True, cache_ttl: int = 3600):
    key = f"scraper:{url}"
    if use_cache:
        try:
            cached = await cache.get(key)
            if cached:
                return cached
        except Exception:
            pass
    if not _can_fetch(url):
        return {'url': url, 'status': 'denied', 'title': None, 'content': None}
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10.0) as client:
            r = await client.get(url)
            r.raise_for_status()
            html = r.text
            title = BeautifulSoup(html, 'html.parser').title
            title = title.string if title else ''
            content = _extract_text(html)
            out = {'url': url, 'status': r.status_code, 'title': title, 'content': content}
            try:
                await cache.set(key, out, ttl=cache_ttl)
            except Exception:
                pass
            return out
    except Exception as e:
        logger.exception('fetch failed: %s', e)
        return {'url': url, 'status': 'error', 'title': None, 'content': None}

async def fetch_pdf(url: str):
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=20.0) as client:
            r = await client.get(url)
            r.raise_for_status()
            if 'application/pdf' in r.headers.get('Content-Type',''):
                return r.content
            return None
    except Exception as e:
        logger.exception('fetch_pdf failed: %s', e)
        return None
