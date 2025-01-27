from collections import defaultdict
from functools import wraps
from time import time
from typing import Dict, Tuple

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    def __init__(self):
        # Dictionary to store request counts and timestamps
        # Format: {key: (request_count, window_start_time)}
        self.requests: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, time()))

    def _get_rate_limit_key(self, request: Request) -> str:
        """Generate a unique key for rate limiting based on IP or user ID"""
        # If user is authenticated, use their ID
        if hasattr(request.state, "user"):
            return f"rate_limit:user:{request.state.user.id}"
        # Otherwise use IP address
        return f"rate_limit:ip:{request.client.host}"

    def is_rate_limited(
        self, request: Request, limit: int = 100, window: int = 60
    ) -> bool:
        """
        Check if the request should be rate limited

        Args:
            request: FastAPI request object
            limit: Maximum number of requests allowed in the window
            window: Time window in seconds
        """
        key = self._get_rate_limit_key(request)
        current_time = time()

        # Get current count and window start time
        count, window_start = self.requests[key]

        # If window has expired, reset counter
        if current_time - window_start > window:
            count = 0
            window_start = current_time

        # Check if limit is exceeded
        if count >= limit:
            return True

        # Update counter
        self.requests[key] = (count + 1, window_start)
        return False


def rate_limit(limit: int = 100, window: int = 60):
    """
    Rate limiting decorator for FastAPI endpoints

    Args:
        limit: Maximum number of requests allowed in the window
        window: Time window in seconds
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            limiter = request.state.rate_limiter

            if limiter.is_rate_limited(request, limit, window):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Too many requests",
                        "limit": limit,
                        "window_seconds": window,
                        "retry_after": window,
                    },
                )

            return func(request=request, *args, **kwargs)

        return wrapper

    return decorator


# Example usage:
"""
@router.post("/games/{game_id}/state")
@rate_limit(limit=60, window=60)  # 60 заявки в минута (1 в секунда)
def update_game_state():
    ...
    
@router.get("/games")
@rate_limit(limit=100, window=60)  # 100 заявки в минута
def get_games():
    ...

@router.get("/users/me")
@rate_limit(limit=30, window=60)  # 30 заявки в минута
def get_profile():
    ...
"""
