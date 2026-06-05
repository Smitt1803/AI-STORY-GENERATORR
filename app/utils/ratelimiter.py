import time
from collections import deque

class RateLimiter:
    """Simple rate limiter to prevent API abuse"""
    
    def __init__(self, requests_per_minute=60, window_size=60):
        self.requests_per_minute = requests_per_minute
        self.window_size = window_size  # in seconds
        self.requests = deque()
    
    def allow_request(self):
        """Check if the request is allowed under the current rate limit"""
        current_time = time.time()
        
        # Remove requests older than the window size
        while self.requests and self.requests[0] < current_time - self.window_size:
            self.requests.popleft()
        
        # Check if we're under the limit
        if len(self.requests) < self.requests_per_minute:
            self.requests.append(current_time)
            return True
        
        return False
    
    def time_to_next_slot(self):
        """Return the time in seconds until a new request slot is available"""
        if len(self.requests) < self.requests_per_minute:
            return 0
        
        current_time = time.time()
        return max(0, (self.requests[0] + self.window_size) - current_time)
