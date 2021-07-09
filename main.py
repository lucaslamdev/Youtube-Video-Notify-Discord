import requests
import datetime
import json, urllib
import time


def videocheck():
    api_key = 'YOUTUBE-DATA-V3-API-KEY'
    channelId = 'CHANNEL-ID'

    print('Pegando dados de vídeos!')

    base_url = 'https://www.googleapis.com/youtube/v3/search?'
    url_video_check = base_url + f'key={api_key}&channelId={channelId}&part=snippet,id&order=date&fields=items&maxResults=1'
    respostas = requests.get(url_video_check)
    respostas_json = respostas.json()
    youtube_videoId = respostas_json['items'][0]['id']['videoId']
    youtube_channelName = respostas_json['items'][0]['snippet']['channelTitle']
    youtube_videoTitle = respostas_json['items'][0]['snippet']['title']

    print(
        f'Dados: videoId={youtube_videoId}, channel_name={youtube_channelName}, video_title={youtube_videoTitle}'
    )

    video_exists = False
    with open('videoid.json', 'r') as json_file:
        data = json.load(json_file)
        if data['videoId'] != youtube_videoId:
            video_exists = True
            base_url_logoGrab = 'https://www.googleapis.com/youtube/v3/channels?'
            url_logo_grab = base_url_logoGrab + f'part=snippet,id&fields=items&id={channelId}&key={api_key}'
            respostas_logo = requests.get(url_logo_grab)
            respostas_logo_json = respostas_logo.json()
            youtube_logo_url = respostas_logo_json['items'][0]['snippet'][
                'thumbnails']['high']['url']
            print(f'Logo URL: {youtube_logo_url}')
            sendwebhook(youtube_videoId, youtube_channelName,
                        youtube_videoTitle, youtube_logo_url, channelId)
    if video_exists:
        with open('videoid.json', 'w') as json_file:
            data = {'videoId': youtube_videoId}
            json.dump(data, json_file)
            print(video_exists)


def sendwebhook(youtube_videoId, youtube_channelName, youtube_videoTitle,
                youtube_logo_url, channelId):
    urls_webhook = [
        'LINK-1-WEBHOOK',
        'LINK-2-WEBHOOK'
    ]
    username_webhook_discord = 'Youtube Video'
    avatar_logo = 'https://i.imgur.com/afCWfn4.png'
    title_message = youtube_videoTitle
    channel_logo = youtube_logo_url
    channel_name = youtube_channelName
    channel_url = f'https://www.youtube.com/channel/{channelId}'
    video_title = youtube_videoTitle
    video_url = f'https://www.youtube.com/watch?v={youtube_videoId}'
    get_timestamp = str(datetime.datetime.today())
    separator = 'https://i.imgur.com/PMY3Lts.gif'

    data = {"username": username_webhook_discord, "avatar_url": avatar_logo}
    data2 = {
        "username": username_webhook_discord,
        "avatar_url": avatar_logo,
        "content": video_url
    }
    data3 = {
        "username": username_webhook_discord,
        "avatar_url": avatar_logo,
        "content": "@everyone"
    }
    data4 = {
        "username": username_webhook_discord,
        "avatar_url": avatar_logo,
        "content": separator
    }

    data["embeds"] = [{
        "color": "1752220",
        "title": "Video Novo!",
        "url": video_url,
        "author": {
            "name": channel_name,
            "url": channel_url
        },
        "thumbnail": {
            "url": channel_logo
        },
        "description": video_title,
        "fields": [{
            "name": 'Video Link:',
            "value": video_url
        }],
        "timestamp": get_timestamp
    }]

    i = 0
    print('####################')
    for x in urls_webhook:
        print(f'-------WebHook_Num={i}----------')
        result = requests.post(urls_webhook[i], json=data)
        time.sleep(1)
        print(result)
        result = requests.post(urls_webhook[i], json=data2)
        print(result)
        result = requests.post(urls_webhook[i], json=data3)
        print(result)
        result = requests.post(urls_webhook[i], json=data4)
        print(result)
        i = i + 1
    print('####################')


def main():
    while True:
        print('Entrando no videocheck!')
        videocheck()
        time.sleep(910)


main()
