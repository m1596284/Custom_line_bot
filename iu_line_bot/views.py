# -*- coding: UTF-8 -*-
import sys
import json
import datetime
from time import time
from pathlib import Path
from src.py_logging import py_logger, remove_old_log
from django.http import HttpResponse, JsonResponse, HttpRequest
from . import models
import requests
from bs4 import BeautifulSoup
import re
import random
from pytube import YouTube
from youtube_search import YoutubeSearch
import instaloader
from gforms import Form
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    StickerSendMessage,
    FlexSendMessage,
    VideoSendMessage,
    BubbleContainer,
    ImageComponent,
    URIAction,
    CarouselContainer,
    BoxComponent,
    TextComponent,
    SeparatorComponent,
    LinearGradientBackground,
)
from openai import OpenAI
import tiktoken
from notion_client import Client


# set path and name
py_path = Path(__file__).parent
py_name = Path(__file__).stem
project_path = Path(__file__).parent.parent
project_name = Path(__file__).parent.stem
log_path = f"{py_path}/log"
log_name = py_name
logger_name = f"{project_name}_{py_name}"

# set logger
remove_old_log(log_path=log_path, log_name=py_name)
log = py_logger(
    write_mode="a",
    level="INFO",
    log_path=log_path,
    log_name=log_name,
    logger_name=logger_name,
)

# Loading the access token and secret for line bot
with open(f"{str(py_path)}/config/line_bot_channel.json", encoding="utf-8") as f:
    channel_json = json.load(f)
    line_bot_api = LineBotApi(channel_json["iu_fans"]["channel_access_token"])
    handler = WebhookHandler(channel_json["iu_fans"]["channel_secret"])

# parameter
with open(f"{str(py_path)}/config/line_bot_headers.json", encoding="utf-8") as f:
    headers_json = json.load(f)
    headers_IG = headers_json["headers_IG"]
    headers_tiktok = headers_json["headers_tiktok"]
    headers_hashtag = headers_json["headers_hashtag"]
    headers_postman = headers_json["headers_postman"]

# dictionary
with open(f"{str(py_path)}/config/line_bot_dictionary.json", encoding="utf-8") as f:
    dictionary_json = json.load(f)
    IU_test = dictionary_json["IU_test"]
    IU_fans_club = dictionary_json["IU_fans_club"]
    sex_club_list = dictionary_json["sex_club_list"]
    spirit_chamber = dictionary_json["spirit_chamber"]
    IU_fans_club_chat_room = dictionary_json["IU_fans_club_chat_room"]
    permission_dict_chat_room_hometown = dictionary_json["permission_dict_chat_room_hometown"]
    legend_family = dictionary_json["legend_family"]
    line_user_dict = dictionary_json["line_user_dict"]
    keyword_dict = dictionary_json["keyword_dict"]
    dog_dict = dictionary_json["dog_dict"]
    sticker_dict = dictionary_json["sticker_dict"]
    horoscope_dict = dictionary_json["horoscope_dict"]
    weather_dict = dictionary_json["weather_dict"]
    city_encoding = dictionary_json["city_encoding"]
    location_to_city = dictionary_json["location_to_city"]

# list
with open(f"{str(py_path)}/config/line_bot_list.json", encoding="utf-8") as f:
    list_json = json.load(f)
    cityLocations = list_json["cityLocations"]
    Language_List = list_json["Language_List"]

with open(f"{str(py_path)}/config/gpt_key.json", encoding="utf-8") as f:
    gpt_key = json.load(f)["gpt_key"]

#
with open(f"{str(py_path)}/config/IG_secrets.json", encoding="utf-8") as f:
    list_json = json.load(f)
    IG_account = list_json["account"]
    IG_password = list_json["password"]

# ig = instaloader.Instaloader()
# ig.login(IG_account, IG_password)


# get admin id
admin_id = list(IU_fans_club.keys())[0]


def print_request_detail(request):
    log.info(f"{sys._getframe().f_code.co_name}: Test start")
    request_dict = json.loads(request.body.decode("utf-8"))
    destination = request_dict.get("destination")
    events = request_dict.get("events")
    events_type = request_dict["events"][0].get("type")
    events_message = request_dict["events"][0].get("message")
    events_timestamp = request_dict["events"][0].get("timestamp")
    events_source = request_dict["events"][0].get("source")
    events_reply_token = request_dict["events"][0].get("replyToken")
    events_mode = request_dict["events"][0].get("mode")
    source_type = request_dict["events"][0]["source"].get("type")
    source_group_id = request_dict["events"][0]["source"].get("groupId", "None")
    source_room_id = request_dict["events"][0]["source"].get("roomId", "None")
    source_user_id = request_dict["events"][0]["source"].get("userId")
    message_type = request_dict["events"][0]["message"].get("type")
    message_id = request_dict["events"][0]["message"].get("id")
    message_text = request_dict["events"][0]["message"].get("text")
    log.info(f"request_dict: {request_dict}")
    log.info(f"destination:\t{destination}")
    log.info(f"destination:\t{events}")
    log.info(f"events_type:\t{events_type}")
    log.info(f"events_message:\t{events_message}")
    log.info(f"message_type:\t{message_type}")
    log.info(f"message_id:\t{message_id}")
    log.info(f"message_text:\t{message_text}")
    log.info(f"events_timestamp:\t{events_timestamp}")
    log.info(f"events_source:\t{events_source}")
    log.info(f"events_reply_token:\t{events_reply_token}")
    log.info(f"events_mode:\t{events_mode}")
    log.info(f"source_type:\t{source_type}")
    log.info(f"source_group_id:\t{source_group_id}")
    log.info(f"source_room_id:\t{source_room_id}")
    log.info(f"source_user_id:\t{source_user_id}")
    # request sample
    # {
    #     "destination": "U7b5246f2dcb119442f7fc847c66d8824",
    #     "events": [
    #         {
    #             "type": "message",
    #             "message": {"type": "text", "id": "14957918020461", "text": "1"},
    #             "timestamp": 1634919357482,
    #             "source": {
    #                 "type": "user",
    #                 "userId": "U898b0be359442b95fabc587d6b9aed9e",
    #             },
    #             "replyToken": "35364dee67244dea95ab8b22a3350bc2",
    #             "mode": "active",
    #         }
    #     ],
    # }
    pass


def db_update_chat_log(user_id, user_name, chat_room, message_text):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    models.chat_log_table.objects.create(
        user_id=user_id,
        user_name=user_name,
        chat_room=chat_room,
        chat_text=message_text,
    )
    pass


def reply_help(reply_token):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    help_message = (
        "IU Line Bot v7.1 2023/05/16 " + "lunch notification" + "\n"
        "IU : 隨機IU" + "\n"
        "OO : 歐美" + "\n"
        "CC : Cosplay" + "\n"
        "MM : 台灣妹子" + "\n"
        "PP : 18禁" + "\n"
        "9fun : 9gag-funny" + "\n"
        "9girl : 9gag-girl" + "\n"
        "9hot : 9gag-nsfw" + "\n" + "\n"
        "ex : line buy" + "\n" + "顯示回饋最高的10個網站" + "\n" + "\n"
        "ex : line buy 蝦皮" + "\n" + "顯示回饋網站的網站跟連結" + "\n" + "\n"
        "ex : 雙子, 巨蟹" + "\n" + "當日運勢短評" + "\n" + "\n"
        "ex : 來首 張震嶽" + "\n" + "ex:點播 105度的你" + "\n" + "會自動播出Youtube" + "\n\n"
        "ex : 字典 dinner" + "\n" + "提供Key的詞性解釋" + "\n\n"
        "ex : 許願 新增五月天圖庫" + "\n" + "將許願資訊匿名傳送給作者" + "\n\n"
        "ex : 雷達, 雲圖, 溫度, 紫外線, 雨量" + "\n" + "最近時間的天氣資訊" + "\n\n"
        "ex : 台北士林天氣" + "\n" + "高雄天氣" + "\n" + "地點的短期天氣預報" + "\n\n"
        "ex : 我就爛" + "\n" + "觸發關鍵字會自動展圖" + "\n" + "-h keyword 列出關鍵字表" + "\n\n"
        "自動展圖 : IG, youtube, Ptt(moPtt), 抖音, Twitter, imgur, #tag" + "\n"
        "Porn keyword ..."
    )
    line_bot_api.reply_message(reply_token, TextSendMessage(text=help_message))


def reply_help_keyword(reply_token):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    help_message = ""
    for key in keyword_dict.keys():
        help_message = f"{help_message}\n{key}"
    for key in dog_dict.keys():
        help_message = f"{help_message}\n{key}"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=help_message))


def reply_keyword(reply_token, message_text):
    if message_text in keyword_dict:
        url_keyword = keyword_dict[message_text]
    elif message_text in dog_dict:
        url_keyword = dog_dict[message_text]
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=url_keyword, preview_image_url=url_keyword),
    )


def reply_dog_card(reply_token):
    url_keyword = random.choice(list(dog_dict.values()))
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=url_keyword, preview_image_url=url_keyword),
    )


def reply_sticker(reply_token, message_text):
    sitcker_id = sticker_dict[message_text]
    line_bot_api.reply_message(reply_token, StickerSendMessage(package_id=11537, sticker_id=sitcker_id))


