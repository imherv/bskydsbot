# BSKY Discord Bot

Discord Bot using ([BlueSky](https://bsky.app/)) public API made by Herv ([@hervdesign.com on BlueSky](https://bsky.app/profile/hervdesign.com))

# Functionalities
This bot is designed to fetch and post updates from the Bluesky platform to a specified Discord channel. Below are the main functionalities of the bot:

1. **Fetching Posts from Bluesky:**

- The bot periodically checks the Bluesky platform using the BLUESKY_API_URL for new posts.
- It processes these posts and prepares them to be sent as messages in the configured Discord channel.

2. **Formatting and Sending Posts to Discord:**

- For each post retrieved, the bot extracts important details such as the post content, author information, and any images.
- The bot formats these details into a Discord embed, which includes:
- Author Information: The bot sets the author name and profile picture using the set_author method.
- Post Content: The text of the post is included in the embed description.
- Images: If an image is present in the post, it is added to the embed using the set_image method.
- Post URL: A footer is added with a link to view the full post on Bluesky.
- The bot then sends the formatted embed to the specified Discord channel.

# Configuration Guide
To get the bot up and running, you need to configure three key variables: BOT_TOKEN, CHANNEL_ID, and BLUESKY_API_URL.

1. **BOT_TOKEN:**
   
- This is the token used to authenticate the bot with the Discord API.
- You can obtain this token by creating a bot in the Discord Developer Portal.

2. **CHANNEL_ID:**
   
- This is the ID of the Discord channel where the bot will send the posts.
- You can find the channel ID by enabling Developer Mode in Discord and right-clicking the channel to copy its ID.

3. **BLUESKY_API_URL:**
   
- This is the URL used to fetch posts from the Bluesky platform.
- You should replace this URL with the appropriate API endpoint that your bot will use to retrieve posts.
- You can find the URL (in ad://) if you use skyfeed.app

# Example Code Setup
Here’s how you might set up these variables in your bot script:

```py
import os

# Load your Discord bot token
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_discord_bot_token')

# Channel ID where the bot will send messages
CHANNEL_ID = int(os.getenv('CHANNEL_ID', 123456789012345678))

# API URL for fetching Bluesky posts
BLUESKY_API_URL = os.getenv('BLUESKY_API_URL', 'https://example.com/api/posts')
```

Ensure that you replace the placeholder values with actual data and store sensitive information securely.

# Running the Bot
Once everything is configured:

1. **Install Required Packages:** Ensure you have discord.py and any other required packages installed.
```
pip install discord.py
```

2. **Run the Script:** Execute your bot script. If configured correctly, the bot will start fetching posts and sending them to the specified Discord channel.
```
python your_bot_script.py
```

That's it! Your bot should now be live, fetching posts from Bluesky, and posting them to your Discord channel as embeds.
