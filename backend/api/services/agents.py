"""Async multi-agent implementations: SearchAgent, SummarizerAgent, MediaAgent, IngestAgent."""
import logging, asyncio
from .paper_retriever import search as paper_search
from .llm import LLMModel
from .embeddings import Embeddings
from .vector_pinecone import PineconeClient
from .ppt_creator import create_pptx
from .video_gen import generate_video_from_slides

logger = logging.getLogger('autoscillab.agents')

class SearchAgent:
    def __init__(self):
        pass
    async def run(self, query, top_k=5):
        return await paper_search(query, top_k=top_k)

class SummarizerAgent:
    def __init__(self):
        self.llm = LLMModel()
    async def run(self, text):
        prompt = f"Summarize the following text in 3 concise bullet points:\n\n{text[:3000]}"
        loop = asyncio.get_event_loop()
        # LLMModel.chat is sync (HTTP); run in threadpool to avoid blocking
        resp = await loop.run_in_executor(None, self.llm.chat, prompt)
        return resp

class MediaAgent:
    def __init__(self):
        pass
    async def create_ppt(self, title, slides):
        loop = asyncio.get_event_loop()
        path = await loop.run_in_executor(None, create_pptx, title, slides)
        return path
    async def create_video(self, slides):
        loop = asyncio.get_event_loop()
        path = await loop.run_in_executor(None, generate_video_from_slides, slides)
        return path

class IngestAgent:
    def __init__(self):
        self.embedder = Embeddings()
        self.vdb = PineconeClient()
    async def index(self, text, meta=None):
        loop = asyncio.get_event_loop()
        vec = await loop.run_in_executor(None, self.embedder.embed, text)
        # upsert may be blocking; run in executor
        vid = await loop.run_in_executor(None, self.vdb.upsert, None, vec, meta or {})
        return vid
