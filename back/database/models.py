from sqlalchemy import Column, String, Integer, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from database.database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)

    name = Column(String)
    email = Column(String, unique=True)
    image = Column(String)
    hashed_password = Column(String)

    posts = relationship("Posts", back_populates="author", uselist=True)
    comments = relationship("Comments", back_populates="author", uselist=True)
    likes = relationship("Likes", back_populates="author", uselist=True)
    user_external_map = relationship("UserExternalMapping")


class Posts(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, Sequence("post_id_seq"), primary_key=True)

    author_id = Column(String, ForeignKey("users.user_id"), nullable=False)

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)

    like_count = Column(Integer, default=0, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)

    author = relationship("Users", back_populates="posts")
    comments = relationship("Comments", back_populates="post", uselist=True)
    likes = relationship("Likes", back_populates="post", uselist=True)


class Comments(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, Sequence("comment_id_seq"), primary_key=True)

    author_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)

    content = Column(String, nullable=False)

    author = relationship("Users", back_populates="comments")
    post = relationship("Posts", back_populates="comments")


class Likes(Base):
    __tablename__ = "likes"

    author_id = Column(String, ForeignKey("users.user_id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)

    author = relationship("Users", back_populates="likes")
    post = relationship("Posts", back_populates="likes")


class Images(Base):
    __tablename__ = "images"

    image_id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)


class UserExternalMapping(Base):
    __tablename__ = "user_external_mapping"

    external_id = Column(String, primary_key=True)
    provider = Column(String, primary_key=True)

    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)

    user = relationship("Users", back_populates="user_external_map")
