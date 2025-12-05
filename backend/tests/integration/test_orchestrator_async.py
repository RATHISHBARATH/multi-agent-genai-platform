import pytest, asyncio, os
from api.services.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_orchestrator_runs():
    orch = Orchestrator()
    res = await orch.run_research_pipeline('graph neural networks', user_meta={'test':True})
    assert 'summary' in res and 'papers' in res
