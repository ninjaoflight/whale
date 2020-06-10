from flask_login import UserMixin

from db import get_db


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id, auth_type = "basic"):
        db = get_db()
        user = None
        if auth_type == "basic":  # recuperar el usuario justo como en el placeholder
            user = db.execute(
                "SELECT * FROM usuario WHERE id = ?", (user_id,)
            ).fetchone()
            if user:
                user = User(
                    id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
                )
        elif auth_type == "gauth": #recuperar mediante login de google
            user_id = db.execute(
                "select id from gcreds where openid = ?", (user_id,)
            ).fetchone()
            if user_id:
                user = User.get(user_id[0])
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, auth_type="basic"):
        db = get_db()
        if auth_type == "basic":
            db.execute(
                "INSERT INTO usuario (id, nombre, email, foto_perfil)"
                " VALUES (?, ?, ?, ?)",
                (id_, name, email, profile_pic),
            )
            db.execute(
                "INSERT INTO credenciales (id, pass)"
                " VALUES (?, ?)",
                (id_, "1234"),
            )

        elif auth_type == "gauth":
            db.execute(
                "INSERT INTO usuario (id, nombre, email, foto_perfil)"
                " VALUES (?, ?, ?, ?)",
                (email, name, email, profile_pic),
            )
            db.execute(
                "INSERT INTO gcreds (openid, id)"
                " VALUES (?, ?)",
                (id_, email),
            )
            db.execute(
                "INSERT INTO credenciales (id, pass)"
                " VALUES (?, ?)",
                (email, "1234"),
            )

        db.commit()
