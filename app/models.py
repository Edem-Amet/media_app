from .database import Base, engine
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship



# SQLAlchemy model for the Post table
# Defines all the columns and their data types for the Post table in the database
class Post(Base):

    __tablename__ = "posts"


    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String,
        nullable=False
    )

    content = Column(
        String,
        nullable=False
    )

    published = Column(
        Boolean,
        server_default='TRUE'
    )

    Timestamp = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )


    owner_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    owner = relationship(
        "User",
        back_populates="posts"
    )
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )

    email = Column(
        String,
        nullable=False,
        unique=True
    )

    password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )


    posts = relationship(
        "Post",
        back_populates="owner",
        cascade="all, delete"
    )