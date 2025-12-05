import os, time, requests, pytest

BACKEND = os.getenv('BACKEND_URL', 'http://localhost:8000')
TIMEOUT = int(os.getenv('E2E_TIMEOUT', '120'))

def wait_for_status(task_id, timeout=TIMEOUT):
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f"{BACKEND}/agents/task_status/{task_id}")
        if r.status_code == 200:
            data = r.json()
            status = data.get('status') or data.get('status', 'unknown')
            if status and status != 'running' and status != 'pending':
                return data
        time.sleep(2)
    return None

def test_celery_research_pipeline():
    # Start research task via API
    r = requests.post(f"{BACKEND}/agents/start_research", json={'q': 'graph neural networks'})
    assert r.status_code == 200
    job = r.json().get('task_id')
    assert job
    # Poll for completion
    res = wait_for_status(job, timeout=TIMEOUT)
    assert res is not None, "Task did not complete in time"
    assert res.get('status') == 'success', f"Task failed: {res}"
    assert 'result' in res or 'ppt' in res or 'video' in res