def reply_porn(reply_token, message_text):
    input_url = "https://www.xvideos.com/?k=" + message_text + "&sort=relevance&quality=hd"
    r = requests.get(input_url, headers=headers_postman, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    video_all = soup.find_all("div", class_="thumb")
    video = str(video_all[random.randint(1, 27)])
    input_url = "https://www.xvideos.com" + video[video.find("href") + 6 : video.find('">', 20)]
    r = requests.get(input_url, headers=headers_postman, timeout=10)
    video = r.text
    output_url = video[video.find("setVideoUrlHigh") + 17 : video.find("')", video.find("setVideoUrlHigh"))]
    picture_url = video[video.find("setThumbUrl169") + 16 : video.find("')", video.find("setThumbUrl169"))]
    line_bot_api.reply_message(
        reply_token,
        VideoSendMessage(original_content_url=output_url, preview_image_url=picture_url),
    )


def reply_xvideos(reply_token, message_text):
    input_url = message_text
    r = requests.get(input_url, headers=headers_postman, timeout=10)
    video = r.text
    output_url = video[video.find("setVideoUrlHigh") + 17 : video.find("')", video.find("setVideoUrlHigh"))]
    picture_url = video[video.find("setThumbUrl169") + 16 : video.find("')", video.find("setThumbUrl169"))]
    line_bot_api.reply_message(
        reply_token,
        VideoSendMessage(original_content_url=output_url, preview_image_url=picture_url),
    )


def reply_douyin(reply_token, message_text):
    # url preprocessing
    if message_text.find("v.douyin.com") != -1:
        input_url = message_text[message_text.find("http") : message_text.find("/", message_text.find("http") + 21) + 1]
        redirect_url = requests.get(input_url, headers=headers_hashtag, timeout=10).url
        item_ids = redirect_url[redirect_url.find("video") + 6 : redirect_url.find("?")]
    else:
        redirect_url = message_text[message_text.find("http") :]
        item_ids = redirect_url[redirect_url.find("video") + 6 : redirect_url.find("?")]
    redirect_url = redirect_url[0 : redirect_url.find("?")]
    r = requests.get(redirect_url, headers=headers_hashtag, timeout=10)
    input_url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_ids}"
    log.info(input_url)
    r = requests.get(input_url, headers=headers_hashtag, timeout=10)
    output_url = r.json()["item_list"][0]["video"]["play_addr"]["url_list"][0]
    picture_url = r.json()["item_list"][0]["video"]["cover"]["url_list"][0]
    # picture_url = picture_url.replace("300x400","540x960")
    r = requests.get(picture_url, timeout=10)
    if r.text.find("Fail to handle imagesite request") > 1:
        picture_url = picture_url.replace("540x960", "300x400")
    line_bot_api.reply_message(
        reply_token,
        VideoSendMessage(original_content_url=output_url, preview_image_url=picture_url),
    )


def reply_tiktok(reply_token, message_text):
    r = requests.get(message_text, headers=headers_tiktok, timeout=10)
    r_text = r.text
    video_url = r_text[r_text.find("playAddr") + 11 : r_text.find("downloadAddr") - 3]
    video_url = video_url.encode("utf-8").decode("unicode_escape")
    picture_url = r_text[r_text.find("originCover") + 14 : r_text.find("dynamicCover") - 3]
    picture_url = picture_url.encode("utf-8").decode("unicode_escape")
    headers_tiktok_referer = {"referer": f"{video_url}"}
    r = requests.get(video_url, headers=headers_tiktok_referer, timeout=10)
    ts = str(time()).replace(".", "")
    temp_path = f"{project_path}/media/tiktok/{ts}.mp4"
    with open(temp_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    warehouse_url = f"https://iufans.club/warehouse/tiktok/{ts}"
    line_bot_api.reply_message(
        reply_token,
        VideoSendMessage(original_content_url=warehouse_url, preview_image_url=picture_url),
    )


def reply_IG(reply_token, chat_room, message_text):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    # url preprocessing
    if message_text[0:22] == "https://instagram.com/":
        message_text = f"https://www.{message_text[8:]}"
    # picture, video of post
    if "/p/" in message_text or "/reel/" in message_text:  # Instagram
        log.info("IG post")
        if message_text[0:31] == "https://www.instagram.com/reel/":
            message_text = message_text.replace("/reel/", "/p/")
        shortcode = message_text[message_text.find("/p/") + 3 : message_text.find("/", message_text.find("/p/") + 3)]
        sub_page = f"https://www.instagram.com/p/{shortcode}/"
        log.info(shortcode)

        # init instaloader
        ig = instaloader.Instaloader()
        # log.info(ig)
        post = instaloader.Post.from_shortcode(ig.context, shortcode)
        # log.info(post)
        # get IG_post_title
        IG_post_title = post.caption
        IG_post_title_lines = IG_post_title.count("\n")
        if IG_post_title_lines > 6:
            IG_post_title_ratio = "30%"
        elif IG_post_title_lines < 2:
            IG_post_title_ratio = "12%"
        else:
            IG_post_title_ratio = str(int(IG_post_title_lines * 5)) + "%"
        log.info(IG_post_title_lines)
        log.info(IG_post_title_ratio)
        log.info(post)

        # find meida_count
        media_num = post.mediacount
        log.info(media_num)
        picture_list = []
        video_list = []
        if media_num > 1:
            log.info("media")
            for each_post in post.get_sidecar_nodes():
                if each_post.is_video:
                    video_list.append(each_post.display_url)
                    video_list.append(each_post.video_url)
                else:
                    picture_list.append(each_post.display_url)
        elif media_num == 1 and post.is_video:
            video_list.append(post.url)
            video_list.append(post.video_url)
        else:
            picture_list.append(post.url)
        log.info(picture_list)
        log.info(video_list)
        # reply picture
        # reply multiple picture
        if len(picture_list) > 1:
            log.info("IG multiple picture")
            bubble_container = []
            for i in range(len(picture_list)):
                if i == 0:
                    container = BubbleContainer(
                        size="giga",
                        body=BoxComponent(
                            layout="vertical",
                            margin="none",
                            padding_all="0px",
                            contents=[
                                ImageComponent(
                                    url=picture_list[i],
                                    size="full",
                                    aspect_mode="cover",
                                    aspect_ratio="1:1",
                                    action=URIAction(uri=picture_list[i]),
                                ),
                                BoxComponent(
                                    layout="vertical",
                                    contents=[
                                        TextComponent(
                                            text=IG_post_title,
                                            size="xs",
                                            color="#ffffff",
                                            wrap=True,
                                        )
                                    ],
                                    background=LinearGradientBackground(
                                        angle="0deg",
                                        start_color="#00000099",
                                        end_color="#00000000",
                                    ),
                                    position="absolute",
                                    width="100%",
                                    height=IG_post_title_ratio,
                                    offset_bottom="0px",
                                    offset_start="0px",
                                    offset_end="0px",
                                ),
                            ],
                        ),
                    )
                    bubble_container.append(container)
                else:
                    container = BubbleContainer(
                        size="giga",
                        hero=ImageComponent(
                            url=picture_list[i],
                            size="full",
                            aspect_mode="cover",
                            action=URIAction(uri=picture_list[i]),
                        ),
                    )
                    bubble_container.append(container)
            line_bot_api.reply_message(
                reply_token,
                FlexSendMessage(
                    alt_text="Multiple pictures",
                    contents=CarouselContainer(contents=bubble_container),
                ),
            )
        elif len(picture_list) == 1:
            log.info("IG single picture")
            single_url = picture_list[0]
            bubble_container = []
            container = BubbleContainer(
                size="giga",
                body=BoxComponent(
                    layout="vertical",
                    margin="none",
                    padding_all="0px",
                    contents=[
                        ImageComponent(
                            url=single_url,
                            size="full",
                            aspect_mode="cover",
                            aspect_ratio="1:1",
                            action=URIAction(uri=single_url),
                        ),
                        BoxComponent(
                            layout="vertical",
                            contents=[
                                TextComponent(
                                    text=IG_post_title,
                                    size="xs",
                                    color="#ffffff",
                                    wrap=True,
                                )
                            ],
                            background=LinearGradientBackground(
                                angle="0deg",
                                start_color="#00000099",
                                end_color="#00000000",
                            ),
                            position="absolute",
                            width="100%",
                            height=IG_post_title_ratio,
                            offset_bottom="0px",
                            offset_start="0px",
                            offset_end="0px",
                        ),
                    ],
                ),
            )
            bubble_container.append(container)
            line_bot_api.reply_message(
                reply_token,
                FlexSendMessage(
                    alt_text="Multiple pictures",
                    contents=CarouselContainer(contents=bubble_container),
                ),
            )

        log.info(video_list)
        log.info(len(video_list))
        if len(video_list) > 2:
            log.info("IG multiple video")
            # push video
            int(len(video_list) / 2)
            for i in range(int(len(video_list) / 2)):
                thumbnail_url = video_list[i * 2]
                video_url = video_list[i * 2 + 1]
                line_bot_api.push_message(
                    chat_room,
                    VideoSendMessage(original_content_url=video_url, preview_image_url=thumbnail_url),
                )
        else:
            log.info("IG single video")
            thumbnail_url = video_list[0]
            video_url = video_list[1]
            line_bot_api.reply_message(
                reply_token,
                VideoSendMessage(original_content_url=video_url, preview_image_url=thumbnail_url),
            )
    # picture, video of story
    elif message_text[0:34] == "https://www.instagram.com/stories/":  # IG time limit
        pass
        # get IG_post_title
        # story_num = message_text[message_text.find("/", 34) + 1 : message_text.find("?")]
        # media_dict = cl.media_info(story_num).dict()
        # IG_post_title = media_dict["caption_text"]
        # if str(media_dict["video_url"]) == "None":
        #     thumbnail_url = str(media_dict["thumbnail_url"])
        #     line_bot_api.reply_message(
        #         reply_token,
        #         ImageSendMessage(
        #             original_content_url=thumbnail_url, preview_image_url=thumbnail_url
        #         ),
        #     )
        # else:
        #     thumbnail_url = str(media_dict["thumbnail_url"])
        #     video_url = str(media_dict["video_url"])
        #     line_bot_api.reply_message(
        #         reply_token,
        #         VideoSendMessage(original_content_url=video_url, preview_image_url=thumbnail_url),
        #     )
    # video of TV
    elif "/tv/" in message_text:  # IG time limit
        pass
        # get IG_post_title
        # sub_page = message_text
        # media_code = cl.media_pk_from_url(sub_page)
        # media_dict = cl.media_info(media_code).dict()
        # IG_post_title = media_dict["caption_text"]
        # log.info(media_dict)
        # thumbnail_url = str(media_dict["thumbnail_url"])
        # video_url = str(media_dict["video_url"])
        # line_bot_api.reply_message(
        #     reply_token,
        #     VideoSendMessage(original_content_url=video_url, preview_image_url=thumbnail_url),
        # )
    # picture of user
    elif message_text[0:26] == "https://www.instagram.com/":
        url_num = 5
        Main_page = message_text
        r = requests.get(Main_page, headers=headers_IG, timeout=10)
        start_main = r.text.find('content="https://instagram') + 9
        end_main = r.text.find('"', start_main)
        main_url = r.text[start_main:end_main]
        start = 0
        bubble_container = []
        tag_num = r.text.count("shortcode")
        post_list = []
        post_codes = []
        likecount_list = []
        likecount_nums = []
        for _ in range(tag_num):
            start = r.text.find("shortcode", start) + 12
            end = start + 11
            shortcode = r.text[start:end].replace('"', "")
            post_list.append(shortcode)
            start_like = r.text.find("edge_liked_by", start) + 24
            end_like = r.text.find("}", r.text.find("edge_liked_by", start) + 24)
            try:
                post_like = int(r.text[start_like:end_like])
            except Exception:
                post_like = 9999999999
            likecount_list.append(post_like)
        for likecount_index, _ in enumerate(likecount_list):
            try:
                if likecount_list[likecount_index] != likecount_list[likecount_index + 1]:
                    likecount_nums.append(likecount_list[likecount_index])
                    post_codes.append(post_list[likecount_index])
            except Exception:
                if likecount_list[likecount_index] != likecount_list[0]:
                    likecount_nums.append(likecount_list[likecount_index])
                    post_codes.append(post_list[likecount_index])
        if len(post_codes) > url_num:
            loop_times = url_num
        else:
            loop_times = len(post_codes)
        container = BubbleContainer(
            size="giga",
            hero=ImageComponent(
                url=main_url,
                size="full",
                aspect_mode="cover",
                action=URIAction(uri=main_url),
            ),
        )
        bubble_container.append(container)
        for opt_num in range(loop_times):
            shortcode = post_codes[opt_num]
            sub_page = f"https://www.instagram.com/p/{shortcode}/"
            r_2 = requests.get(sub_page, headers=headers_IG, timeout=10)
            start = 0
            start = r_2.text.find("display_url", start) + 14
            end = r_2.text.find(",", start) - 1
            url_tag = r_2.text[start:end].replace("\\u0026", "&")
            container = BubbleContainer(
                size="giga",
                hero=ImageComponent(
                    url=url_tag,
                    size="full",
                    aspect_mode="cover",
                    action=URIAction(uri=url_tag),
                ),
            )
            bubble_container.append(container)
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text="Multiple pictures",
                contents=CarouselContainer(contents=bubble_container),
            ),
        )


