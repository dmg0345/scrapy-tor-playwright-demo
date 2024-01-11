"""Scrapy settings for project, more settings can be found in the documentation:

    - https://docs.scrapy.org/en/latest/topics/settings.html
    - https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
    - https://docs.scrapy.org/en/latest/topics/spider-middleware.html
    - https://docs.scrapy.org/en/latest/topics/feed-exports.html
    - https://docs.scrapy.org/en/latest/topics/item-pipeline.html
    - https://docs.scrapy.org/en/latest/topics/extensions.html
    - https://docs.scrapy.org/en/latest/topics/signals.html
    - https://docs.scrapy.org/en/latest/topics/practices.html#avoiding-getting-banned
    - https://github.com/microsoft/playwright-python
    - https://github.com/scrapy-plugins/scrapy-playwright
    - https://github.com/AtuboDad/playwright_stealth
    - https://github.com/TeamHG-Memex/scrapy-rotating-proxies"""

# pylint: disable=line-too-long

import os

import scrapy_playwright
import scrapy_playwright.headers

## Scrapy and general extensions settings ##############################################################################
BOT_NAME = "scrapy_tor_playwright_demo"

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 4

DEPTH_LIMIT = 0
DEPTH_PRIORITY = 0
DEPTH_STATS_VERBOSE = True

DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 10000
DNS_TIMEOUT = 180

# For details, refer to: https://docs.scrapy.org/en/latest/topics/downloader-middleware.html.
DOWNLOADER_MIDDLEWARES = {
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.robotstxt
    "scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware": 100,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpauth
    "scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware": 300,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.downloadtimeout
    "scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware": 350,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.defaultheaders
    "scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware": 400,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.useragent
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": 500,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.retry
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.ajaxcrawl
    "scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware": 560,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#metarefreshmiddleware
    "scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware": 580,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpcompression
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 590,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.redirect
    "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": 600,
    # Details:
    #   https://github.com/TeamHG-Memex/scrapy-rotating-proxies#usage
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "scrapy_tor_playwright_demo.middlewares.middlewares.PlaywrightMiddleware": 615,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.cookies
    "scrapy.downloadermiddlewares.cookies.CookiesMiddleware": 700,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpproxy
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 750,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.stats
    "scrapy.downloadermiddlewares.stats.DownloaderStats": 850,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpcache
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 900,
}
DOWNLOADER_CLIENT_TLS_VERBOSE_LOGGING = True
DOWNLOADER_STATS = True
DOWNLOAD_HANDLERS = {
    "data": "scrapy.core.downloader.handlers.datauri.DataURIDownloadHandler",
    "file": "scrapy.core.downloader.handlers.file.FileDownloadHandler",
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "s3": "scrapy.core.downloader.handlers.s3.S3DownloadHandler",
    "ftp": "scrapy.core.downloader.handlers.ftp.FTPDownloadHandler",
}
DOWNLOAD_TIMEOUT = 180
DOWNLOAD_MAXSIZE = 1073741824
DOWNLOAD_WARNSIZE = 33554432
DOWNLOAD_FAIL_ON_DATALOSS = True

DUPEFILTER_DEBUG = True

# For details, refer to https://docs.scrapy.org/en/latest/topics/extensions.html.
EXTENSIONS = {
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/extensions.html#module-scrapy.extensions.corestats
    "scrapy.extensions.corestats.CoreStats": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/extensions.html#module-scrapy.extensions.telnet
    "scrapy.extensions.telnet.TelnetConsole": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/extensions.html#module-scrapy.extensions.memusage
    "scrapy.extensions.memusage.MemoryUsage": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/extensions.html#module-scrapy.extensions.memdebug
    "scrapy.extensions.memdebug.MemoryDebugger": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/extensions.html#module-scrapy.extensions.closespider
    "scrapy.extensions.closespider.CloseSpider": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/feed-exports.html
    "scrapy.extensions.feedexport.FeedExporter": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/extensions.html#module-scrapy.extensions.logstats
    "scrapy.extensions.logstats.LogStats": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/spiders.html
    "scrapy.extensions.spiderstate.SpiderState": 0,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/autothrottle.html
    "scrapy.extensions.throttle.AutoThrottle": 0,
}

# For details, refer to https://docs.scrapy.org/en/latest/topics/item-pipeline.html.
ITEM_PIPELINES = {
    "scrapy_tor_playwright_demo.pipelines.pipelines.FileSystemPipeline": 300,
}

