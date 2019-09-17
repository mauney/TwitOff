"""Entry point for TwitOff."""
from .app import create_app

# reminders:
# export FLASK_APP=twitoff:APP
# export FLASK_ENV=development

APP = create_app()
