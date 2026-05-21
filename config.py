COMMAND_PREFIX = "!"

# Roles
MEMBER_ROLE_ID = 1449584437107884196
STAFF_ROLE_ID = 1449583557084446810

# Channels
LOG_CHANNEL_ID = 1505340380256800938
REPORT_CATEGORY_ID = 1506781294678380745

# Text XP
XP_FILE = "levels.json"
XP_COOLDOWN_SECONDS = 60
TEXT_XP_MIN = 5
TEXT_XP_MAX = 15

# Voice XP
VOICE_XP_FILE = "voice_levels.json"
VOICE_XP_PER_MINUTE = 10

# Automod
AUTOMOD_BLOCK_INVITES = True
AUTOMOD_BLOCK_LINKS = True
AUTOMOD_BLOCK_CAPS = True
AUTOMOD_BLOCK_SPAM = True
AUTOMOD_IGNORE_STAFF = False
AUTOMOD_CAPS_MIN_LETTERS = 12
AUTOMOD_CAPS_PERCENT = 0.75
AUTOMOD_SPAM_SECONDS = 8
AUTOMOD_SPAM_MESSAGE_LIMIT = 5
AUTOMOD_REPEAT_MESSAGE_LIMIT = 3

# Moderation
CLEAN_MAX_DELETE = 50
CLEAN_SEARCH_LIMIT = 500

# Add blocked words in lowercase.
BLOCKED_WORDS = [
    "badword1",
    "badword2"
]

COGS = [
    "cogs.afk",
    "cogs.automod",
    "cogs.command_list",
    "cogs.leveling",
    "cogs.logs",
    "cogs.moderation",
    "cogs.polls",
    "cogs.tickets"
]
