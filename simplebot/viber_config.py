from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

from config import TOKEN


bot_configuration = BotConfiguration(
    name="Test_Bot",
    avatar="",
    auth_token=TOKEN
)

viber = Api(bot_configuration)
