from datetime import datetime

AUTHOR = 'Stefan Jenkner'
SITENAME = "A developer's notebook"
SITETITLE = "Stefan Jenkner"
SITESUBTITLE = "A developer's notebook"
SITEURL = ""
SITELOGO = SITEURL + "/images/profile_2025.png"

PATH = "content"

STATIC_PATHS = ["images", "extra/robots.txt", "extra/keybase.txt"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/keybase.txt": {"path": "keybase.txt"},
}

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MAIN_MENU = True

# Blogroll
LINKS = (
)

# Social widget
SOCIAL = (
    ("github", "https://github.com/stefanjenkner"),
    ("mastodon", "https://dresden.network/@stefanjenkner"),
    ("rss", "/feeds/all.atom.xml"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = 'themes/Flex'
THEME_COLOR = 'dark'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

GITHUB_CORNER_URL = "https://github.com/stefanjenkner/stefanjenkner.github.io"

COPYRIGHT_YEAR = datetime.now().year
