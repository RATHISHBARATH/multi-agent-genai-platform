"""Async orchestrator using agents to perform research pipeline."""
import uuid, logging, asyncio
from .agents import SearchAgent, SummarizerAgent, IngestAgent, MediaAgent

logger = logging.getLogger('autoscillab.orchestrator_async')

class Orchestrator:
    def __init__(self):
        self.search = SearchAgent()
        self.summarizer = SummarizerAgent()
        self.ingest = IngestAgent()
        self.media = MediaAgent()

    async def run_research_pipeline(self, query, user_meta=None):
        papers = await self.search.run(query, top_k=5)
        text_blob = ''
        for p in papers:
            text_blob += (p.get('title','') + '. ' + (p.get('abstract') or '') )[:2000] + '\n'
        summary = await self.summarizer.run(text_blob)
        doc_id = uuid.uuid4().hex
        meta = {'source': 'orchestrator', 'query': query, 'user': user_meta}
        await self.ingest.index(summary, meta=meta)
        slides = [{'heading': f'Result {i+1}', 'content': (p.get('abstract') or '')[:800]} for i,p in enumerate(papers[:5])]
        ppt_path = await self.media.create_ppt(query, slides)
        video_path = await self.media.create_video([s['content'] for s in slides])
        return {'id': doc_id, 'summary': summary, 'ppt': ppt_path, 'video': video_path, 'papers': papers}
