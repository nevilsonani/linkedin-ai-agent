from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

class PostScheduler:
    def __init__(self, post_function, hour=10, minute=0):
        self.scheduler = BackgroundScheduler()
        self.post_function = post_function
        self.hour = hour
        self.minute = minute
    
    def start(self):
        # Schedule the job daily at specified hour and minute
        self.scheduler.add_job(self.post_function, 'cron', hour=self.hour, minute=self.minute)
        self.scheduler.start()
        print(f"Scheduler started: posts will be made daily at {self.hour:02d}:{self.minute:02d}")
    
    def stop(self):
        self.scheduler.shutdown()
