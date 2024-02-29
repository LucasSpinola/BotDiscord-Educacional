from dotenv import load_dotenv
import os
from logging.config import dictConfig
import logging
import pathlib
import discord

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")

API_BOT = os.getenv("API_URL")

GUILDS_ID = discord.Object(id=int(os.getenv("GUILD")))

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"
LOGGIN_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": " %(levelname)s - %(asctime)s - %(module)-15s - %(message)s"
        },
        "standart": {
            "format": " %(levelname)s - %(name)-15s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standart"
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standart"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "Logs/infos.log",
            "mode": "w",
            "formatter": "verbose"
        }
    },
    "loggers": {
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

dictConfig(LOGGIN_CONFIG)