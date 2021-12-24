from typing import Mapping
from core.models.postModel import CreatePostModel, PostModel
import sqlite3
import uuid
from core.errors.errors import PostExistsError, AccessError, UserExistsError
from .user import UserCRUD
from datetime import datetime

user_crud = UserCRUD()


class PostCRUD:
    def create(self, conn: sqlite3.Connection, data: CreatePostModel) -> None:
        cur = conn.cursor()

        try:
            post_id = uuid.uuid4()

            creater_id = user_crud.user_data_by_login(conn, data.creater).id

            cur.execute(
                "INSERT INTO Post VALUES(?, ?, ?, ?, ?)",
                (str(post_id), data.title,
                 data.description, creater_id, datetime.now())
            )
        finally:
            cur.close()

    def post_is_exist(self, conn: sqlite3.Connection, post_id: str) -> bool:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT * FROM Post WHERE Post.id = ?", (post_id,)
            )
            row = cur.fetchone()

            if row is None:
                return False
            return True
        finally:
            cur.close()

    def user_is_post_creater(self, conn: sqlite3.Connection, post_id: str, login: str) -> bool:
        cur = conn.cursor()
        try:
            creater_id = user_crud.user_data_by_login(conn, login).id

            cur.execute(
                "SELECT * FROM Post WHERE Post.id = ? AND Post.creater = ?", (
                    post_id, creater_id)
            )
            row = cur.fetchone()

            if row is None:
                return False
            return True
        finally:
            cur.close()

    def delete(self, conn: sqlite3.Connection, post_id: str, login: str):
        cur = conn.cursor()

        try:
            if self.post_is_exist(conn, post_id) is False:
                raise PostExistsError(
                    f"Post {post_id} is not exist")

            if self.user_is_post_creater(conn, post_id, login) is False:
                raise AccessError(
                    f"User {login} is not post creater"
                )

            cur.execute(
                "DELETE FROM Post WHERE Post.id = ?", (post_id,)
            )
        finally:
            cur.close()

    def get(self, conn: sqlite3.Connection, login: str):
        cur = conn.cursor()

        try:
            if user_crud.user_is_exist(conn, login) is False:
                raise UserExistsError(
                    f"User {login} is not exist")

            user_id = user_crud.user_data_by_login(conn, login).id

            cur.execute(
                "SELECT * FROM Post WHERE Post.creater = ? ORDER BY Post.create_date DESC", (
                    user_id,)
            )
            row = cur.fetchall()
            posts = []
            for r in row:
                posts.append(PostModel(id=r[0], title=r[1], description=r[2], creater=r[3], create_date=r[4]))

            return posts
        finally:
            cur.close()

    def get_follows_post(self, conn: sqlite3.Connection, login: str):
        cur = conn.cursor()

        try:
            if user_crud.user_is_exist(conn, login) is False:
                raise UserExistsError(
                    f"User {login} is not exist")

            user_id = user_crud.user_data_by_login(conn, login).id

            cur.execute(
                """SELECT Post.id, Post.title, Post.description, Post.creater, Post.create_date FROM Post
                WHERE Post.creater IN (SELECT Follow.follow FROM Follow WHERE Follow.follower=?)
                ORDER BY Post.create_date DESC""", (
                    user_id,)
            )
            row = cur.fetchall()
            posts = []
            for r in row:
                posts.append(PostModel(
                    id=r[0], title=r[1], description=r[2], creater=r[3], create_date=r[4]))

            return posts
        finally:
            cur.close()
