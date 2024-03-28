# 基础配置
PLATFORM = "xhs"
KEYWORDS = "python,golang"
LOGIN_TYPE = "qrcode"  # qrcode or phone or cookie
COOKIES = "bc=1; .AspNetCore.Antiforgery.z7Zm84z88Q4=CfDJ8MJJ4hfglf9Hmu9HR0pg2mIJ9ei1K873wuPLA1Flfj2wPV5VSzlYX3vBdpygxT6cfk3nPM2yR5Q5LA_-OJSh42ySi4H5514QGil2vyXHyraGEJgtECXHxIyW5ws0m5GfXgJVj82OhgRzho4e83W2da8; dnid=CfDJ8MJJ4hfglf9Hmu9HR0pg2mKoUsxurrc_nbjlXu4neIQrxbL6bS04Py1zN0EevBLaFuwsokTlg9mc03n_IrzRZbCABBlsbXsRDANxBkHQDM4_56BQpawhjZnaU1lGPzpMXFCVyk-rBdyWjucAHR00JCRk71TMcHgvKj6kqwZegYIeOziobYexRWFJfoDYV-Ysb2HlkLj4W6vUINXhBcHtc9fnx0UlXsPqIXddFqT1GsJhY8EK59j5vmkZ-mbpFoFBjCC4TP8ajio4gjZW_5q2IRA51i6z8Kmo6BRgBVDyYXfOy6GMLj-wjDjmdhcKA8yPRq7n-ssNzkVSEIJKlhlZzj3sHz2qYN67SftNWEpEj9vhUBkmMTyoRqLNly4bbrrp4aqeBeUn4D2owEZiKO2LLQS0PSl7kVydB7jiF6MqKSIYmgl5TVUvW_vIHu1Z3rbkk7ybQFW4zGDAhh4hdHgfTNdx3ug9GZJIblH027A650Xi40DLKIMr8nyXdDimRV3xpjUkozgHQ9sQieg3v3Pr8iBVJflWw110JEc-4CuNKQkKkUiBkeVlEmRqqzUZjApbZ5nX5gWe1QRZ0Sey7DLK3JgRCLXxmMVfISs79lVRWhhIvDjU961x4RZGykQYsOOrBJfwD4ulVT_JlFbyxOM7fIcyMWm5bC9bISo174CzEStlNB7dfrdRu5Wv-ybCFzjzXI-wSMOmKhaA-p5SkiRtMd7pQIrnjfAPirO59xKVxok4; AWSALB=yFkYOWsu4GZe6gpIW5MW8zuOjeQCjzGtWAJhMj5f7UwwMsmI/SzbWp1YLN26Yywp1kNhxZw6+QcA0oWaBe76IcFEgk3ITrKM1ofSM9FMpcd1DXmukP+EMCMPmonO; AWSALBCORS=yFkYOWsu4GZe6gpIW5MW8zuOjeQCjzGtWAJhMj5f7UwwMsmI/SzbWp1YLN26Yywp1kNhxZw6+QcA0oWaBe76IcFEgk3ITrKM1ofSM9FMpcd1DXmukP+EMCMPmonO"
SORT_TYPE = "popularity_descending"  # 具体值参见media_platform.xxx.field下的枚举值，展示只支持小红书
CRAWLER_TYPE = "search" # 爬取类型，search(关键词搜索) | detail(帖子相亲)| creator(创作者主页数据) | video_download (视频下载暂时只支持 bili)

# 是否开启 IP 代理
ENABLE_IP_PROXY = False

# 代理IP池数量
IP_PROXY_POOL_COUNT = 2

# 设置为True不会打开浏览器（无头浏览器），设置False会打开一个浏览器（小红书如果一直扫码登录不通过，打开浏览器手动过一下滑动验证码）
HEADLESS = True

# 是否保存登录状态
SAVE_LOGIN_STATE = True

# 数据保存类型选项配置,支持三种类型：csv、db、json
SAVE_DATA_OPTION = "json"  # csv or db or json

# 用户浏览器缓存的浏览器文件配置
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# 爬取视频/帖子的数量控制
CRAWLER_MAX_NOTES_COUNT = 20

# 并发爬虫数量控制
MAX_CONCURRENCY_NUM = 4

# 是否开启爬评论模式, 默认不开启爬评论
ENABLE_GET_COMMENTS = True

# 指定小红书需要爬虫的笔记ID列表
XHS_SPECIFIED_ID_LIST = [
    "6422c2750000000027000d88",
    "64ca1b73000000000b028dd2",
    "630d5b85000000001203ab41",
    # ........................
]

# 指定抖音需要爬取的ID列表
DY_SPECIFIED_ID_LIST = [
    "7280854932641664319",
    "7202432992642387233"
    # ........................
]

# 指定快手平台需要爬取的ID列表
KS_SPECIFIED_ID_LIST = [
    "3xf8enb8dbj6uig",
    "3x6zz972bchmvqe"
]

# 指定B站平台需要爬取的视频bvid列表
BILI_SPECIFIED_ID_LIST = [
    "BV1d54y1g7db",
    "BV1Sz4y1U77N",
    "BV14Q4y1n7jz",
    # ........................
]

# 指定微博平台需要爬取的帖子列表
WEIBO_SPECIFIED_ID_LIST = [
    "4982041758140155",
    # ........................
]

# 指定小红书创作者ID列表
XHS_CREATOR_ID_LIST = [
    "63e36c9a000000002703502b",
    # ........................
]