LOG_ENABLED = True
LOG_ENCODING = "utf-8"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scrapy.log")
LOG_FILE_APPEND = False
LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s: %(message)s]"
LOG_DATEFORMAT = "%d-%m-%Y %H:%M:%S"
LOG_LEVEL = "DEBUG"
LOG_STDOUT = False
LOG_SHORT_NAMES = False
LOGSTATS_INTERVAL = 60.0

MEMDEBUG_ENABLED = False
MEMDEBUG_NOTIFY = []
MEMUSAGE_ENABLED = True
MEMUSAGE_LIMIT_MB = 0
MEMUSAGE_CHECK_INTERVAL_SECONDS = 60.0
MEMUSAGE_WARNING_MB = 0

ROBOTSTXT_OBEY = False
ROBOTSTXT_USER_AGENT = None

SCHEDULER_DEBUG = True

# For details, refer to https://docs.scrapy.org/en/latest/topics/spider-middleware.html.
SPIDER_MIDDLEWARES = {
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.httperror
    "scrapy.spidermiddlewares.httperror.HttpErrorMiddleware": 50,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.offsite
    "scrapy.spidermiddlewares.offsite.OffsiteMiddleware": 500,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.referer
    "scrapy.spidermiddlewares.referer.RefererMiddleware": 700,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.urllength
    "scrapy.spidermiddlewares.urllength.UrlLengthMiddleware": 800,
    # Details:
    #   https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.depth
    "scrapy.spidermiddlewares.depth.DepthMiddleware": 900,
}
NEWSPIDER_MODULE = "scrapy_tor_playwright_demo.spiders"
SPIDER_MODULES = ["scrapy_tor_playwright_demo.spiders"]
CLOSESPIDER_TIMEOUT = 0
CLOSESPIDER_ITEMCOUNT = 0
CLOSESPIDER_PAGECOUNT = 0
CLOSESPIDER_ERRORCOUNT = 0

STATS_DUMP = True

URLLENGTH_LIMIT = 2083

USER_AGENT = None

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True
CONCURRENT_REQUESTS_PER_DOMAIN = CONCURRENT_REQUESTS
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_DELAY = 0

COMMANDS_MODULE = ""

COOKIES_ENABLED = False
COOKIES_DEBUG = True

FILES_EXPIRES = 90
FILES_STORE = "/path/to/valid/dir"
IMAGES_EXPIRES = 90
IMAGES_STORE = "/path/to/valid/dir"
MEDIA_ALLOW_REDIRECTS = False

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_IGNORE_SCHEMES = ["file"]
HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
HTTPCACHE_GZIP = False
HTTPCACHE_ALWAYS_STORE = False
HTTPCACHE_IGNORE_RESPONSE_CACHE_CONTROLS = []

HTTPERROR_ALLOWED_CODES = []
HTTPERROR_ALLOW_ALL = False

METAREFRESH_ENABLED = True
METAREFRESH_IGNORE_TAGS = []
METAREFRESH_MAXDELAY = 100

REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 20

REFERER_ENABLED = True
REFERRER_POLICY = "scrapy.spidermiddlewares.referer.DefaultReferrerPolicy"

RETRY_ENABLED = True
RETRY_TIMES = 100
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 403, 408, 429]
RETRY_PRIORITY_ADJUST = -1

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"proxy": {"server": "per-context"}}
PLAYWRIGHT_CONTEXTS = {}
PLAYWRIGHT_MAX_CONTEXTS = CONCURRENT_REQUESTS
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = DOWNLOAD_TIMEOUT * 1000
PLAYWRIGHT_PROCESS_REQUEST_HEADERS = scrapy_playwright.headers.use_scrapy_headers
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 1
PLAYWRIGHT_ABORT_REQUEST = None

ROTATING_PROXY_LIST = [
    "http://tor-proxy-pool-zero:8888",
    "http://tor-proxy-pool-one:8888",
    "http://tor-proxy-pool-two:8888",
    "http://tor-proxy-pool-three:8888",
    "http://tor-proxy-pool-four:8888",
    "http://tor-proxy-pool-five:8888",
    "http://tor-proxy-pool-six:8888",
    "http://tor-proxy-pool-seven:8888",
    "http://tor-proxy-pool-eight:8888",
    "http://tor-proxy-pool-nine:8888",
]
ROTATING_PROXY_LOGSTATS_INTERVAL = 30
ROTATING_PROXY_CLOSE_SPIDER = False
ROTATING_PROXY_PAGE_RETRY_TIMES = 100
ROTATING_PROXY_BACKOFF_BASE = 300
ROTATING_PROXY_BACKOFF_CAP = 3600
ROTATING_PROXY_BAN_POLICY = "rotating_proxies.policy.BanDetectionPolicy"

## Other ###############################################################################################################

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
