from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Categoria, Produto

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Página inicial
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    produtos = db.query(Produto).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "categorias": categorias,
            "produtos": produtos
        }
    )


# Criar categoria
@app.post("/categorias")
def criar_categoria(
    nome: str = Form(...),
    descricao: str = Form(None),
    status: bool = Form(False),
    db: Session = Depends(get_db)
):
    nova = Categoria(
        nome=nome,
        descricao=descricao,
        status=status
    )
    db.add(nova)
    db.commit()

    return RedirectResponse(url="/", status_code=303)


# Criar produto
@app.post("/produtos")
def criar_produto(
    nome: str = Form(...),
    preco: float = Form(...),
    estoque: int = Form(...),
    categoria_id: int = Form(...),
    db: Session = Depends(get_db)
):
    novo = Produto(
        nome=nome,
        preco=preco,
        estoque=estoque,
        categoria_id=categoria_id
    )
    db.add(novo)
    db.commit()

    return RedirectResponse(url="/", status_code=303)


# Excluir produto
@app.post("/produtos/{produto_id}/delete")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):

    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if produto:
        db.delete(produto)
        db.commit()

    return RedirectResponse(url="/", status_code=303)