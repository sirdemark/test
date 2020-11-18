from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from calculator import Calculator, CalculatorResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error_msg": exc.errors()})


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/calculate/", response_model=CalculatorResponse)
async def calculate(calculator: Calculator) -> CalculatorResponse:
    response = CalculatorResponse(
        price_per_good=calculator.price_per_good,
        number_of_goods=calculator.number_of_goods,
        state=calculator.state,
        result=calculator.execute()
    )
    return response

