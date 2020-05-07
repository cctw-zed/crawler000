from threading import Thread

from GuangdongPeopleSpider import GuangdongPeopleSpider
from GuizhouPeopleSpider import GuizhouPeopleSpider
from HebeiPeopleSpider import HebeiPeopleSpider
from HenanPeopleSpider import HenanPeopleSpider
from JiangSuPeopleSpider import JiangSuPeopleSpider
from NeimengPeopleSpider import NeimengPeopleSpider
from TianJinSpider import TianJinSpider
from XinjiangPeopleSpider import XinjiangPeopleSpider
from XizangSpider import XizangSpider
from YunnanPeopleSpider import YunnanPeopleSpider
from ZhejiangPeopleSpider import ZhejiangPeopleSpider

if __name__ == '__main__':
    # t1 = Thread(target=GuangdongPeopleSpider().run)
    # t2 = Thread(target=GuizhouPeopleSpider().run)
    # t3 = Thread(target=HebeiPeopleSpider().run)
    t4 = Thread(target=HenanPeopleSpider().run)
    t5 = Thread(target=JiangSuPeopleSpider().run)
    # t6 = Thread(target=NeimengPeopleSpider().run)
    t7 = Thread(target=TianJinSpider().run)
    t8 = Thread(target=XinjiangPeopleSpider().run)
    t9 = Thread(target=XizangSpider().run)
    t10 = Thread(target=YunnanPeopleSpider().run)
    # t11 = Thread(target=ZhejiangPeopleSpider().run)

    # t1.start()
    # t2.start()
    # t3.start()
    t4.start()
    t5.start()
    # t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    # t11.start()