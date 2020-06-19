# Slack Daily Bot

This is a Flask app that can be used on Slack and that helps to track what are the tasks done by a user and create a daily report of them.

*NOTE* Messages won't be stored into the bot database, only the data to get them from slack.

## Usage

Send a private message to the Slack Bot linked to this application or tag the bot.
You can use the shortcut `/msg @daily your message` that sends a private message to the bot.

The bot will answer with a `thumbsup` and will register your message.

After you can use a command linked to the `/report` endpoint to get a list of the saved messages.

You can clean all your messages using a slash command linked to the `/clean-all` endpoint.

## Configuration

Configure two commands:
* /daily-report: Get a daily report. It must be linked to the `/report` endpoint.
* /daily-clean-all: Remove all messages stored by the user. It must be linked to the `/clean-all` endpoint.

### Bot Token Scopes
* app_mentions:read
* channels:history
* chat:write
* commands
* im:history
* im:write
* incoming-webhook
* reactions:write

### Subscribed bot events
* app_mention
* app_mentions:read
* message.im 

### Environment Variables
* DATABASE_URL:      Contains the DB URL that can be used to configure the DB
* SLACK_OAUTH_TOKEN: OAuth token used to post messages/reactions
* SLACK_SIGN_SECRET: Sign Secret
* SLACK_WORKSPACE:   The workspace where the bot is linked
* SLACK_VERIFICATION_ENABLED : Disable the authentication to allow the initial endpoint verification