def reply_hashtag(reply_token, message_text):
    Main_page = f"https://www.instagram.com/explore/tags/{message_text}/"
    url_num = 10
    r = requests.get(Main_page, headers=headers_hashtag, timeout=10)
    start = 0
    bubble_container = []
    tag_num = r.text.count("display_url")
    display_url_list = []
    likecount_list = []
    if tag_num != 0:
        for i in range(tag_num):
            start = r.text.find("display_url", start) + 14
            end = r.text.find("edge_liked_by", start) - 3
            display_url = r.text[start:end].replace('"', "").replace("\\u0026", "&")
            display_url_list.append(display_url)
            start_like = r.text.find("edge_liked_by", start) + 24
            end_like = r.text.find("}", r.text.find("edge_liked_by", start) + 24)
            post_like = int(r.text[start_like:end_like])
            likecount_list.append(post_like)
        for post_index, post_code in enumerate(display_url_list):
            if display_url_list.count(post_code) > 1:
                display_url_list.remove(display_url_list[post_index])
                likecount_list.remove(likecount_list[post_index])
        if len(display_url_list) > url_num:
            loop_times = url_num
        else:
            loop_times = len(display_url_list)
        for _ in range(loop_times):
            display_url = display_url_list[likecount_list.index(max(likecount_list))]
            display_url_list.remove(display_url_list[likecount_list.index(max(likecount_list))])
            likecount_list.remove(max(likecount_list))
            container = BubbleContainer(
                size="giga",
                hero=ImageComponent(
                    url=display_url,
                    size="full",
                    aspect_mode="cover",
                    action=URIAction(uri=display_url),
                ),
            )
            bubble_container.append(container)
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text="Multiple pictures",
                contents=CarouselContainer(contents=bubble_container),
            ),
        )
    else:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="無此Tag"))


def reply_fb(reply_token, message_text):
    r = requests.get(message_text, timeout=10)
    if r.text.find("hd_src") != -1:
        output_url = re.search('hd_src:"(.+?)"', r.text).group(1)
        display_url = re.search("spriteIndexToURIMap:{(.+?)}", r.text)[1]
        display_url = display_url[5 : display_url.find(",")].replace(",", "").replace('"', "")
        line_bot_api.reply_message(
            reply_token,
            VideoSendMessage(original_content_url=output_url, preview_image_url=display_url),
        )
    else:
        start = r.text.find("og:image") + 19
        end = r.text.find(" />", start + 1) - 1
        output_url = r.text[start:end]
        output_url = output_url.replace("&amp;", "&")
        display_url = output_url
        print(output_url)
        print(display_url)
        line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(original_content_url=output_url, preview_image_url=display_url),
        )


def reply_youtube(reply_token, message_text):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    input_url = message_text
    yt = YouTube(input_url)
    output_url = yt.streams.get_highest_resolution().url
    if input_url.find("youtube") != -1:
        start = input_url.find("v=") + 2
        end = start + 11
        display_url = f"https://i.ytimg.com/vi/{input_url[start:end]}/0.jpg"
    else:
        start = input_url.find(".be/") + 4
        end = start + 11
        display_url = f"https://i.ytimg.com/vi/{input_url[start:end]}/0.jpg"
    line_bot_api.reply_message(
        reply_token,
        VideoSendMessage(original_content_url=output_url, preview_image_url=display_url),
        True,
    )


def reply_ptt(reply_token, message_text):
    if message_text.find("www.ptt.cc") != -1:
        message_text = message_text[message_text.find("https") : message_text.find(".html") + 5]
        message_text = message_text.replace(".html", "").replace("/", ".").replace("https:..www.ptt.cc.bbs.", "https://moptt.tw/p/")
    input_url = message_text
    input_url = input_url.replace("/p/", "/ptt/")
    bubble_container = []
    output_url = json.loads(requests.get(input_url).text)
    loop_times = output_url["content"].count("imgur")
    if loop_times > 10:
        loop_times = 10
    start = 0
    for _ in range(loop_times):
        start = output_url["content"].find("http", start + 1)
        end = output_url["content"].find("\n", start)
        if output_url["content"][start:end].find(".gif") == -1:
            if output_url["content"][start:end].find("i.imgur") == -1:
                url_out = output_url["content"][start:end].replace("imgur", "i.imgur") + ".jpg"
            else:
                url_out = output_url["content"][start:end]
            if url_out.find("https") == -1:
                url_out = url_out.replace("http", "https")
            container = BubbleContainer(
                size="giga",
                hero=ImageComponent(
                    url=url_out,
                    size="full",
                    aspect_mode="cover",
                    action=URIAction(uri=url_out),
                ),
            )
            bubble_container.append(container)
    line_bot_api.reply_message(
        reply_token,
        FlexSendMessage(
            alt_text="Multiple pictures",
            contents=CarouselContainer(contents=bubble_container),
        ),
    )


def reply_twitter(reply_token, message_text):
    url = "https://www.expertsphp.com/instagram-reels-downloader.php"
    data_1 = {"url": message_text}
    r = requests.post(url, data=data_1)
    url_out = r.text[r.text.find('src="http://pbs') + 5 : r.text.find(".jpg", r.text.find('src="http://pbs')) + 4]
    if url_out.find("https") == -1:
        url_out = url_out.replace("http", "https")
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=url_out, preview_image_url=url_out),
    )


def reply_imgur(reply_token, message_text):
    # error
    url_out = message_text
    if url_out.find("https") == -1:
        url_out = url_out.replace("http", "https")
    if url_out.find("m.imgur.com") != -1:
        url_out = url_out.replace("m.imgur.com", "i.imgur.com")
        url_out = url_out + ".jpg"
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=url_out, preview_image_url=url_out),
    )


def IU_call_love_list(reply_token, chat_room):
    iu_love_list = models.iu_love_table.objects.all().order_by("id")
    bubble_container = []
    for table_id, table_object in enumerate(iu_love_list):  # table_id start from 0
        container = BubbleContainer(
            size="giga",
            hero=ImageComponent(
                url=table_object.url,
                size="full",
                aspect_mode="cover",
                action=URIAction(uri=table_object.url),
            ),
        )
        bubble_container.append(container)
        if (table_id % 10) == 9 or table_id == len(iu_love_list) - 1:
            line_bot_api.push_message(
                chat_room,
                FlexSendMessage(
                    alt_text="Multiple pictures",
                    contents=CarouselContainer(contents=bubble_container),
                ),
            )
            bubble_container = []


