from sqlalchemy import ForeignKey, BigInteger, String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from typing import List

from dotenv import dotenv_values
import os

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

DB_URL = dotenv['DB_URL']

engine = create_async_engine(url=DB_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    ...


class Languages(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id = mapped_column(BigInteger, unique=True)
    language_code: Mapped[str] = mapped_column(String(20), default="", nullable=True)


class Staff(Base):
    __tablename__ = 'staff'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(240))


class Contacts(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text)


class AboutUs(Base):
    __tablename__ = 'about_us'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    eng_message: Mapped[str] = mapped_column(Text)
    rus_message: Mapped[str] = mapped_column(Text)
    uzb_message: Mapped[str] = mapped_column(Text)


class Consumers(Base):
    __tablename__ = 'consumers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    telegram_name: Mapped[str] = mapped_column(String(240), nullable=True)
    full_name: Mapped[str] = mapped_column(String(240), nullable=True)
    contact: Mapped[str] = mapped_column(String(240), nullable=True)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title_eng: Mapped[str] = mapped_column(String(240))
    title_rus: Mapped[str] = mapped_column(String(240))
    title_uzb: Mapped[str] = mapped_column(String(240))
    good_rel: Mapped[List['Good']] = relationship(back_populates='category_rel', cascade="all, delete", passive_deletes=True)


class Good(Base):
    __tablename__ = 'goods'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete="CASCADE"))
    price: Mapped[int] = mapped_column()
    photo: Mapped[str] = mapped_column(String(400))
    category_rel: Mapped['Category'] = relationship(back_populates='good_rel')


async def set_tables():
    async with async_session() as connect:
        query = """
        INSERT INTO contacts(message)
        VALUES ('contacts');
        """
        await connect.execute(text(query))
        await connect.commit()

    async with async_session() as connect:
        query = """
        INSERT INTO about_us(eng_message, rus_message, uzb_message)
        VALUES ('Description', 'Описание', 'Tavsif');
        """
        await connect.execute(text(query))
        await connect.commit()


async def async_main():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)