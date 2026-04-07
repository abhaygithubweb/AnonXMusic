# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import re
import aiohttp

from anony import logger
from anony.helpers import Track


class YouTube:
    def __init__(self):
        self.api_base = "https://musiker-seven.vercel.app/?search="
        self.base = "https://www.youtube.com/watch?v="

        # YouTube URL validator (optional use)
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )

    # ✅ Check valid YouTube URL
    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    # ✅ Search using YOUR API
    async def search(self, query: str, m_id: int, video: bool = False) -> Track | None:
        try:
            api_url = f"{self.api_base}{query}"

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    data = await resp.json()

            if data and data.get("results"):
                item = data["results"][0]

                return Track(
                    id=item.get("download_url"),  # using download URL as ID
                    channel_name=item.get("performer"),
                    duration="",
                    duration_sec=0,
                    message_id=m_id,
                    title=item.get("title", "")[:25],
                    thumbnail=item.get("thumb_url"),
                    url=item.get("download_url"),
                    view_count="",
                    video=video,
                )

        except Exception as e:
            logger.warning(f"Search API failed: {e}")

        return None

    # ✅ Multiple results (useful for inline buttons / list UI)
    async def search_many(self, query: str, limit: int = 5) -> list[Track]:
        results_list = []

        try:
            api_url = f"{self.api_base}{query}"

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    data = await resp.json()

            if data and data.get("results"):
                for item in data["results"][:limit]:
                    track = Track(
                        id=item.get("download_url"),
                        channel_name=item.get("performer"),
                        duration="",
                        duration_sec=0,
                        message_id=0,
                        title=item.get("title", "")[:25],
                        thumbnail=item.get("thumb_url"),
                        url=item.get("download_url"),
                        view_count="",
                        video=False,
                    )
                    results_list.append(track)

        except Exception as e:
            logger.warning(f"Search_many API failed: {e}")

        return results_list

    # ✅ Download (returns direct audio URL from API)
    async def download(self, query: str, video: bool = False) -> str | None:
        try:
            api_url = f"{self.api_base}{query}"

            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    data = await resp.json()

            if not data.get("results"):
                return None

            result = data["results"][0]

            # Direct audio/video link from your API
            return result.get("download_url")

        except Exception as e:
            logger.warning(f"Download API failed: {e}")
            return None