def IU_call_random_pic(reply_token):
    iu_list = models.iu_table.objects.all().order_by("id")
    chose_id = random.randint(0, len(iu_list))
    url_out = iu_list[chose_id].url
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=url_out, preview_image_url=url_out),
    )


def reply_yuyan(reply_token):
    yuyan_list = models.yuyan_table.objects.all().order_by("id")
    chose_id = random.randint(0, len(yuyan_list))
    url_out = yuyan_list[chose_id].url
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=url_out, preview_image_url=url_out),
    )


def reply_double_word_pic(reply_token, message_text):
    if message_text == "MM":
        log.info("MM")
        double_word_table = models.mm_table
        log.info(double_word_table)
    elif message_text == "OO":
        double_word_table = models.oo_table
    elif message_text == "CC":
        double_word_table = models.cc_table
    elif message_text == "PP":
        double_word_table = models.pp_table
    double_word_list = double_word_table.objects.all().order_by("id")
    package_num = int(double_word_list[0].package)
    if package_num == int(double_word_list[len(double_word_list) - 1].package):
        package_num = int(double_word_list[len(double_word_list) - 1].package)
        # package_num = 1
    else:
        package_num = package_num + 1
    package_num = str(package_num)
    log.info(package_num)
    picture_list = double_word_table.objects.filter(package=package_num).order_by("id")
    log.info(picture_list)
    bubble_container = []
    for num, picture in enumerate(picture_list):
        picture_text = picture.package_name
        if num == 0:
            container = BubbleContainer(
                size="giga",
                body=BoxComponent(
                    layout="vertical",
                    margin="none",
                    padding_all="0px",
                    contents=[
                        ImageComponent(
                            url=picture.url,
                            size="full",
                            aspect_mode="cover",
                            aspect_ratio="1:1",
                            action=URIAction(uri=picture.url),
                        ),
                        BoxComponent(
                            layout="vertical",
                            contents=[
                                TextComponent(
                                    text=picture_text,
                                    size="xs",
                                    color="#ffffff",
                                    wrap=True,
                                )
                            ],
                            background=LinearGradientBackground(
                                angle="0deg",
                                start_color="#00000099",
                                end_color="#00000000",
                            ),
                            position="absolute",
                            width="100%",
                            height="10%",
                            offset_bottom="0px",
                            offset_start="0px",
                            offset_end="0px",
                        ),
                    ],
                ),
            )
        else:
            container = BubbleContainer(
                size="giga",
                hero=ImageComponent(
                    url=picture.url,
                    size="full",
                    aspect_mode="cover",
                    action=URIAction(uri=picture.url),
                ),
            )
        bubble_container.append(container)
    line_bot_api.reply_message(
        reply_token,
        FlexSendMessage(
            alt_text="Multiple pictures",
            contents=CarouselContainer(contents=bubble_container),
        ),
    )
    double_word_table.objects.filter(id=0).update(package=package_num)


def reply_9gag(reply_token, message_text):
    if message_text == "9FUN":
        ngag_table = models.ngag_funny_table
    elif message_text == "9GIRL":
        ngag_table = models.ngag_girl_table
    elif message_text == "9HOT":
        ngag_table = models.ngag_nsfw_table
    ngag_list = ngag_table.objects.all().order_by("id")
    row_id = int(ngag_list[0].article_id)
    if row_id == int(ngag_list[len(ngag_list) - 1].id):
        row_id = int(ngag_list[len(ngag_list) - 1].id)
        # package_num = 1
    else:
        row_id = row_id + 1
    ngag_row = ngag_table.objects.get(id=row_id)
    if ngag_row.article_type == "mp4":
        video_url = f"https://img-9gag-fun.9cache.com/photo/{ngag_row.article_id}_460sv.mp4"
        display_url = f"https://img-9gag-fun.9cache.com/photo/{ngag_row.article_id}_700b.jpg"
        line_bot_api.reply_message(
            reply_token,
            VideoSendMessage(original_content_url=video_url, preview_image_url=display_url),
        )
        ngag_table.objects.filter(id=0).update(article_id=row_id)
    else:
        display_url = f"https://img-9gag-fun.9cache.com/photo/{ngag_row.article_id}_460s.jpg"
        display_url = f"https://img-9gag-fun.9cache.com/photo/{ngag_row.article_id}_700b.jpg"
        bubble_container = []
        container = BubbleContainer(
            size="giga",
            body=BoxComponent(
                layout="vertical",
                margin="none",
                padding_all="0px",
                contents=[
                    ImageComponent(
                        url=display_url,
                        size="full",
                        action=URIAction(uri=display_url),
                    ),
                    BoxComponent(
                        layout="vertical",
                        contents=[
                            TextComponent(
                                text=ngag_row.article_title,
                                size="xs",
                                color="#ffffff",
                                wrap=True,
                                offset_start="60px",
                                position="absolute",
                            )
                        ],
                        background=LinearGradientBackground(angle="0deg", start_color="#00000099", end_color="#00000000"),
                        position="absolute",
                        width="100%",
                        height="10%",
                        offset_bottom="0px",
                        offset_start="0px",
                        offset_end="0px",
                    ),
                ],
            ),
        )
        bubble_container.append(container)
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(
                alt_text="Multiple pictures",
                contents=CarouselContainer(contents=bubble_container),
            ),
        )
        ngag_table.objects.filter(id=0).update(article_id=row_id)


def reply_for_ccc(reply_token):
    ccc_list = models.ccc_table.objects.all().order_by("id")
    chose_id = random.randint(0, len(ccc_list))
    url_out = ccc_list[chose_id].url
    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=url_out, preview_image_url=url_out),
    )


def reply_for_man(reply_token):
    man_list = models.man_table.objects.all().order_by("id")
    package_num = int(man_list[0].package)
    if package_num == int(man_list[len(man_list) - 1].package):
        package_num = int(man_list[len(man_list) - 1].package)
    else:
        package_num = package_num + 1
    picture_list = models.man_table.objects.filter(package=package_num).order_by("id")

    bubble_container = []
    for num, picture in enumerate(picture_list):
        picture_text = picture.package_name
        if num == 0:
            container = BubbleContainer(
                size="giga",
                body=BoxComponent(
                    layout="vertical",
                    margin="none",
                    padding_all="0px",
                    contents=[
                        ImageComponent(
                            url=picture.url,
                            size="full",
                            aspect_mode="cover",
                            aspect_ratio="1:1",
                            action=URIAction(uri=picture.url),
                        ),
                        BoxComponent(
                            layout="vertical",
                            contents=[
                                TextComponent(
                                    text=picture_text,
                                    size="xs",
                                    color="#ffffff",
                                    wrap=True,
                                )
                            ],
                            background=LinearGradientBackground(
                                angle="0deg",
                                start_color="#00000099",
                                end_color="#00000000",
                            ),
                            position="absolute",
                            width="100%",
                            height="10%",
                            offset_bottom="0px",
                            offset_start="0px",
                            offset_end="0px",
                        ),
                    ],
                ),
            )
        else:
            container = BubbleContainer(
                size="giga",
                hero=ImageComponent(
                    url=picture.url,
                    size="full",
                    aspect_mode="cover",
                    action=URIAction(uri=picture.url),
                ),
            )
        bubble_container.append(container)

    line_bot_api.reply_message(
        reply_token,
        FlexSendMessage(
            alt_text="Multiple pictures",
            contents=CarouselContainer(contents=bubble_container),
        ),
    )
    models.man_table.objects.filter(id=0).update(package=package_num)


def dict_translator(reply_token, message_text):
    main_url = f"https://api.urbandictionary.com/v0/define?term={message_text}"
    r = requests.get(main_url, headers=headers_hashtag)
    json_dict = json.loads(r.text)
    output_str = f"Urban dictionary\n{message_text}\n\n"
    for num in range(len(json_dict["list"])):
        if num < 3:
            temp_str = json_dict["list"][num]["definition"].replace("[", "").replace("]", "").replace("-", ": ").replace("\n", "")
            output_str = f"{output_str}Def {num+1}: {temp_str}\n"
            temp_str = json_dict["list"][num]["example"].replace("[", "").replace("]", "").replace("-", ": ").replace("\n", "")
            output_str = f"{output_str}Ex {num+1}: {temp_str}\n\n"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=output_str))


