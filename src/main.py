import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.bot import Bot

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')

templates = Jinja2Templates(directory='src/templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'test': False})


@app.get('/test', response_class=HTMLResponse)
async def test_index(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'test': True})


class Predict(BaseModel):
    board: str
    test: bool


def create_bot(is_testing: bool):
    if is_testing:
        return Bot(strategy='fixed')
    else:
        return Bot(strategy='mcts')


@app.post('/predict')
async def predict(predict: Predict):
    bot = create_bot(predict.test)
    prediction = bot.predict(predict.board)
    return {'move': prediction}
