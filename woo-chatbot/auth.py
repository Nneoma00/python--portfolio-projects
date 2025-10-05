"""
This is where i write the code for authentication and rate limiting
"""
from http.client import HTTPException
import time

GLOBAL_RATE_LIMIT= 3
GLOBAL_RATE_LIMIT_SECONDS = 60


def apply_limit(user_id: str):
    current_time = time.time()
    rate_limit = GLOBAL_RATE_LIMIT
    time_window = GLOBAL_TIME_WINDOW_SECONDS


    #Filter out requests older than the global time window
    user_requests[user_id] = [
        t for t in user_requests[user_id] if t > current_time - time_window
    ]

    if len(user_requests[user_id]) >= rate_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )

    user_requests[user_id].append(current_time)
    return True