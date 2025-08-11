from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20))
    lastname: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    followers: Mapped[List["Follower"]] = relationship("Follower", back_populates="followed", foreign_keys="[Follower.followed_id]")
    following: Mapped[List["Follower"]] = relationship("Follower", back_populates="follower", foreign_keys="[Follower.follower_id]")

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    image: Mapped[str] = mapped_column(String(120))
    caption: Mapped[str] = mapped_column(String(120))
    
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    media_items: Mapped[List["Media"]] = relationship(back_populates="post")
    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column(String(120))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    
    post: Mapped["Post"] = relationship(back_populates="media_items")

class Follower(db.Model):
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    
    follower: Mapped["User"] = relationship("User", back_populates="following", foreign_keys=[follower_id])
    followed: Mapped["User"] = relationship("User", back_populates="followers", foreign_keys=[followed_id])