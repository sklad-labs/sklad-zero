import asyncio
import json
import httpx
import base64
import hashlib
from Crypto.Cipher import AES

API_URL = "https://api.allanime.day/api"
ANIME_ID = "wm2zBXuqhdKM7L7AL"
EPISODE = "1"
TRANSLATION = "sub"
HASH = "d405d0edd690624b66baba3068e0edc3ac90f1597d898a1ec8db4e5c43c00fec"


def decrypt_tobeparsed(tobeparsed: str) -> dict:
    padding = (4 - len(tobeparsed) % 4) % 4
    raw = base64.b64decode(tobeparsed + "=" * padding)
    key = hashlib.sha256(b"Xot36i3lK3:v1").digest()
    nonce = raw[1:13]
    ctr_iv = bytes.fromhex(nonce.hex() + "00000002")
    ct_len = len(raw) - 13 - 16
    plaintext = AES.new(key, AES.MODE_CTR, initial_value=ctr_iv, nonce=b"").decrypt(raw[13: 13 + ct_len])
    return json.loads(plaintext)


def decode_xor(hex_str: str) -> str:
    return bytes([int(hex_str[i:i+2], 16) ^ 56 for i in range(0, len(hex_str), 2)]).decode("utf-8", errors="ignore")


async def main():
    params = {
        "variables": json.dumps({"showId": ANIME_ID, "translationType": TRANSLATION, "episodeString": EPISODE}, separators=(",", ":")),
        "extensions": json.dumps({"persistedQuery": {"version": 1, "sha256Hash": HASH}}, separators=(",", ":")),
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://youtu-chan.com",
        "Origin": "https://youtu-chan.com",
    }

    async with httpx.AsyncClient(headers=headers, timeout=15) as client:
        r = await client.get(API_URL, params=params)
        data = r.json()

    tobeparsed = data.get("data", {}).get("tobeparsed")
    if tobeparsed:
        data = {"data": decrypt_tobeparsed(tobeparsed)}

    episode = data.get("data", {}).get("episode") or {}
    sources = episode.get("sourceUrls") or []

    print(f"Ukupno izvora: {len(sources)}\n")
    for s in sources:
        name = s.get("sourceName", "???")
        url = s.get("sourceUrl", "")
        if url.startswith("--"):
            url = decode_xor(url[2:])
        print(f"  name={name!r:20}  url={url[:80]}")


async def resolve_clock(path: str) -> str | None:
    json_path = path.replace("clock", "clock.json")
    url = f"https://api.allanime.day{json_path}"
    async with httpx.AsyncClient(headers={"Referer": "https://allmanga.to/"}, timeout=10) as client:
        r = await client.get(url)
        print(f"  clock.json status={r.status_code} body={r.text[:300]}")
        if r.status_code != 200:
            return None
        data = r.json()
    links = data.get("links") or []
    if not links:
        return None
    link = links[0]
    if isinstance(link, dict):
        return link.get("link") or link.get("src") or link.get("url")
    return link if isinstance(link, str) else None


async def main_resolved():
    params = {
        "variables": json.dumps({"showId": ANIME_ID, "translationType": TRANSLATION, "episodeString": EPISODE}, separators=(",", ":")),
        "extensions": json.dumps({"persistedQuery": {"version": 1, "sha256Hash": HASH}}, separators=(",", ":")),
    }
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://youtu-chan.com", "Origin": "https://youtu-chan.com"}

    async with httpx.AsyncClient(headers=headers, timeout=15) as client:
        r = await client.get(API_URL, params=params)
        data = r.json()

    tobeparsed = data.get("data", {}).get("tobeparsed")
    if tobeparsed:
        data = {"data": decrypt_tobeparsed(tobeparsed)}

    episode = data.get("data", {}).get("episode") or {}
    sources = episode.get("sourceUrls") or []

    print("\n=== Clock URL resolution ===\n")
    for s in sources:
        name = s.get("sourceName", "???")
        url = s.get("sourceUrl", "")
        if url.startswith("--"):
            url = decode_xor(url[2:])
        if url.startswith("/apivtwo/clock"):
            print(f"[{name}] clock URL: {url}")
            resolved = await resolve_clock(url)
            print(f"  → resolved: {resolved}\n")
        else:
            print(f"[{name}] direct URL: {url[:80]}\n")


asyncio.run(main())
asyncio.run(main_resolved())
