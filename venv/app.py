from fastapi import FastAPI
# from routing_async import router
from routing import router
import uvicorn
from memory_profiling import PyInstrumentMiddleware
from security_headers import SecurityHeadersMiddleware

app = FastAPI()

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(PyInstrumentMiddleware)

# Include routing
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
