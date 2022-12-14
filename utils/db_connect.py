import asyncpg
import psycopg_pool
from typing import List
from asyncpg import Record


class Request:
    def __init__(self, connector: psycopg_pool.AsyncConnectionPool.connection):
        self.connector = connector

    async def add_user(self, user_id, user_name, chat_id, login_time):
        query = f"INSERT INTO users (user_id, user_name, chat_id, login_time) VALUES ({user_id}, '{user_name}', {chat_id}, '{login_time}') " \
                f"ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)

    async def select_all_memes(self):
        query = f"SELECT * FROM memes"
        memes_list = await self.connector.execute(query).fetchall()
        return memes_list
