from pyinstrument import Profiler
from starlette.middleware.base import BaseHTTPMiddleware

class PyInstrumentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        profiler = Profiler()
        profiler.start()

        # Proceed with the request
        response = await call_next(request)

        profiler.stop()

       # Save profiler results into a human-readable HTML file
        endpoint = request.url.path.replace('/', '_')
        with open(f"memory_profile_{endpoint}.html", "w") as f:
            f.write(profiler.output_html())

        return response
