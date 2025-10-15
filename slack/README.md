# Slack Integration

To connect the showcase with Slack you need a Slack App with the Events API enabled.

## Setup Steps

1. Create a new Slack app from [api.slack.com](https://api.slack.com/apps).
2. Under **Basic Information** copy the Signing Secret and set the environment variable `SLACK_SIGNING_SECRET`.
3. Create a bot token with the scopes `app_mentions:read`, `channels:history`, and `chat:write`. Store it in `SLACK_BOT_TOKEN`.
4. Configure the Events Request URL to point to `https://your-host/slack/events`.
5. Subscribe to the following events:
   - `app_mention`
   - `message.channels`
6. Invite the bot to your channels and mention it, e.g. `@AccountantAgent reconcile INV-001`.

Without credentials the backend will operate in mock mode and simply log messages instead of posting to Slack.
