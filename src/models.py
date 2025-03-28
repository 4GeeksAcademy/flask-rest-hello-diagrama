import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    profile_pic = Column(String(300))
    bio = Column(Text)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    followers = relationship("Follower", foreign_keys="[Follower.followed_id]", back_populates="followed")
    following = relationship("Follower", foreign_keys="[Follower.follower_id]", back_populates="follower")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(300), nullable=False)
    caption = Column(Text)
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
   
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uq_like_user_post'),
    )

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    followed_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
    
    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id', name='uq_follower_followed'),
    )


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e