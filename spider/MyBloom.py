from pybloom_live import ScalableBloomFilter

# 布隆过滤器
# 用法：创建对象
# 调用isExist方法，返回false则不插入，返回true则插入
class MyBloom:
    def __init__(self):
        self.sbf = ScalableBloomFilter(initial_capacity=100)

    def isExist(self, title):
        if title in self.sbf:
            return False
        else:
            self.sbf.add(title)
            return True
