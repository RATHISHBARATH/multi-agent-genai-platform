import requests, os, sys, time
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

def test_root():
    r = requests.get(BACKEND + "/health/ping")
    print("root:", r.status_code, r.text)
    return r.status_code == 200

if __name__ == '__main__':
    ok = test_root()
    sys.exit(0 if ok else 1)
