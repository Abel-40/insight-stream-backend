from fastapi import FastAPI,HTTPException,Request
from app.api.v1 import users,auth,topic
from fastapi.exceptions import RequestValidationError
from .utils.response import error_response
app = FastAPI()


app.include_router(router=topic.router,prefix="/insight")
app.include_router(router=auth.router, prefix="/insight")


@app.exception_handler(HTTPException)
def http_exception_handler(request:Request,exc:HTTPException):
  return error_response(status_code=exc.status_code,message=exc.detail)

@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    field_errors = {}
    for err in exc.errors():
        location = err["loc"][-1]
        field = str(location) 
        
        field_errors.setdefault(field, []).append(err["msg"])
        
    return error_response(
        status_code=422, 
        message="Invalid request data", 
        errors=field_errors
    )

@app.exception_handler(Exception)
def general_exception_handler(request:Request,exc:Exception):
  return error_response(status_code=500,message="Something went wrong please try again later!!!")

