from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse # Requisição html
from fastapi.templating import Jinja2Templates # Para renderizar os templates
from pathlib import Path # Manipular caminhos dos arquivos 
from fastapi.staticfiles import StaticFiles 
import fonte # Còdigo Fonte

fonte.DatabaseManager()
# fonte.Produto.cadastrar_produto()


app = FastAPI()
templates = Jinja2Templates(directory="static")

@app.get("/",response_class=HTMLResponse)


async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})