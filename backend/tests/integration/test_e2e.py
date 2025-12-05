import os, time, requests, pytest, subprocess

BACKEND = os.getenv('BACKEND_URL', 'http://localhost:8000')

def wait_for(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            time.sleep(1)
    return False

def test_full_pipeline():
    # assume docker-compose up has been run (CI step)
    assert wait_for(BACKEND + "/health/ping", timeout=60)
    # create token
    r = requests.post(BACKEND + '/auth/token', data={'username':'admin','password':'secret'})
    assert r.status_code == 200
    token = r.json().get('access_token')
    assert token
    # ingest a sample query
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'q': 'graph neural networks optimization'}
    r2 = requests.post(BACKEND + '/ingest/papers', json=payload, headers=headers)
    assert r2.status_code == 200
    data = r2.json()
    assert 'results' in data
