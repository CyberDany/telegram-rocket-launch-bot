import httpx
from urllib.parse import urljoin
from typing import List, NamedTuple, Text
import asyncio

class Video(NamedTuple):
    """
    Video structure from the API
    """

    name: Text
    width: int
    height: int
    frames: int
    frame_rate: List[int]
    url: Text
    first_frame: Text
    last_frame: Text

class VideoAPIClient:
    def __init__(self, api_base_url: Text):
        self.api_base_url = api_base_url.rstrip('/')
        self.client = httpx.AsyncClient()

    async def _make_request(self, endpoint: Text, retries: int = 3, backoff: float = 1.0):
        """
        Intenta realizar una solicitud GET a un endpoint con reintentos y backoff exponencial.
        """
        url = urljoin(self.api_base_url, endpoint)
        for attempt in range(retries):
            try:
                timeout = httpx.Timeout(10.0, connect=60.0)
                response = await self.client.get(url, timeout=timeout)
                response.raise_for_status()  # Levanta excepción si la respuesta tiene un código de error
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                if attempt < retries - 1:  # No esperar después del último intento
                    await asyncio.sleep(backoff * 2 ** attempt)  # Espera exponencial
                else:
                    raise e  # Levanta la excepción si se alcanza el máximo de reintentos


    async def get_video_list(self) -> List[Video]:
        video_list = await self._make_request("/api/video/")
        return [Video(**video_data) for video_data in video_list]

    async def get_video(self, video_name: Text) -> Video:
        video_list = await self.get_video_list()
        for video in video_list:
            if video.name == video_name:
                return video
        raise ValueError(f"Video {video_name} not found in the video list.")
    
    def get_frame_url(self, video_name: Text, frame_number: int) -> Text:
        return f"{self.api_base_url}/api/video/{video_name}/frame/{frame_number}/"

    async def get_frame(self, video_name: Text, frame_number: int) -> bytes:
        frame_url = self.get_frame_url(video_name, frame_number)
        response = await self.client.get(frame_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.content

    async def get_total_frames(self, video_name: Text) -> int:
        video_list = await self.get_video_list()
        for video in video_list:
            if video.name == video_name:
                return video.frames
        raise ValueError(f"Video {video_name} not found in the video list.")


