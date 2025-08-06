import requests
import json
from datetime import datetime
import os

def get_wall_posts(owner_id, access_token, count=100):
    """
    Получение постов со стены пользователя/группы
    owner_id: ID пользователя
    """
    url = "https://api.vk.com/method/wall.get"
    
    params = {
        'owner_id': owner_id,
        'count': count,
        'access_token': access_token,
        'v': '5.131'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'response' in data:
        posts = data['response']['items']
        
        posts_info = []
        for post in posts:
            post_info = {
                'id': post['id'],
                'date': datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S'),
                'text': post['text'][:100] + '...' if len(post['text']) > 100 else post['text'],
                'likes': post['likes']['count'],
                'comments': post['comments']['count'],
                'reposts': post['reposts']['count'],
                'views': post['views']['count'] if 'views' in post else 0
            }
            posts_info.append(post_info)
        
        return posts_info
    else:
        print(f"Ошибка: {data}")
        return []


owner_id = 292394399  # ID пользователя
access_token = ""

posts = get_wall_posts(owner_id, access_token)

# Сохранение в CSV
import pandas as pd
df = pd.DataFrame(posts)
df.to_csv('vk_posts.csv', index=False, encoding='utf-8')