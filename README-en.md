[中文](./README.md) | English
Translated by ChatGPT

# A web crawler for v2ex.com

A small crawler written to learn scrapy.

The data is stored in an SQLite database for easy sharing, with a total database size of 3.7GB.

I have released the complete SQLite database file on GitHub.

**Database Update: 2023-07-22-full**

It contains all post data, including hot topics. Both post and comment content are now scraped in their original HTML format. Additionally, the "topic" has a new field "reply_count," and "comment" has a new field "no."

## It is not recommended to run the crawler as the data is already available

The crawling process took several dozen hours because rapid crawling can result in IP banning, and I didn't use a proxy pool. Setting the concurrency to 3 should allow for continuous crawling.

[Download the database](https://github.com/oldshensheep/v2ex_scrapy/releases)

## Explanation of Crawled Data

The crawler starts crawling from `topic_id = 1`, and the path is `https://www.v2ex.com/t/{topic_id}`. The server might return 404/403/302/200 status codes. A 404 indicates that the post has been deleted, 403 indicates that the crawler has been restricted, 302 is usually a redirection to the login page or homepage, and 200 indicates a normal page.

The crawler fetches post content, comments, and user information during the crawling process.

Database table structure: [Table structure source code](./v2ex_scrapy/items.py)

## Running

Ensure Python version is >=3.10

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

The default concurrency is set to 1. To change it, modify `CONCURRENT_REQUESTS`.

#### Cookie

Some posts and post information require login for crawling. You can set a Cookie to log in. Modify the `COOKIES` value in `v2ex_scrapy/settings.py`:

```python
COOKIES = """
a=b;c=d;e=f
"""
```

#### Proxy

Change the value of `PROXIES` in `v2ex_scrapy/settings.py`, for example:

```python
[
     "http://127.0.0.1:7890"
]
```

Requests will randomly choose one of the proxies. If you need a more advanced proxy method, you can use a third-party library or implement Middleware yourself.

#### LOG

The writing of Log files is disabled by default. To enable it, uncomment this line in `v2ex_scrapy\settings.py`:

```python
LOG_FILE = "v2ex_scrapy.log"
```

### Run the Crawler

Crawl all posts, user information, and comments on the entire site:

```bash
scrapy crawl v2ex
```

Crawl posts, user information, and comments for a specific node. If node-name is empty, it crawls "flamewar":

```bash
scrapy crawl v2ex-node node=${node-name}
```

Crawl user information, starting from uid=1 and crawling up to uid=635000:

```bash
scrapy crawl v2ex-member start_id=${start_id} end_id=${end_id}
```

> If you see `scrapy: command not found`, it means the Python package installation path has not been added to the environment variable.

### Resuming the Crawl

Simply run the crawl command again, and it will automatically continue crawling, skipping the posts that have already been crawled:

```bash
scrapy crawl v2ex
```

### Notes

If you encounter a 403 error during the crawling process, it is likely due to IP restrictions. Wait for a while before trying again.

## Statistical Analysis

The SQL queries used for statistics can be found in the [query.sql](query.sql) file, and the source code for the charts is in the [analysis](analysis) subproject. It includes a Python script for exporting data to JSON for analysis and a frontend display project.

The first analysis can be found at <https://www.v2ex.com/t/954480>

For more detailed data, I suggest downloading the database.

### Statistics of Posts, Comments, and Users

Total posts: 801,038 (800,000)
Total comments: 10,899,382 (10 million)
Total users: 194,534 (200,000) - See Note 2 in the Explanation of Crawled Data

### Top Comments by Gratitude

Gratitude count is too large to display the full content. You can click on the links or download the database to query using SQL. The SQL queries are also included in the open-source files.

| Comment Link | Gratitude Count |
| :--- | :--- |
| [https://www.v2ex.com/t/820687#r_11150263](https://www.v2ex.com/t/820687#r_11150263) | 316 |
| [https://www.v2ex.com/t/437760#r_5432223](https://www.v2ex.com/t/437760#r_5432223) | 297 |
| [https://www.v2ex.com/t/915584#r_12684442](https://www.v2ex.com/t/915584#r_12684442) | 248 |
| [https://www.v2ex.com/t/917858#r_12720322](https://www.v2ex.com/t/917858#r_12720322) | 246 |
| [https://www.v2ex.com/t/949195#r_13227124](https://www.v2ex.com/t/949195#r_13227124) | 246 |
| [https://www.v2ex.com/t/881410#r_12126164](https://www.v2ex.com/t/881410#r_12126164) | 245 |
| [https://www.v2ex.com/t/884719#r_12178891](https://www.v2ex.com/t/884719#r_12178891) | 240 |
| [https://www.v2ex.com/t/901263#r_12442916](https://www.v2ex.com/t/901263#r_12442916) | 240 |
| [https://www.v2ex.com/t/749163#r_10129442](https://www.v2ex.com/t/749163#r_10129442) | 217 |
| [https://www.v2ex.com/t/877829#r_12070911](https://www.v2ex.com/t/877829#r_12070911) | 216 |

### Most Upvoted Posts

| Post Link | Title | Votes |
| :--- | :--- | :--- |
| [https://www.v2ex.com/t/110327](https://www.v2ex.com/t/110327) | UP n DOWN vote in V2EX | 321 |
| [https://www.v2ex.com/t/295433](https://www.v2ex.com/t/295433) | Snipaste - 开发了三年的截图工具，但不只是截图 | 274 |
| [https://www.v2ex.com/t/462641](https://www.v2ex.com/t/462641) | 在 D 版发过了，不过因为不少朋友看不到 D 版，我就放在这里吧，说说我最近做的这个 Project | 200 |
| [https://www.v2ex.com/t/658387](https://www.v2ex.com/t/658387) | 剽窃别人成果的人一直有，不过今天遇到了格外厉害的 | 179 |
| [https://www.v2ex.com/t/745030](https://www.v2ex.com/t/745030) | QQ 正在尝试读取你的浏览记录 | 177 |
| [https://www.v2ex.com/t/689296](https://www.v2ex.com/t/689296) | 早上还在睡觉，自如管家进了我卧室... | 145 |
| [https://www.v2ex.com/t/814025](https://www.v2ex.com/t/814025) | 分享一张我精心修改调整的 M42 猎户座大星云(Orion Nebula)壁纸。用了非常多年，首次分享出来，能和 MBP 2021 新屏幕和谐相处。 | 136 |
| [https://www.v2ex.com/t/511827](https://www.v2ex.com/t/511827) | 23 岁，得了癌症，人生无望 | 129 |
| [https://www.v2ex.com/t/427796](https://www.v2ex.com/t/427796) | 隔壁组的小兵集体情愿 要炒了 team leader | 123 |
| [https://www.v2ex.com/t/534800](https://www.v2ex.com/t/534800) | 使用 Github 账号登录 黑客派 之后， Github 自动 follow | 112 |

### Most Viewed Posts

| Post Link | Title | Views |
| :--- | :--- | :--- |
| [https://www.v2ex.com/t/510849](https://www.v2ex.com/t/510849) | chrome 签到插件 \[魂签\] 更新啦 | 39,452,510 |
| [https://www.v2ex.com/t/706595](https://www.v2ex.com/t/706595) | 迫于搬家 ··· 继续出 700 本书\~ 四折 非技术书还剩 270 多本· | 2,406,584 |
| [https://www.v2ex.com/t/718092](https://www.v2ex.com/t/718092) | 使用 GitHub 的流量数据为仓库创建访问数和克隆数的徽章 | 1,928,267 |
| [https://www.v2ex.com/t/861832](https://www.v2ex.com/t/861832) | 帮朋友推销下福建古田水蜜桃，欢迎各位购买啊 | 635,832 |
| [https://www.v2ex.com/t/176916](https://www.v2ex.com/t/176916) | 王垠这是在想不开吗 | 329,617 |
| [https://www.v2ex.com/t/303889](https://www.v2ex.com/t/303889) | 关于 V2EX 提供的 Android Captive Portal Server 地址的更新 | 295,681 |
| [https://www.v2ex.com/t/206766](https://www.v2ex.com/t/206766) | 如何找到一些有趣的 telegram 群组？ | 294,553 |
| [https://www.v2ex.com/t/265474](https://www.v2ex.com/t/265474) | ngrok 客户端和服务端如何不验证证书 | 271,244 |
| [https://www.v2ex.com/t/308080](https://www.v2ex.com/t/308080) | Element UI——一套基于 Vue 2.0 的桌面端组件库 | 221,099 |
| [https://www.v2ex.com/t/295433](https://www.v2ex.com/t/295433) | Snipaste - 开发了三年的截图工具，但不只是截图 | 210,675 |

### Users with Most Comments

| User | Comment Count |
| :--- | :--- |
| [Livid](https://www.v2ex.com/member/Livid) | 19559 |
| [loading](https://www.v2ex.com/member/loading) | 19190 |
| [murmur](https://www.v2ex.com/member/murmur) | 17189 |
| [msg7086](https://www.v2ex.com/member/msg7086) | 16768 |
| [Tink](https://www.v2ex.com/member/Tink) | 15919 |
| [imn1](https://www.v2ex.com/member/imn1) | 11468 |
| [20015jjw](https://www.v2ex.com/member/20015jjw) | 10293 |
| [x86](https://www.v2ex.com/member/x86) | 9704 |
| [opengps](https://www.v2ex.com/member/opengps) | 9694 |
| [est](https://www.v2ex.com/member/est) | 9532 |

### Users with Most Posts

| User | Topic Count |
| :--- | :--- |
| [Livid](https://www.v2ex.com/member/Livid) | 6974 |
| [icedx](https://www.v2ex.com/member/icedx) | 722 |
| [ccming](https://www.v2ex.com/member/ccming) | 646 |
| [2232588429](https://www.v2ex.com/member/2232588429) | 614 |
| [razios](https://www.v2ex.com/member/razios) | 611 |
| [coolair](https://www.v2ex.com/member/coolair) | 604 |
| [Kai](https://www.v2ex.com/member/Kai) | 599 |
| [est](https://www.v2ex.com/member/est) | 571 |
| [Newyorkcity](https://www.v2ex.com/member/Newyorkcity) | 553 |
| [WildCat](https://www.v2ex.com/member/WildCat) | 544 |

## Curves

For detailed data, I recommend downloading the database.

### Line Chart for New Users per Month

![1688470374959](image/t/1688470374959.png)

### Line Chart for New Posts per Month

![1688469358680](image/t/1688469358680.png)

### Line Chart for Comment Count

![1688470738877](image/t/1688470738877.png)

### Most Frequently Used Nodes

| Node | Count |
| :--- | :--- |
| [qna](https://www.v2ex.com/go/qna) | 188011 |
| [all4all](https://www.v2ex.com/go/all4all) | 103254 |
| [programmer](https://www.v2ex.com/go/programmer) | 51706 |
| [jobs](https://www.v2ex.com/go/jobs) | 49959 |
| [share](https://www.v2ex.com/go/share) | 35942 |
| [apple](https://www.v2ex.com/go/apple) | 20713 |
| [macos](https://www.v2ex.com/go/macos) | 19040 |
| [create](https://www.v2ex.com/go/create) | 18685 |
| [python](https://www.v2ex.com/go/python) | 14124 |
| [career](https://www.v2ex.com/go/career) | 13170 |

### Most Frequently Used Tags (auto-generated by V2EX)

| Tag | Count |
| :--- | :--- |
| [开发](https://www.v2ex.com/tag/%E5%BC%80%E5%8F%91) | 16414 |
| [App](https://www.v2ex.com/tag/App) | 13240 |
| [Python](https://www.v2ex.com/tag/Python) | 13016 |
| [Mac](https://www.v2ex.com/tag/Mac) | 12931 |
| [Java](https://www.v2ex.com/tag/Java) | 10984 |
| [Pro](https://www.v2ex.com/tag/Pro) | 9375 |
| [iOS](https://www.v2ex.com/tag/iOS) | 9216 |
| [微信](https://www.v2ex.com/tag/%E5%BE%AE%E4%BF%A1) | 8922 |
| [V2EX](https://www.v2ex.com/tag/V2EX) | 8426 |
| [域名](https://www.v2ex.com/tag/%E5%9F%9F%E5%90%8D) | 8424 |
