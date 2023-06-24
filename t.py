import httpx
import arrow

from tutorial_scrapy.items import *

db = DB()
a = db.exist(type(MemberItem), 1)
print(a)
