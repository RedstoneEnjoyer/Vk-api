import json
from datetime import datetime

import requests
import time

# Лимит на число выгруженных строк
LIMIT = 10000

def get_wall_posts(owner_id, access_token, count=100, max_posts=None):
    """
    Получение постов со стены пользователя/группы с поддержкой пагинации
    owner_id: ID пользователя/группы
    access_token: токен доступа
    count: количество постов за один запрос (максимум 100)
    max_posts: максимальное количество постов для получения (None = все доступные)
    """
    url = "https://api.vk.com/method/wall.get"
    all_posts = []
    offset = 0
    
    while offset < LIMIT:
        print(int(offset/100))
        params = {
            'owner_id': owner_id,
            'count': min(count, 100),  # VK API позволяет максимум 100 за раз
            'offset': offset,
            'access_token': access_token,
            'v': '5.131'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'response' not in data:
            print(f"Ошибка: {data}")
            break
            
        posts = data['response']['items']
        
        # Если постов нет, выходим из цикла
        if not posts:
            break
            
        # Обрабатываем посты
        for post in posts:
            post_info = {
                'id': post['id'],
                'date': datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S'),
                'likes': post['likes']['count'],
                'comments': post['comments']['count'],
                'reposts': post['reposts']['count'],
                'views': post['views']['count'] if 'views' in post else 0
            }
            all_posts.append(post_info)
            
            # Если достигли максимального количества постов, останавливаемся
            if max_posts and len(all_posts) >= max_posts:
                return all_posts[:max_posts]
        
        # Увеличиваем смещение для следующего запроса
        offset += len(posts)
        
        # Если получили меньше постов, чем запрашивали, значит это все посты
        if len(posts) < count:
            break
            
        # Небольшая задержка между запросами для соблюдения лимитов API
        time.sleep(0.1)
    
    return all_posts

import os

import pandas as pd

owner_id = 'hnnnnnnnnnnnnnnnn'  # id пользователя/группы
access_token = os.getenv("VK_TOKEN")

posts = get_wall_posts(owner_id, access_token)

# Сохранение в CSV
df = pd.DataFrame(posts)
df.to_csv('data/posts.csv', index=False, encoding='utf-8')


import sqlite3


conn = sqlite3.connect('sqlite/default.db')

# Сохранение датафрейма в базу данных
df.to_sql('posts', conn, if_exists='replace', index=False)

conn.close()