def weather(reply_token, message_text):
    Authorization = "CWB-7DBEB9CD-CC73-4483-8615-B05C5CE54979"
    if len(message_text) == 6:
        message_text = message_text.replace("台", "臺")
        city_message_text = message_text[:2]
        loc_message_text = message_text[2:4]
        print(city_message_text)
        print(loc_message_text)
        for item in cityLocations:
            if city_message_text == "宜蘭" and loc_message_text == "宜蘭":
                city = "宜蘭縣"
                location = "宜蘭市"
                city_code = city_encoding[city]
                break
            elif city_message_text in item and loc_message_text in item:
                city_code = city_encoding[item[:3]]
                city = item[:3]
                location = item[3:]
                break
    else:
        message_text = message_text[:2].replace("台", "臺")
        print(message_text)
        city_counter = 0
        city_start = 0
        for item in cityLocations:
            if item[:3].find(message_text) == 0:
                city_counter = city_counter + 1
        for item in cityLocations:
            if message_text in item:
                if item.find(message_text) < 2:
                    print(item)
                    city_code = city_encoding[item[:3]]
                    city = item[:3]
                    print(city_start, city_counter)
                    location = cityLocations[city_start + random.randint(0, city_counter - 1)][3:]
                    print(item, city, location, city_code)
                else:
                    print(item)
                    city_code = city_encoding[item[:3]]
                    city = item[:3]
                    location = item[3:]
                break
            city_start = city_start + 1
    w_page = f"https://opendata.cwb.gov.tw/api/v1/rest/datastore/{city_code}?Authorization={Authorization}&locationName={location}"
    # print(w_page)
    r = json.loads(requests.get(w_page).text)
    rain_1_start = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][0]["startTime"][11:13])
    if int(rain_1_start) > 11:
        rain_1_daytime = "晚上"
        rain_2_daytime = "白天"
        rain_3_daytime = "晚上"
        rain_4_daytime = "早上"
    else:
        rain_1_daytime = "早上"
        rain_2_daytime = "晚上"
        rain_3_daytime = "早上"
        rain_4_daytime = "晚上"
    if rain_1_start == "00":
        rain_1_daytime = "凌晨"
        rain_2_daytime = "早上"
        rain_3_daytime = "晚上"
        rain_4_daytime = "早上"
    rain_1_day = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][0]["startTime"][5:10])
    rain_1_day = f"{rain_1_day[0:2]}/{rain_1_day[3:]}"
    rain_2_day = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][1]["startTime"][5:10])
    rain_2_day = f"{rain_2_day[0:2]}/{rain_2_day[3:]}"
    rain_3_day = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][2]["startTime"][5:10])
    rain_3_day = f"{rain_3_day[0:2]}/{rain_3_day[3:]}"
    rain_4_day = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][3]["startTime"][5:10])
    rain_4_day = f"{rain_4_day[0:2]}/{rain_4_day[3:]}"
    rain_1_po = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][0]["elementValue"][0]["value"])
    rain_2_po = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][1]["elementValue"][0]["value"])
    rain_3_po = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][2]["elementValue"][0]["value"])
    rain_4_po = str(r["records"]["locations"][0]["location"][0]["weatherElement"][0]["time"][3]["elementValue"][0]["value"])
    temp_1 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"][0]["elementValue"][0]["value"])
    temp_2 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"][1]["elementValue"][0]["value"])
    temp_3 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"][2]["elementValue"][0]["value"])
    temp_4 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][1]["time"][3]["elementValue"][0]["value"])
    wind_1 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][4]["time"][0]["elementValue"][0]["value"])
    wind_2 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][4]["time"][1]["elementValue"][0]["value"])
    wind_3 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][4]["time"][2]["elementValue"][0]["value"])
    wind_4 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][4]["time"][3]["elementValue"][0]["value"])
    wind_1_d = str(r["records"]["locations"][0]["location"][0]["weatherElement"][13]["time"][0]["elementValue"][0]["value"])
    wind_2_d = str(r["records"]["locations"][0]["location"][0]["weatherElement"][13]["time"][1]["elementValue"][0]["value"])
    wind_3_d = str(r["records"]["locations"][0]["location"][0]["weatherElement"][13]["time"][2]["elementValue"][0]["value"])
    wind_4_d = str(r["records"]["locations"][0]["location"][0]["weatherElement"][13]["time"][3]["elementValue"][0]["value"])
    wx_1 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][6]["time"][0]["elementValue"][0]["value"])
    wx_2 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][6]["time"][1]["elementValue"][0]["value"])
    wx_3 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][6]["time"][2]["elementValue"][0]["value"])
    wx_4 = str(r["records"]["locations"][0]["location"][0]["weatherElement"][6]["time"][3]["elementValue"][0]["value"])
    if len(wx_1) < 6:
        wx_1_1 = wx_1[0:3]
        wx_1_2 = wx_1[3:]
        wx_1_3 = " "
        wx_1_4 = " "
    else:
        wx_1_1 = wx_1[0:3]
        wx_1_2 = wx_1[3:6]
        wx_1_3 = wx_1[6:]
        if len(wx_1_3) > 3:
            wx_1_3 = wx_1[6:9]
            wx_1_4 = wx_1[9:]
        else:
            wx_1_4 = " "
    if len(wx_2) < 6:
        wx_2_1 = wx_2[0:3]
        wx_2_2 = wx_2[3:]
        wx_2_3 = " "
        wx_2_4 = " "
    else:
        wx_2_1 = wx_2[0:3]
        wx_2_2 = wx_2[3:6]
        wx_2_3 = wx_2[6:]
        if len(wx_2_3) > 3:
            wx_2_3 = wx_2[6:9]
            wx_2_4 = wx_2[9:]
        else:
            wx_2_4 = " "
    if len(wx_3) < 6:
        wx_3_1 = wx_3[0:3]
        wx_3_2 = wx_3[3:]
        wx_3_3 = " "
        wx_3_4 = " "
    else:
        wx_3_1 = wx_3[0:3]
        wx_3_2 = wx_3[3:6]
        wx_3_3 = wx_3[6:]
        if len(wx_3_3) > 3:
            wx_3_3 = wx_3[6:9]
            wx_3_4 = wx_3[9:]
        else:
            wx_3_4 = " "
    if len(wx_4) < 6:
        wx_4_1 = wx_4[0:3]
        wx_4_2 = wx_4[3:]
        wx_4_3 = " "
        wx_4_4 = " "
    else:
        wx_4_1 = wx_4[0:3]
        wx_4_2 = wx_4[3:6]
        wx_4_3 = wx_4[6:]
        if len(wx_4_3) > 3:
            wx_4_3 = wx_4[6:9]
            wx_4_4 = wx_4[9:]
        else:
            wx_4_4 = " "
    bubble_container = []
    container = BubbleContainer(
        size="giga",
        body=BoxComponent(
            layout="vertical",
            margin="none",
            contents=[
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text=f"{city}", size="sm", margin="none"),
                        TextComponent(text=f"{rain_1_day}", size="sm"),
                        TextComponent(text=f"{rain_2_day}", size="sm"),
                        TextComponent(text=f"{rain_3_day}", size="sm"),
                        TextComponent(text=f"{rain_4_day}", size="sm"),
                    ],
                ),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text=f"{location}", size="sm", margin="none"),
                        TextComponent(text=f"{rain_1_daytime}", size="sm"),
                        TextComponent(text=f"{rain_2_daytime}", size="sm"),
                        TextComponent(text=f"{rain_3_daytime}", size="sm"),
                        TextComponent(text=f"{rain_4_daytime}", size="sm"),
                    ],
                ),
                SeparatorComponent(margin="sm"),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text="降雨機率", size="sm"),
                        TextComponent(text=f"{rain_1_po}%", size="sm"),
                        TextComponent(text=f"{rain_2_po}%", size="sm"),
                        TextComponent(text=f"{rain_3_po}%", size="sm"),
                        TextComponent(text=f"{rain_4_po}%", size="sm"),
                    ],
                ),
                SeparatorComponent(margin="sm"),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text="氣溫", size="sm"),
                        TextComponent(text=f"{temp_1}℃", size="sm"),
                        TextComponent(text=f"{temp_2}℃", size="sm"),
                        TextComponent(text=f"{temp_3}℃", size="sm"),
                        TextComponent(text=f"{temp_4}℃", size="sm"),
                    ],
                ),
                SeparatorComponent(margin="sm"),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text="風力", size="sm"),
                        TextComponent(text=f"{wind_1}", size="sm"),
                        TextComponent(text=f"{wind_2}", size="sm"),
                        TextComponent(text=f"{wind_3}", size="sm"),
                        TextComponent(text=f"{wind_4}", size="sm"),
                    ],
                ),
                SeparatorComponent(margin="sm"),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text="風向", size="sm"),
                        TextComponent(text=f"{wind_1_d}", size="sm"),
                        TextComponent(text=f"{wind_2_d}", size="sm"),
                        TextComponent(text=f"{wind_3_d}", size="sm"),
                        TextComponent(text=f"{wind_4_d}", size="sm"),
                    ],
                ),
                SeparatorComponent(margin="sm"),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text=" ", size="sm"),
                        TextComponent(text=f"{wx_1_1} ", size="sm"),
                        TextComponent(text=f"{wx_2_1} ", size="sm"),
                        TextComponent(text=f"{wx_3_1} ", size="sm"),
                        TextComponent(text=f"{wx_4_1} ", size="sm"),
                    ],
                ),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text="概況", size="sm"),
                        TextComponent(text=f"{wx_1_2} ", size="sm"),
                        TextComponent(text=f"{wx_2_2} ", size="sm"),
                        TextComponent(text=f"{wx_3_2} ", size="sm"),
                        TextComponent(text=f"{wx_4_2} ", size="sm"),
                    ],
                ),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text=" ", size="sm"),
                        TextComponent(text=f"{wx_1_3} ", size="sm"),
                        TextComponent(text=f"{wx_2_3} ", size="sm"),
                        TextComponent(text=f"{wx_3_3} ", size="sm"),
                        TextComponent(text=f"{wx_4_3} ", size="sm"),
                    ],
                ),
                BoxComponent(
                    layout="baseline",
                    margin="sm",
                    contents=[
                        TextComponent(text=" ", size="sm"),
                        TextComponent(text=f"{wx_1_4} ", size="sm"),
                        TextComponent(text=f"{wx_2_4} ", size="sm"),
                        TextComponent(text=f"{wx_3_4} ", size="sm"),
                        TextComponent(text=f"{wx_4_4} ", size="sm"),
                    ],
                ),
            ],
        ),
    )
    bubble_container.append(container)
    line_bot_api.reply_message(
        reply_token,
        FlexSendMessage(alt_text="Weather", contents=CarouselContainer(contents=bubble_container)),
    )


