import json

import aiohttp
from fastapi import Request
from fastapi.routing import APIRouter
from utils.response import handleResponse
from utils import log

router = APIRouter()
logger = log.createLogger("SearchAPI")

KW_SEARCH = "http://search.kuwo.cn/r.s"
KG_SEARCH = "http://songsearch.kugou.com/song_search_v2?keyword={keyword}&page={page}&pagesize={limit}&platform=WebFilter"
TX_SEARCH = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?w={keyword}&format=json&p={page}&n={limit}"

# Public LX Music API for KuWo URL (works without login)
RENDER_API = "https://lxmusicapi.onrender.com/url/kw/{songId}/{quality}"


@router.get("/search")
async def handleSearch(
    request: Request,
    source: str,
    keyword: str,
    page: int = 1,
    limit: int = 20
):
    try:
        if source == "kg":
            return await _search_kg(keyword, page, limit)
        elif source == "tx":
            return await _search_tx(keyword, page, limit)
        elif source == "kw":
            return await _search_kw(keyword, page, limit)
        else:
            return handleResponse(
                request, {"code": 400, "message": f"不支持的搜索源: {source}"}
            )
    except Exception as e:
        logger.error(f"搜索失败 [{source}] {keyword}: {e}")
        return handleResponse(
            request, {"code": 500, "message": f"搜索失败: {e}"}
        )


@router.get("/url/public")
async def handlePublicUrl(
    request: Request,
    source: str,
    songId: str,
    quality: str = "128k"
):
    """Proxy to public LX Music API (render.com) for platforms that don't need login."""
    try:
        if source == "kw":
            url = RENDER_API.format(songId=songId, quality=quality)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=10),
                    headers={"X-Request-Key": "share-v3"}
                ) as resp:
                    data = await resp.json()

            play_url = data.get("url", "")
            if play_url:
                return {"code": 200, "message": "成功", "url": play_url}
            else:
                return {"code": 500, "message": data.get("msg", "无法获取播放链接")}
        else:
            return handleResponse(
                request, {"code": 400, "message": f"不支持的源: {source}"}
            )
    except Exception as e:
        logger.error(f"Public URL failed [{source}] {songId}: {e}")
        return handleResponse(
            request, {"code": 500, "message": f"获取链接失败: {e}"}
        )


async def _search_kg(keyword: str, page: int, limit: int):
    url = KG_SEARCH.format(keyword=keyword, page=page, limit=limit)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                text = await resp.text()
                data = json.loads(text)
    except Exception:
        return await _search_kw(keyword, page, limit)

    songs = data.get("data", {}).get("lists", [])
    results = []
    for s in songs:
        dur = int(s.get("Duration", 0) or 0)
        if dur <= 45:
            continue
        results.append({
            "id": s.get("FileHash") or s.get("SQFileHash") or s.get("HQFileHash") or "",
            "name": s.get("SongName", ""),
            "artist": s.get("SingerName", ""),
            "duration": dur,
            "source": "kg",
        })
    return {"code": 200, "message": "成功", "data": results}


async def _search_tx(keyword: str, page: int, limit: int):
    url = TX_SEARCH.format(keyword=keyword, page=page, limit=limit)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=8),
            headers={"Referer": "https://y.qq.com/"}
        ) as resp:
            text = await resp.text()
            data = json.loads(text)

    songs = data.get("data", {}).get("song", {}).get("list", [])
    results = []
    for s in songs:
        dur = s.get("interval", 0)
        if dur <= 45:
            continue
        results.append({
            "id": s.get("songmid") or s.get("mid", ""),
            "name": s.get("songname") or s.get("name", ""),
            "artist": "/".join([si.get("name", "") for si in s.get("singer", [])]),
            "duration": int(dur),
            "source": "tx",
        })
    return {"code": 200, "message": "成功", "data": results}


async def _search_kw(keyword: str, page: int, limit: int):
    params = {
        "client": "kt",
        "all": keyword,
        "pn": page - 1,
        "rn": limit,
        "uid": "2574109560",
        "ver": "kwplayer_ar_8.5.4.2",
        "vipver": "1",
        "ft": "music",
        "cluster": "0",
        "strategy": "2012",
        "encoding": "utf8",
        "rformat": "json",
        "vermerge": "1",
        "mobi": "1",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            KW_SEARCH,
            params=params,
            timeout=aiohttp.ClientTimeout(total=8),
            headers={"Referer": "http://www.kuwo.cn/"}
        ) as resp:
            text = await resp.text()
            data = json.loads(text)

    songs = data.get("abslist", [])
    results = []
    for s in songs:
        dur = int(s.get("DURATION", 0) or 0)
        if dur <= 45:
            continue
        rid = (s.get("MUSICRID") or "").replace("MUSIC_", "")
        results.append({
            "id": rid,
            "name": s.get("NAME", ""),
            "artist": s.get("ARTIST", ""),
            "duration": dur,
            "source": "kw",
        })
    return {"code": 200, "message": "成功", "data": results}
