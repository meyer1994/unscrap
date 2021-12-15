from io import BytesIO
from dataclasses import dataclass

from fastapi import FastAPI, Depends
from pydantic import conint
from starlette.responses import StreamingResponse
from playwright.async_api import async_playwright


app = FastAPI()

browser = None
playwright = None


@app.on_event('startup')
async def startup():
    global browser, playwright
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch()


@app.on_event('shutdown')
async def shutdown():
    await browser.close()
    await playwright.stop()


@dataclass
class Req:
    url: str
    width: conint(gt=100, le=1920) = 1920
    height: conint(gt=100, le=1920) = 1080

    @property
    def size(self) -> dict:
        return {'width': self.width, 'height': self.height}


@app.get('/')
async def get(req: Req = Depends(Req)) -> StreamingResponse:
    page = await browser.new_page()
    await page.set_viewport_size(req.size)
    await page.goto(req.url)
    buff = await page.screenshot(full_page=True)
    buff = BytesIO(buff)
    await page.close()
    return StreamingResponse(buff, media_type='image/png')
