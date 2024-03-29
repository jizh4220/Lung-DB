from flask import request
from app import db
from app.wordcloud import wordcloud_bp
import io
import base64
from wordcloud import WordCloud

# 真正调用词云库生成图片
def get_word_cloud(text):
    # font = "./SimHei.ttf"
    # pil_img = WordCloud(width=500, height=500, font_path=font).generate(text=text).to_image()

    pil_img = WordCloud(width=800, height=300, background_color="white").generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64



# 生成词云图片接口，以base64格式返回
@wordcloud_bp.route('/', methods=["POST"])
def cloud():
    text = request.json.get("word")
    res = get_word_cloud(text)
    return res