def wish(reply_token, user_id, user_name, message_text):
    models.pray_table.objects.create(user_id=user_id, user_name=user_name, pray_text=message_text)
    line_bot_api.reply_message(reply_token, TextSendMessage(text="願望收到囉 敬請期待"))


def hometown(reply_token, chat_room, message_text):
    try:
        point_num_request = int(message_text[9:])
    except Exception:
        point_num_request = "error"
    if message_text[8:] == "":
        hometown_day_info_list = models.hometown_day_info_table.objects.get(id=0)
        line_bot_api.reply_message(reply_token, TextSendMessage(text=hometown_day_info_list.day_info))
    elif message_text[9:] == "早班" or message_text[9:] == "中班" or message_text[9:] == "晚班" or message_text[9:] == "新進":
        shift_request = message_text[9:]
        hometown_info_list = models.hometown_info_table.objects.all().order_by("id")
        hometown_history_list = models.hometown_history_table.objects.all().order_by("id")
        bubble_container = []
        for item in hometown_info_list:
            image = item.url
            shift = item.shift
            point_num = item.id_num
            # real_working_time = item.time
            body_language = item.body
            introduction = item.info
            history_exp = " "
            for item in hometown_history_list:
                id_num = item.id_num
                history = item.history
                if str(point_num) == str(id_num):
                    history_exp = f"exp: {history}"
            # introduction_1 = " "
            # introduction_2 = " "
            # introduction_3 = " "
            # if len(introduction[:18]) > 0:
            #     introduction_1 = introduction[:18]
            # if len(introduction[18:36]) > 0:
            #     introduction_2 = introduction[18:36]
            # if len(introduction[36:]) > 0:
            #     introduction_3 = introduction[36:]
            if shift in shift_request:
                container = BubbleContainer(
                    size="giga",
                    hero=ImageComponent(
                        url=image,
                        size="full",
                        aspect_mode="cover",
                        action=URIAction(uri=image),
                    ),
                    body=BoxComponent(
                        layout="vertical",
                        margin="none",
                        contents=[
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{point_num}", size="sm"),
                                ],
                            ),
                            SeparatorComponent(margin="md"),
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{body_language}", size="sm"),
                                ],
                            ),
                            SeparatorComponent(margin="md"),
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{introduction}", size="sm", wrap=True),
                                ],
                            ),
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{history_exp}", size="sm", wrap=True),
                                ],
                            ),
                        ],
                    ),
                )
                bubble_container.append(container)
        working_total_num = len(bubble_container)
        quo = int(working_total_num / 10)
        remain = int(working_total_num % 10)
        for i in range(quo):
            if i == 0:
                reply_bubble_container = bubble_container[i * 10 : i * 10 + 10]
                line_bot_api.reply_message(
                    reply_token,
                    FlexSendMessage(
                        alt_text=shift_request,
                        contents=CarouselContainer(contents=reply_bubble_container),
                    ),
                )
            else:
                push_bubble_container = bubble_container[i * 10 : i * 10 + 10]
                line_bot_api.push_message(
                    chat_room,
                    FlexSendMessage(
                        alt_text=shift_request,
                        contents=CarouselContainer(contents=push_bubble_container),
                    ),
                )
        if remain != 0:
            push_bubble_container = bubble_container[quo * 10 :]
            line_bot_api.push_message(
                chat_room,
                FlexSendMessage(
                    alt_text=shift_request,
                    contents=CarouselContainer(contents=push_bubble_container),
                ),
            )
    elif str(point_num_request) != "error" and point_num_request < 10000:
        try:
            point_num_request = int(message_text[9:])
            try:
                hometown_info_list = models.hometown_info_table.objects.get(id_num=point_num_request)
            except Exception:
                hometown_info_list = "None"
            try:
                hometown_history_list = models.hometown_history_table.objects.get(id_num=point_num_request)
                hometown_history = hometown_history_list.history
            except Exception:
                hometown_history = ""
            if hometown_info_list != "None":
                bubble_container = []
                image = hometown_info_list.url
                shift = hometown_info_list.shift
                point_num = hometown_info_list.id_num
                # real_working_time = hometown_info_list.time
                body_language = hometown_info_list.body
                introduction = hometown_info_list.info
                history_exp = f"exp: {hometown_history}"
                # introduction_1 = " "
                # introduction_2 = " "
                # introduction_3 = " "
                # if len(introduction[:18]) > 0:
                #     introduction_1 = introduction[:18]
                # if len(introduction[18:36]) > 0:
                #     introduction_2 = introduction[18:36]
                # if len(introduction[36:]) > 0:
                #     introduction_3 = introduction[36:]
                container = BubbleContainer(
                    size="giga",
                    hero=ImageComponent(
                        url=image,
                        size="full",
                        aspect_mode="cover",
                        action=URIAction(uri=image),
                    ),
                    body=BoxComponent(
                        layout="vertical",
                        margin="none",
                        contents=[
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{point_num}", size="sm"),
                                ],
                            ),
                            SeparatorComponent(margin="md"),
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{body_language}", size="sm"),
                                ],
                            ),
                            SeparatorComponent(margin="md"),
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{introduction}", size="sm"),
                                ],
                            ),
                            BoxComponent(
                                layout="baseline",
                                margin="md",
                                contents=[
                                    TextComponent(text=f"{history_exp}", size="sm", wrap=True),
                                ],
                            ),
                        ],
                    ),
                )
                bubble_container.append(container)
                reply_bubble_container = bubble_container
                line_bot_api.reply_message(
                    reply_token,
                    FlexSendMessage(
                        alt_text=point_num,
                        contents=CarouselContainer(contents=reply_bubble_container),
                    ),
                )
            else:
                reply_text = "Number not exist !"
                line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))
        except Exception:
            pass
    else:
        pass


def IU_fans_info(reply_token):
    url = "https://drive.google.com/file/d/0B7BRqa5AOBuHSlR1YWZiMVFONXM/view?usp=sharing"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=url))


def reply_horoscope(reply_token, message_text):
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    Main_page = f"https://astro.click108.com.tw/daily_{horoscope_dict[message_text]}.php?iAcDay={today}&iAstro={horoscope_dict[message_text]}"
    r = requests.get(Main_page, headers=headers_hashtag)
    soup = BeautifulSoup(r.text, "html.parser")
    today_content = soup.find("div", class_="TODAY_CONTENT")
    msg = ""
    for thing in today_content:
        if str(type(thing)) != "<class 'bs4.element.NavigableString'>":
            msg = f"{msg}{thing.text}\n"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=msg))


def reply_weather(reply_token, message_text):
    if message_text == "radar":
        timestamp = datetime.datetime.now().timestamp() - 60 * 10
        date_time = datetime.datetime.fromtimestamp(timestamp)
        hour_now = date_time.strftime("%H")
        mins_now = date_time.strftime("%M")
        mins_now = f"{mins_now[:1]}0"
        today = date_time.strftime("%Y%m%d")
        today = f"{today}{hour_now}{mins_now}"
        log.info(today)
        url = f"https://www.cwa.gov.tw/Data/radar/CV1_3600_{today}.png"
        log.info(url)
        line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(original_content_url=url, preview_image_url=url),
        )
    elif message_text == "cloud":
        timestamp = datetime.datetime.now().timestamp() - 60 * 30
        date_time = datetime.datetime.fromtimestamp(timestamp)
        hour_now = date_time.strftime("%H")
        mins_now = date_time.strftime("%M")
        mins_now = f"{mins_now[:1]}0"
        today = date_time.strftime("%Y-%m-%d")
        today = f"{today}-{hour_now}-{mins_now}"
        url = f"https://www.cwa.gov.tw/Data/satellite/TWI_VIS_TRGB_1375/TWI_VIS_TRGB_1375-{today}.jpg"
        line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(original_content_url=url, preview_image_url=url),
        )
    elif message_text == "rain":
        timestamp = datetime.datetime.now().timestamp() - 60 * 20
        date_time = datetime.datetime.fromtimestamp(timestamp)
        hour_now = date_time.strftime("%H")
        mins_now = date_time.strftime("%M")
        mins_now = int(mins_now[:1])
        if mins_now > 3:
            mins_now = 3
        else:
            mins_now = 0
        mins_now = f"{mins_now}0"
        today = date_time.strftime("%Y-%m-%d")
        today = f"{today}_{hour_now}{mins_now}"
        url = f"https://www.cwa.gov.tw/Data/rainfall/{today}.QZT8.jpg"
        line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(original_content_url=url, preview_image_url=url),
        )
    elif message_text == "UV":
        url = "https://www.cwa.gov.tw/Data/UVI/UVI.png"
        line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(original_content_url=url, preview_image_url=url),
        )
    elif message_text == "temperature":
        timestamp = datetime.datetime.now().timestamp() - 60 * 30
        date_time = datetime.datetime.fromtimestamp(timestamp)
        hour_now = date_time.strftime("%H")
        mins_now = "00"
        today = date_time.strftime("%Y-%m-%d")
        today = f"{today}_{hour_now}{mins_now}"
        url = f"https://www.cwa.gov.tw/Data/temperature/{today}.GTP8.jpg"
        line_bot_api.reply_message(
            reply_token,
            ImageSendMessage(original_content_url=url, preview_image_url=url),
        )


def yt_one(reply_token, message_text):
    results = YoutubeSearch(message_text, max_results=10).to_dict()
    video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=video_url))


