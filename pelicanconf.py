AUTHOR = 'Stefan Jenkner'
SITENAME = "A developer's notebook"
SITEURL = ""
SITELOGO = SITEURL + "/images/profile.png"

PATH = "content"

STATIC_PATHS = ["images", "extra/robots.txt", "extra/keybase.txt"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/keybase.txt": {"path": "keybase.txt"},
}

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
)

# Social widget
SOCIAL = (
    ("github", "https://github.com/stefanjenkner"),
    ("mastodon", "https://dresden.network/@stefanjenkner"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = 'themes/Flex'

GITHUB_CORNER_URL = "https://github.com/stefanjenkner/stefanjenkner.github.io"
