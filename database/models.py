from sqlalchemy import Column, ForeignKey, JSON, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    # authorization_id = Column(Integer, ForeignKey("authorizations.id"))
    nickname = Column(String, unique=True)
    name = Column(String)
    surname = Column(String)
    grade = Column(String)
    contacts = Column(JSON, default=None)
    description = Column(String, default=None)
    avatar_uuid = Column(UUID, default=None)
    is_admin = Column(Boolean, default=False)
    is_teacher = Column(Boolean, default=False)

    tags = relationship("Tag", backref="user")
    fav_colabs = relationship("FavColab", backref="user")
    fav_archives = relationship("FavArchive", backref="user")
    # fav_users = relationship("FavUser", foreign_keys="FavUser.user_id")


class Authorization(Base):
    __tablename__ = "authorizations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, unique=True)
    nickname = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    hashed_password = Column(String)

    user = relationship("User", backref="authorization")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tag = Column(String)


class FavColab(Base):
    __tablename__ = "favourite_colab"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    colab_id = Column(Integer)


class FavArchive(Base):
    __tablename__ = "favourite_archive"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    archive_id = Column(Integer)


class FavUser(Base):
    __tablename__ = "favourite_user"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    fav_user_id = Column(Integer, ForeignKey("users.id"))

    main_user = relationship("User", foreign_keys=[user_id], backref="fav_users")
    fav_user = relationship("User", foreign_keys=[fav_user_id])


# Лучше использовать список всех контактов сразу у юзера.
# class Contact(Base):
#     __tablename__ = "contacts"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     contact = Column(String)