def reply_password_info(reply_token, search_keyword, user_id, chat_room):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    if user_id == admin_id and chat_room in IU_test:
        with open(f"{str(py_path)}/config/notion_config.json", encoding="utf-8") as f:
            config_json = json.load(f)
            notion_token = config_json["notion_info"]["token"]
            database_id = config_json["notion_info"]["database_id"]
        notion = Client(auth=notion_token)
        results = notion.databases.query(
            database_id,
            sorts=[{"property": "service", "direction": "ascending"}],
            filter={
                "or": [
                    {"property": "service", "rich_text": {"contains": search_keyword}},
                    {"property": "tag", "multi_select": {"contains": search_keyword}},
                ]
            },
        )
        reply_text = "Password Book\n\n"
        for result in results["results"]:
            service = result["properties"]["service"]["title"][0]["plain_text"]
            account = result["properties"]["account"]["rich_text"][0]["plain_text"]
            password = result["properties"]["password"]["rich_text"][0]["plain_text"]
            link = result["properties"]["link"]["rich_text"][0]["plain_text"]
            reply_text += f"{service}\n{account}\n{password}\n{link}\n\n"
        line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))
    else:
        pass


def add_password_info(reply_token, message_text):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    password_book_list = models.password_book.objects.all().order_by("id")
    id_num = password_book_list[password_book_list.count() - 1].id + 1
    service, account, password, link = message_text.split(" ")
    # data_dict = {
    #     "id": id_num,
    #     "service": f"{service}",
    #     "account": f"{account}",
    #     "password": f"{password}",
    #     "link": f"{link}",
    # }
    pw_saver = models.password_book(id=id_num, service=service, account=account, password=password, link=link)
    pw_saver.save()
    reply_text = "pw add ok"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))


def reply_line_buy(reply_token, message_text):
    reply_text = "Line 購物\n\n"
    if message_text == "TOP":
        line_buy_list = models.line_buy_table.objects.all().order_by("-point")
        top_list = line_buy_list[0:10]
        for item in top_list:
            reply_text = f"{reply_text}品牌: {item.name}\n回饋: {item.point}%\n網址: {item.url}\n\n"
    else:
        search_list = models.line_buy_table.objects.filter(name__contains=f"{message_text}")
        for item in search_list:
            reply_text = f"{reply_text}品牌: {item.name}\n回饋: {item.point}%\n網址: {item.url}\n\n"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))
    # line_bot_api.reply_message(reply_token,ImageSendMessage(original_content_url= url_out, preview_image_url=url_out))


def reply_test(reply_token, message_text, user_id, chat_room):
    if user_id == admin_id and chat_room in IU_test:
        if len(message_text) == 4:
            # output_url = f"{project_path}/media/tiktok/test1.mp4"
            # output_url = "https://iufans.club/warehouse/tiktok/1"
            # picture_url = "https://i.imgur.com/4sDRcxn.jpg"
            # reply_9gag(reply_token, chat_room, message_text)
            # output_url = ""
            # picture_url = ""
            # line_bot_api.reply_message(reply_token,VideoSendMessage(original_content_url=output_url,preview_image_url=picture_url))
            # line_bot_api.reply_message(reply_token,ImageSendMessage(original_content_url=output_url, preview_image_url=picture_url))
            # file_path = "/home/qma/mount/nas/98_車趟表_歷年安裝單/105年/06月/1050616.pdf"
            # return FileResponse(open(file_path, "rb"), content_type="application/pdf")
            line_bot_api.reply_message(reply_token, TextSendMessage(text="Test Ok Master"))
            # https://github.com/line/line-bot-sdk-python
            # user name
            # user_id = ""
            # group_id = ""
            # profile = line_bot_api.get_profile('')
            # print(profile.display_name)
            # print(profile.user_id)
            # print(profile.picture_url)
            # print(profile.status_message)
            # profile = line_bot_api.get_group_member_profile(group_id, user_id)
            # print(profile.display_name)
            # print(profile.user_id)
            # print(profile.picture_url)
            # profile = line_bot_api.get_room_member_profile(room_id, user_id)
            # print(profile.display_name)
            # print(profile.user_id)
            # print(profile.picture_url)
    elif len(message_text) == 4:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="Test Ok"))
    else:
        pass


def reply_qq_test(reply_token, message_text):
    sub_page = "https://www.instagram.com/p/CkkOxIOJAE_/"
    log.info(sub_page)
    headers_IG = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
        "cookie": 'ig_nrcb=1; ig_did=42521413-B3A9-4554-80C7-6C800E20109F; mid=Y1f5ngAEAAEBmpqoIooBpmrMZfu4; csrftoken=33LZX7Z3G2PGMtupb7DJoKAUeAbnR2F3; ds_user_id=1169657472; shbid="17185\0541169657472\0541699339712:01f70f9212fc4e2250b850bed36123029cf51a8dcbe8d77fe8e89483d7aaecda33e0eab4"; shbts="1667803712\0541169657472\0541699339712:01f7e39d35b9ecb82d3887ea4bdb859dc946739a68c91a40976a7c7b07a1c4268f72a710"; sessionid=1169657472%3AQ6UdEgAlSmleKK%3A5%3AAYd7E_xiCYZvOTO7gsWQfqZNjNz6QKc1Ajh0aEe22w; datr=YapoYyKa2IDSOJewOAR7irJR; rur="EAG\0541169657472\0541699339839:01f7738faec2bebf9a91f35b130aebf5f4a366fb7c87cb0bdfc9ecc388feb83964750091"',
        "referer": "https://www.instagram.com/p/CkkOxIOJAE_/?theme=dark",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "viewport-width": "1021",
    }

    r = requests.get(sub_page, headers_IG, timeout=10)
    log.info(r.text)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=message_text))


def reply_lunch_notification(reply_token, message_text):
    log.info(message_text)
    # url_test = "https://docs.google.com/forms/d/e/1FAIpQLSciRq_XY9MU2HouMIh4bkIzKVCWc-OhGfc59z61E-VgLO6dOw/viewform?usp=sf_link"
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe5jxs_7rCkhvqSDzUdInJs_cYsiEmzlOzFw7Q4p8KwJncP4A/viewform"
    form = Form()
    form.load(url)
    form_str = form.to_str(indent=2)
    # log.info(form_str)

    def callback(element, page_index, element_index):
        log.info(element.name)
        log.info(element_index)
        if element_index == 0:
            return "朱家進"
        if element_index == 1:
            return "26004"
        if element_index == 2:
            return "鴻海"
        if element_index == 4:
            return f"{lunch}"

    if len(message_text) > 3:
        log.info("ordering")
        lunch_index = int(message_text[3:])
        lunch_str = form_str[form_str.find("Radio") :]
        lunch_str = form_str[form_str.find("◯") :]
        # log.info(lunch_str)
        lunch_list = []
        lunch_counter = lunch_str.count("◯")
        lunch_search_num = 0
        for _ in range(lunch_counter):
            log.info(lunch_list)
            log.info(lunch_search_num)
            lunch_list.append(lunch_str[lunch_str.find("◯", lunch_search_num) + 2 : lunch_str.find("\n", lunch_str.find("◯", lunch_search_num))])
            lunch_search_num = lunch_str.find("◯", lunch_search_num) + 1
        lunch = lunch_list[lunch_index]
        log.info(lunch)
        form.fill(callback)
        log.info(form.submit())
        line_bot_api.reply_message(reply_token, TextSendMessage(text=f"ok: {lunch}"))
    else:
        line_bot_api.reply_message(reply_token, TextSendMessage(text=form_str))

    log.info(form_str)  # a text representation, may be useful for CLI applications
    # form.submit()
    # main reply function


def reply_gpt_ask(reply_token, message_text):
    log.info(f"function: {sys._getframe().f_code.co_name} start")
    log.info(message_text)
    model = "gpt-4"
    message = [
        {"role": "user", "content": f"{message_text}"},
    ]
    ask_token = num_tokens_from_messages(message, model)
    log.info(f"num_token = {ask_token}")
    if ask_token <= 2048:
        client = OpenAI(
            api_key=gpt_key,
        )
        completion = client.chat.completions.create(model=model, messages=message, max_tokens=50)
        reply_message = completion.choices[0].message.content
        log.info(completion.choices[0].message)
        log.info(completion.choices[0].message.content)
        line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_message))
    else:
        error_message = "Please contact admin for more information."
        line_bot_api.reply_message(reply_token, TextSendMessage(text=error_message))


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def privacy_policy(request):
    return HttpResponse(status=200, content="privacy_policy check")


def ig_api_webhook(request):
    string = "https://iufans.club/iu_server/line_bot_receive/ig_api_webhook?hub.mode=subscribe&hub.challenge=1596284&hub.verify_token=message_from_ig_app_1016"
    return HttpResponse(status=200, content=string)


