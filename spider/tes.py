from concurrent.futures import ThreadPoolExecutor
import time
 
# 参数times用来模拟网络请求的时间
def get_html(times):
    time.sleep(times)
    print("get page {}s finished".format(times))
    return times
 
executor = ThreadPoolExecutor(max_workers=2)
urls = [6, 2, 4] # 并不是真的url
 
for data in executor.map(get_html, urls):
    print("in main: get page {}s success".format(data))
# 执行结果
# get page 2s finished
# get page 3s finished
# in main: get page 3s success
# in main: get page 2s success
# get page 4s finished
