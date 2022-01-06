from io import BytesIO
from dataclasses import dataclass

from fastapi import FastAPI, Depends
from pydantic import conint
from starlette.responses import StreamingResponse, HTMLResponse
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
class Click:
    x: conint(gt=0, le=1920) = None
    y: conint(gt=0, le=1920) = None

    @property
    def clickable(self) -> bool:
        return None not in (self.x, self.y)

    @property
    def position(self) -> dict:
        return {'x': self.x, 'y': self.y}


@dataclass
class Page:
    id: str
    url: str
    width: conint(gt=100, le=1920) = 1920
    height: conint(gt=100, le=1920) = 1080

    @property
    def size(self) -> dict:
        return {'width': self.width, 'height': self.height}


@dataclass
class Ctx:
    id: str
    page: Page = Depends(Page)
    click: Click = Depends(Click)


SESSIONS = {}


@app.get('/image')
async def get(ctx: Ctx = Depends(Ctx)):
    if ctx.id in SESSIONS:
        tab = SESSIONS[ctx.id]
    else:
        tab = await browser.new_page()
        await tab.goto(ctx.page.url)
        SESSIONS[ctx.id] = tab

    await tab.set_viewport_size(ctx.page.size)

    if ctx.click.clickable:
        await tab.click('html', position=ctx.click.position)

    buff = await tab.screenshot(type='jpeg', quality=50)
    buff = BytesIO(buff)
    return StreamingResponse(buff, media_type='image/jpeg')


@app.get('/', response_class=HTMLResponse)
async def index() -> str:
    with open('index.html', 'rt') as f:
        return f.read()