def line_bot_receive(request):
    log.info(f"function: {sys._getframe().f_code.co_name}")
    request_dict = json.loads(request.body.decode("utf-8"))
    reply_token = request_dict["events"][0].get("replyToken")
    group_id = request_dict["events"][0]["source"].get("groupId", "None")
    room_id = request_dict["events"][0]["source"].get("roomId", "None")
    user_id = request_dict["events"][0]["source"].get("userId")
    events_timestamp = request_dict["events"][0].get("timestamp")
    message_type = request_dict["events"][0]["message"].get("type")
    message_text = request_dict["events"][0]["message"].get("text", "None")
    if message_text == "None":
        message_text = f"{str(message_type)}_{str(events_timestamp)}"
    if group_id != "None":
        chat_room = group_id
        profile = line_bot_api.get_group_member_profile(group_id, user_id)
        user_name = profile.display_name
        models.user_info_table.objects.get_or_create(
            user_id=user_id,
            defaults={
                "user_name": user_name,
            },
        )
    elif room_id != "None":
        chat_room = room_id
        profile = line_bot_api.get_room_member_profile(room_id, user_id)
        user_name = profile.display_name
        models.user_info_table.objects.get_or_create(
            user_id=user_id,
            defaults={
                "user_name": user_name,
            },
        )
    else:
        chat_room = user_id
        profile = line_bot_api.get_profile(user_id)
        user_name = profile.display_name
        models.user_info_table.objects.get_or_create(
            user_id=user_id,
            defaults={
                "user_name": user_name,
            },
        )
    log.info(f"{user_name} : {message_text}")
    db_update_chat_log(user_id, user_name, chat_room, message_text)

    # check text message
    if message_type == "text":
        # Help information
        if message_text.upper() == "HELP" or message_text.upper() == "-H":  # Help for IU
            reply_help(reply_token)
        # keyword list
        elif message_text.upper() == "-H KEYWORD":
            reply_help_keyword(reply_token)
        # sticker by keyword https://developers.line.biz/media/messaging-api/sticker_list.pdf
        elif message_text.upper() in sticker_dict:
            message_text = message_text.upper()
            reply_sticker(reply_token, message_text)
        # picture by keyword
        elif message_text.upper() in keyword_dict or message_text.upper().replace("瑟瑟", "色色") in dog_dict or message_text[0:2] == "警察" or message_text.upper() == "KI的最愛":
            message_text = message_text.upper().replace("瑟瑟", "色色")
            if message_text == "KI的最愛":
                reply_text = keyword_dict["Ki的最愛"]
                line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))
            elif message_text[0:2] == "警察":
                if message_text[3:].upper() == "ANN" or message_text[3:].upper() == "安":
                    message_text = "警察_ann"
                elif message_text[3:].upper() == "馬克":
                    message_text = "警察_chu"
                elif message_text[3:].upper() == "KIKI":
                    message_text = "警察_kiki"
                elif message_text[3:].upper() == "映孜":
                    message_text = "警察_shadow"
                elif message_text[3:].upper() == "大屁":
                    message_text = "警察_pi"
                else:
                    message_text = "警察"
                reply_keyword(reply_token, message_text)
            else:
                reply_keyword(reply_token, message_text)
        # picture by dog keyword
        elif message_text.replace("瑟瑟", "色色") == "色色":
            reply_dog_card(reply_token)
        # video by porn keyword
        elif message_text[0:5].upper() == "PORN ":
            message_text = message_text[5:]
            reply_porn(reply_token, message_text)
        # reply xvideos
        elif message_text[0:23] == "https://www.xvideos.com":
            reply_xvideos(reply_token, message_text)
        # douyin
        elif message_text.find("douyin.com") != -1:
            reply_douyin(reply_token, message_text)
        # tiktok
        elif message_text.find("tiktok.com") != -1:
            reply_tiktok(reply_token, message_text)
        # # instagram
        elif message_text.find("instagram") != -1:
            # if user_id == admin_id:
            reply_IG(reply_token, chat_room, message_text)
        # # 5 picture of hasgtag on IG
        # elif message_text[0:1] == "#" and message_text[1:] != "":
        #     message_text = message_text[1:]
        #     reply_hashtag(reply_token, message_text)
        # Facebook
        elif message_text[0:25] == "https://www.facebook.com/":
            message_text = message_text.strip("\n")
            reply_fb(reply_token, message_text)
        # Youtube
        elif message_text.find("youtu") != -1:
            reply_youtube(reply_token, message_text)
        # MoPtt or Ptt image
        elif message_text.find("moptt") != -1 or message_text.find("www.ptt.cc") != -1:
            reply_ptt(reply_token, message_text)
        # Twitter
        elif message_text.find("twitter.com") != -1:
            reply_twitter(reply_token, message_text)
        # Imgur
        elif message_text.find("imgur.com") != -1:
            reply_imgur(reply_token, message_text)
        # call IU love list
        elif message_text.upper() == "IUU" or message_text.upper() == "UUU":
            IU_call_love_list(reply_token, chat_room)
        # call IU random list
        elif message_text.upper() == "IU" or message_text.upper() == "UU":
            IU_call_random_pic(reply_token)
        # yuyan
        elif message_text == "彭于晏":
            reply_yuyan(reply_token)
        # double word picture
        elif message_text.upper() == "MM" or message_text.upper() == "PP" or message_text.upper() == "OO" or message_text.upper() == "CC":
            message_text = message_text.upper()
            reply_double_word_pic(reply_token, message_text)
        # 9gag
        elif message_text.upper() == "9FUN" or message_text.upper() == "9GIRL" or message_text.upper() == "9HOT" or message_text.upper() == "99" or message_text.upper() == "98":
            message_text = message_text.upper()
            # if message_text == "9GIRL" and user_id not in IU_fans_club:
            #     message_text ="9FUN"
            # if message_text == "9HOT" and user_id not in IU_fans_club:
            #     message_text ="9FUN"
            if message_text == "99" and (user_id in IU_fans_club or user_id in spirit_chamber):
                message_text = "9GIRL"
            if message_text == "98" and (user_id in IU_fans_club or user_id in spirit_chamber):
                message_text = "9HOT"
            reply_9gag(reply_token, message_text)
        # call ccc
        elif message_text.upper() == "CCC":
            reply_for_ccc(reply_token)
        # call cccc
        elif message_text.upper() == "MAN":
            reply_for_man(reply_token)
        # call google translater
        elif (message_text[0:2] == "字典" and message_text[2] == " ") or (message_text[0:4].lower() == "dict" and message_text[4] == " "):
            if message_text[0:2] == "字典":
                dict_translator(reply_token, message_text[3:])
            else:
                dict_translator(reply_token, message_text[5:])
        # IU Weather
        elif len(message_text) <= 6 and "天氣" in message_text:
            weather(reply_token, message_text)
        # youtube song
        elif message_text[:3] == "來一首" or message_text[:3] == "點一首" or message_text[:2] == "點播" or message_text[:2] == "點首" or message_text[:2] == "點歌" or message_text[:2] == "來首":
            if message_text[:3] == "來一首" or message_text[:3] == "點一首":
                message_text = message_text[3:]
            else:
                message_text = message_text[2:]
            yt_one(reply_token, message_text)
        # 12 horoscope
        elif message_text in horoscope_dict:
            reply_horoscope(reply_token, message_text)
        # weather report
        elif message_text in weather_dict:
            message_text = weather_dict[message_text]
            reply_weather(reply_token, message_text)
        # wish list
        elif message_text[0:2] == "許願" and message_text[2:] != "":
            message_text = message_text[2:]
            wish(reply_token, user_id, user_name, message_text)
        # hometown list
        elif message_text[0:8].upper() == "HOMETOWN":
            if user_id in IU_fans_club and (chat_room in permission_dict_chat_room_hometown or chat_room in legend_family):
                hometown(reply_token, chat_room, message_text)
            else:
                pass
        # Line buy point
        elif message_text[0:8].upper() == "LINE BUY":
            if len(message_text) == 8:
                message_text = "TOP"
            else:
                message_text = message_text[9:]
            reply_line_buy(reply_token, message_text)
        # IU fans club function
        elif message_text.upper() == "IU粉汁":
            if user_id in IU_fans_club and chat_room in IU_fans_club_chat_room:
                IU_fans_info(reply_token)
        # password table
        elif message_text[0:2].upper() == "PW":
            if user_id == admin_id:
                if message_text[3:6].upper() == "ADD":
                    message_text = message_text[7:]
                    add_password_info(reply_token, message_text)
                else:
                    message_text = message_text[3:].upper()
                    reply_password_info(reply_token, message_text, user_id, chat_room)
        # protect mode
        elif message_text == ".." or message_text.upper() == "...":
            reply_text = ""
            for _ in range(50):
                reply_text = f"{reply_text}.\n"
            line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_text))
        # test mode
        elif message_text[0:4].upper() == "TEST":
            reply_test(reply_token, message_text, user_id, chat_room)
        # qq test mode
        elif message_text == "qq" and user_id == admin_id:
            reply_qq_test(reply_token, message_text)
        # login ig
        elif message_text[0:2] == "午餐" and user_id == admin_id and chat_room in IU_test:
            reply_lunch_notification(reply_token, message_text)
        # ask gpt
        elif message_text[0:4].upper() == "GPT ":
            message_text = message_text[4:]
            reply_gpt_ask(reply_token, message_text)
        # all else pass
        else:
            pass
    # if image message
    elif message_type == "image":
        pass
        # message_time = events_timestamp
        # # print(f'{user_name} : image {message_time}')
        # message_content = line_bot_api.get_message_content(message_id)
        # with open(f"{project_path}/media/{events_timestamp}.jpg", "wb") as fd:
        #     for chunk in message_content.iter_content():
        #         fd.write(chunk)
    # if video message
    elif message_type == "video":
        pass
        # message_time = events_timestamp
        # # print(f'{user_name} : video {message_time}')
        # message_content = line_bot_api.get_message_content(message_id)
        # with open(f"{project_path}/media/{message_time}.mp4", "wb") as fd:
        #     for chunk in message_content.iter_content():
        #         fd.write(chunk)
    # if audio message
    elif message_type == "audio":
        pass
        # message_time = events_timestamp
        # # print(f'{user_name} : audio {message_time}')
        # message_content = line_bot_api.get_message_content(message_id)
        # with open(f"{project_path}/media/{message_time}.m4a", "wb") as fd:
        #     for chunk in message_content.iter_content():
        #         fd.write(chunk)
    # any other message
    else:
        log.info(f"message_type: {message_type}")
    return HttpResponse(status=200)
