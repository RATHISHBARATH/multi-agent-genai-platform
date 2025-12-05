"""Redis cache wrapper with TTL and in-memory fallback.

Usage:
    from api.utils.cache import cache
    await cache.set('key', 'value', ttl=3600)
    v = await cache.get('key')
""""

import os, json, logging, asyncio
logger = logging.getLogger("autoscillab.cache")

try:
    import aioredis
    REDIS_AVAILABLE = True
except Exception:
    REDIS_AVAILABLE = False

class InMemoryCache:
    def __init__(self):
        self.store = {}
        self.loop = asyncio.get_event_loop()

    async def get(self, key):
        item = self.store.get(key)
        if not item: return None
        val, expiry = item
        if expiry and expiry < self.loop.time():
            del self.store[key]
            return None
        return val

    async def set(self, key, value, ttl: int = None):
        expiry = None
        if ttl:
            expiry = self.loop.time() + ttl
        self.store[key] = (value, expiry)
        return True

    async def delete(self, key):
        return self.store.pop(key, None) is not None

class RedisCache:
    def __init__(self, url):
        self.url = url
        self._conn = None

    async def _get_conn(self):
        if self._conn: return self._conn
        self._conn = await aioredis.from_url(self.url, decode_responses=True)
        return self._conn

    async def get(self, key):
        conn = await self._get_conn()
        v = await conn.get(key)
        return json.loads(v) if v else None

    async def set(self, key, value, ttl: int = None):
        conn = await self._get_conn()
        v = json.dumps(value)
        if ttl:
            await conn.set(key, v, ex=ttl)
        else:
            await conn.set(key, v)
        return True

    async def delete(self, key):
        conn = await self._get_conn()
        return await conn.delete(key)

# instantiate
_cache_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
if REDIS_AVAILABLE:
    cache = RedisCache(_cache_url)
else:
    logger.warning('aioredis not installed or not available; using in-memory cache fallback.')
    cache = InMemoryCache()
