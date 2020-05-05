from linebot import LineBotApi
from config import Config
from rich_menu import richmenu_list

line_bot_api = LineBotApi(Config.CHANNEL_ACCESS_TOKEN)

with open("C:\\Users\\Fegnzi\\PycharmProjects\\linebotClient\\image\\richmenu.jpeg",'rb') as f:
    print(f)
    line_bot_api.set_rich_menu_image(richmenu_list.RichMenu_ID.richmenu_03, "image/jpeg", f)