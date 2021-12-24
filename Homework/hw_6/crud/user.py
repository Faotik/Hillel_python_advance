from hashlib import sha256
from core.models.userModels import RegistrationModel, UserModel
import sqlite3
import uuid
from core import password_hashing
from werkzeug.datastructures import Authorization
from core.errors.errors import AuthError, UserExistsError, UserFollowError


class UserCRUD:
    def create(self, conn: sqlite3.Connection, data: RegistrationModel) -> None:
        cur = conn.cursor()

        try:
            if self.user_is_exist(conn, data.login) is not False:
                raise UserExistsError(f"User with login {data.login} already exists")

            user_id = uuid.uuid4()

            password_manager = password_hashing.PasswordHandler("sha256", 32)

            cur.execute(
                "INSERT INTO User VALUES(?, ?, ?)",
                (str(user_id), data.login, password_manager.hash_password(data.password))
            )
        finally:
            cur.close()

    def authenticate(self, conn: sqlite3.Connection, auth_data: Authorization) -> None:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT password FROM User WHERE login = ?", (auth_data.username,)
            )
            row = cur.fetchone()

            if row is None:
                raise AuthError("Unknown user")

            password_manager = password_hashing.PasswordHandler("sha256", 32)

            if not password_manager.verify_password(auth_data.password, row[0]):
                raise AuthError("Wrong password")

        finally:
            cur.close()

    def user_data_by_login(self, conn: sqlite3.Connection, login: str) -> UserModel:
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT User.id, User.login, COUNT(DISTINCT follow.follow), COUNT(DISTINCT follower.follower)
                    FROM User
                    LEFT JOIN Follow AS follower ON follower.follow=User.id
                    LEFT JOIN Follow AS follow ON follow.follower=User.id
                    WHERE User.login=?
                    GROUP BY User.id""", (login,)
            )
            row = cur.fetchone()

            if row is None:
                raise AuthError("Unknown user")

            _id, _login, _follow, _follower = row

            return UserModel(id=_id, login=_login, follower=_follower, follow=_follow)

        finally:
            cur.close()

    def user_data_by_id(self, conn: sqlite3.Connection, id: str) -> UserModel:
        cur = conn.cursor()
        try:
            cur.execute(
                """SELECT User.id, User.login, COUNT(DISTINCT follow.follow), COUNT(DISTINCT follower.follower)
                    FROM User
                    LEFT JOIN Follow AS follower ON follower.follow=User.id
                    LEFT JOIN Follow AS follow ON follow.follower=User.id
                    WHERE User.id=?
                    GROUP BY User.id""", (id,)
            )
            row = cur.fetchone()

            if row is None:
                raise AuthError("Unknown user")

            _id, _login, _follow, _follower = row

            return UserModel(id=_id, login=_login, follower=_follower, follow=_follow)

        finally:
            cur.close()

    def user_is_exist(self, conn: sqlite3.Connection, login: str) -> bool:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT * FROM User WHERE Login = ?", (login,)
            )
            row = cur.fetchone()

            if row is None:
                return False
            return True
        finally:
            cur.close()

    def follow_is_exist_by_id(self, conn: sqlite3.Connection, follower_id: str, follow_id: str) -> bool:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT Follow.id FROM Follow WHERE follow = ? AND follower = ?", (
                    follow_id, follower_id)
            )
            row = cur.fetchone()

            if row is None:
                return False
            return True
        finally:
            cur.close()

    def follow_user_is_exist(self, conn: sqlite3.Connection, login: str, follow_login: str) -> bool:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT User.id FROM User WHERE login = ?", (login,)
            )
            row = cur.fetchone()

            if row is None:
                return False

            cur.execute(
                "SELECT User.id FROM User WHERE login = ?", (follow_login,)
            )
            row = cur.fetchone()
            if row is None:
                return False

            return True
        finally:
            cur.close()

    def follow(self, conn: sqlite3.Connection, login: str, follow_login: str):
        cur = conn.cursor()

        try:
            if(login == follow_login):
                raise UserFollowError(
                    f"User {login}, can not follow self")
            if self.follow_user_is_exist(conn, login, follow_login) is False:
                raise UserExistsError(
                    f"User {login}, or user {follow_login} is not exist")

            follower_user_id = self.user_data_by_login(conn, login).id
            follow_user_id = self.user_data_by_login(conn, follow_login).id

            if self.follow_is_exist_by_id(conn, follower_user_id, follow_user_id) is True:
                raise UserFollowError(
                    f"User {login} already follow {follow_login}")

            follow_id = uuid.uuid4()

            cur.execute(
                "INSERT INTO Follow VALUES(?, ?, ?)",
                (str(follow_id), follower_user_id, follow_user_id)
            )
        finally:
            cur.close()

    def unfollow(self, conn: sqlite3.Connection, login: str, unfollow_login: str):
        cur = conn.cursor()

        try:
            if(login == unfollow_login):
                raise UserFollowError(
                    f"User {login}, can not unfollow self")
            if self.follow_user_is_exist(conn, login, unfollow_login) is False:
                raise UserExistsError(
                    f"User {login}, or user {unfollow_login} is not exist")

            follower_user_id = self.user_data_by_login(conn, login).id
            follow_user_id = self.user_data_by_login(conn, unfollow_login).id

            if self.follow_is_exist_by_id(conn, follower_user_id, follow_user_id) is False:
                raise UserFollowError(
                    f"User {login} is not follow {unfollow_login}")

            cur.execute(
                "DELETE FROM Follow WHERE Follow.follower = ? AND Follow.follow = ?",
                (follower_user_id, follow_user_id)
            )
        finally:
            cur.close()

    def get_follows(self, conn: sqlite3.Connection, login: str):
        cur = conn.cursor()

        try:
            if self.user_is_exist(conn, login) is False:
                raise UserExistsError(
                    f"User {login} is not exist")
            follower_user_id = self.user_data_by_login(conn, login).id

            cur.execute(
                "SELECT Follow.follow FROM Follow WHERE Follow.follower = ?", (
                    follower_user_id,)
            )
            row = cur.fetchall()
            users = []
            for r in row:
                users.append(self.user_data_by_id(conn, r[0]).login)

            return users
        finally:
            cur.close()

    def get_follower(self, conn: sqlite3.Connection, login: str):
        cur = conn.cursor()

        try:
            if self.user_is_exist(conn, login) is False:
                raise UserExistsError(
                    f"User {login} is not exist")
            follow_user_id = self.user_data_by_login(conn, login).id

            cur.execute(
                "SELECT Follow.follower FROM Follow WHERE Follow.follow = ?", (
                    follow_user_id,)
            )
            row = cur.fetchall()
            users = []
            for r in row:
                users.append(self.user_data_by_id(conn, r[0]).login)

            return users
        finally:
            cur.close()
