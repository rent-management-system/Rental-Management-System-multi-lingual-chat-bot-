from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.clients:
            self.clients[client_ip] = []

        # Filter requests in the current window
        self.clients[client_ip] = [timestamp for timestamp in self.clients[client_ip] if current_time - timestamp < self.window_seconds]

        if len(self.clients[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")

        self.clients[client_ip].append(current_time)

        response = await call_next(request)
        return response
