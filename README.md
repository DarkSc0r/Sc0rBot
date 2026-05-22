# Sc0rBot

Sc0rBot is a Discord moderation and community bot built with `discord.py`.

## Features

### Public Commands

- `!commands` - Shows the command list.
- `!afk <reason>` - Sets your AFK status.
- `!rank` - Shows your text XP rank.
- `!voicerank` - Shows your voice XP rank.
- `!leaderboard` / `!lb` - Shows text and voice leaderboards.
- `!report @user <reason>` - Opens a private report ticket.
- `!serverinfo` - Shows information about the server.

### Staff Commands

- `!poll <question>` - Creates a yes/no poll.
- `!clean @user <amount>` - Deletes recent messages from a user.
- `!close` - Closes a report ticket.

### Automatic Systems

- Welcome messages
- Join and leave logs
- Message edit/delete logs
- Audit log tracking
- AFK mention replies
- Text XP
- Voice XP
- Automod for links, invites, caps, spam, and blocked words

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
