import time
import datetime

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
with open('lsi_clicks.txt','a') as f:
    f.write(st+'\n')
