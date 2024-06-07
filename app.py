from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MemberJoinedEvent
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 用户状态字典，用来存储每个用户的状态
user_state = {}
    
questions_answers = {
    '宮城縣': {
        "日向 翔陽": "烏野高中10號",
        "影山 飛雄": "烏野高中9號",
        "澤村 大地": "烏野高中1號",
        "菅原 孝支": "烏野高中2號",
        "田中 龍之介": "烏野高中5號",
        "東峰 旭": "烏野高中3號",
        "西谷 夕": "烏野高中4號",
        "月島 螢": "烏野高中11號",
        "山口 忠": "烏野高中12號",
        "緣下 力": "烏野高中6號",
        "木下 久志": "烏野高中7號",
        "成田 一仁": "成田一仁8號",
        "及川 徹": "青葉城西高中1號",
        "岩泉 一": "青葉城西高中4號",
        "松川 一靜": "青葉城西高中2號",
        "花卷 貴大": "青葉城西高中3號",
        "渡親 治": "青葉城西高中7號",
        "矢巾 秀": "青葉城西高中6號",
        "金田一 勇太郎": "青葉城西高中12號",
        "國見 英": "青葉城西高中13號",
        "京谷 賢太郎": "青葉城西高中16號",
        "茂庭 要": "伊達工業高中2號",
        "青根 高伸": "伊達工業高中7號",
        "二口 堅治": "伊達工業高中6號",
        "作並 浩輔": "伊達工業高中13號",
        "鐮先 靖志": "伊達工業高中1號",
        "笹谷 武仁": "伊達工業高中3號",
        "小原 豐": "伊達工業高中12號",
        "黃金川 貫至": "伊達工業高中7號",
        "女川 太郎": "伊達工業高中8號",
        "牛島 若利": "白鳥澤學園高中1號",
        "大平 獅音": "白鳥澤學園高中4號",
        "天童 覺": "白鳥澤學園高中5號",
        "五色 工": "白鳥澤學園高中8號",
        "白布 賢二郎": "白鳥澤學園高中10號",
        "川西 太一": "白鳥澤學園高中12號",
        "山形 隼人": "白鳥澤學園高中14號",
        "瀨見 英太": "白鳥澤學園高中3號",
        "中島 猛": "和久谷南高中1號",
        "川渡 瞬己": "和久谷南高中2號",
        "鳴子 哲平": "和久谷南高中8號",
        "白石 優希": "和久谷南高中4號",
        "花山 一雅": "和久谷南高中5號",
        "秋保 和光": "和久谷南高中10號",
        "松島剛": "和久谷南高中11號",
        "百澤 雄大": "角川學園高中9號",
        "古牧 讓": "角川學園高中5號",
        "南田 大志": "角川學園高中12號",
        "淺蟲 快人": "角川學園高中4號",
        "溫川 良明": "角川學園高中1號",
        "馬門 英治": "角川學園高中3號",
        "稲垣 功": "角川學園高中7號",
        "照島 遊兒": "條善寺高中1號",
        "二岐 丈春": "條善寺高中3號",
        "沼尻 凜太郎": "條善寺高中7號",
        "母畑 和馬": "條善寺高中2號",
        "飯坂 信義": "條善寺高中9號",
        "東山 勝道": "條善寺高中4號",
        "土湯 新": "條善寺高中11號",
        "池尻 隼人": "常波高中4號",
        "十和田 良樹": "扇南高中4號",
        "秋宮 昇": "扇南高中1號",
        "唐松 拓巳": "扇南高中2號",
        "田澤 裕樹": "扇南高中4號",
        "森岳 步": "扇南高中5號",
        "小安 颯真": "扇南高中10號",
  }
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    msg = event.message.text.strip()

    if user_id not in user_state:
        user_state[user_id] = None

    if msg == '宮城縣球員':
        user_state[user_id] = '宮城縣'
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入想查詢的球員名稱"))
    else:
        current_state = user_state[user_id]
        if current_state and msg in questions_answers[current_state]:
            reply = questions_answers[current_state][msg]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage("未找到相關答案，請重新輸入相對應的關鍵字"))

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
