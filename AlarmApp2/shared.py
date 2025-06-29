import threading

shared_data = {}
data_lock = threading.Lock()
flag=0