import schedule
import time
from app import *

#schedule.every(1).minutes.do(app)
schedule.every().day.at("10:30").do(app)

while True:
    schedule.run_pending()
    time.sleep(1)