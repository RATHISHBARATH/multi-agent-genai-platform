
def fake_hash_password(pw: str) -> str:
    # placeholder hashing for demo only
    if pw == "secret":
        return "hashed-secret"
    return "hashed-" + pw
