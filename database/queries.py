from database.models import *

from sqlalchemy import text


async def insert_data_to_language(chat_id):
    async with async_session() as connect:
        query = """
        INSERT INTO languages(chat_id)
        VALUES (:chat_id) ON CONFLICT DO NOTHING
        """
        await connect.execute(text(query), {'chat_id': chat_id})
        await connect.commit()


async def update_data_to_language(chat_id, language):
    async with async_session() as connect:
        query = """
        UPDATE languages
        SET language_code = :language_code
        WHERE chat_id = :chat_id
        """
        await connect.execute(text(query), {'language_code': language, 'chat_id': chat_id})
        await connect.commit()


async def get_user_language(chat_id):
    async with async_session() as connect:
        query = """
        SELECT language_code FROM languages
        WHERE chat_id = :chat_id
        """
        data = await connect.execute(text(query), {'chat_id': chat_id})
        return data.fetchone()[0]


async def add_admin_to_db(telegram_id, name):
    async with async_session() as connect:
        query = """
        INSERT INTO staff(telegram_id, name)
        VALUES (:telegram_id, :name) ON CONFLICT DO NOTHING
        """
        await connect.execute(text(query), {'telegram_id': telegram_id, 'name': name})
        await connect.commit()


async def get_admin_id():
    async with async_session() as connect:
        query = """
        SELECT telegram_id FROM staff;
        """
        data = await connect.execute(text(query))
        users = data.fetchall()
        admins = [admin[0] for admin in users]
        return admins


async def get_admin_name():
    async with async_session() as connect:
        query = """
        SELECT name FROM staff;
        """
        data = await connect.execute(text(query))
        users = data.fetchall()
        admins = [admin[0] for admin in users]
        return admins


async def delete_admin_from_table(name):
    async with async_session() as connect:
        query = """
        DELETE FROM staff WHERE name = :name;
        """
        await connect.execute(text(query), {'name': name})
        await connect.commit()


async def category_add(title_eng, title_uzb, title_rus):
    async with async_session() as connect:
        query = """
        INSERT INTO categories(title_eng, title_uzb, title_rus)
        VALUES (:title_eng, :title_uzb, :title_rus)
        """
        await connect.execute(text(query), {'title_eng': title_eng, 'title_uzb': title_uzb, 'title_rus': title_rus})
        await connect.commit()


async def alter_category(ct_id, title_eng, title_uzb, title_rus):
    async with async_session() as connect:
        query = """
        UPDATE categories
        SET title_eng = :title_eng, title_uzb = :title_uzb, title_rus = :title_rus
        WHERE id = :id
        """
        await connect.execute(text(query), {'title_eng': title_eng, 'title_uzb': title_uzb, 'title_rus': title_rus, 'id': ct_id})
        await connect.commit()


async def get_categories():
    async with async_session() as connect:
        query = """
        SELECT title_eng, title_uzb, title_rus, id FROM categories
        """
        data = await connect.execute(text(query))
        return data.fetchall()


async def get_contacts():
    async with async_session() as connect:
        contacts = await connect.execute(text("""
        SELECT message FROM contacts
        WHERE id = 1
        """))
        return contacts.fetchone()[0]


async def get_all_chats():
    async with async_session() as connect:
        data = await connect.execute(text("""
        SELECT chat_id FROM languages
        """))
        users = data.fetchall()
        chats = [user[0] for user in users]
        return chats


async def insert_consumer_data(telegram_id, telegram_name):
    async with async_session() as connect:
        query = """
        INSERT INTO consumers(telegram_id, telegram_name)
        VALUES (:telegram_id, :telegram_name) ON CONFLICT DO NOTHING
        """
        await connect.execute(text(query), {'telegram_id': telegram_id, 'telegram_name': telegram_name})
        await connect.commit()


async def insert_other_consumer_data(telegram_id, contact, full_name):
    async with async_session() as connect:
        query = """
        UPDATE consumers
        SET contact = :contact, full_name = :full_name
        WHERE telegram_id = :telegram_id
        """
        await connect.execute(text(query), {'contact': contact, 'full_name': full_name, 'telegram_id': telegram_id})
        await connect.commit()


async def get_all_consumers():
    async with async_session() as connect:
        query = """
        SELECT telegram_id FROM consumers
        """
        data = await connect.execute(text(query))
        users = data.fetchall()
        users = [user[0] for user in users]
        return users


async def update_eng_description(eng_message):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE about_us
        SET eng_message = :eng_message
        WHERE id = 1
        """), {'eng_message': eng_message})
        await connect.commit()


async def update_rus_description(rus_message):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE about_us
        SET rus_message = :rus_message
        WHERE id = 1
        """), {'rus_message': rus_message})
        await connect.commit()


async def update_uzb_description(uzb_message):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE about_us
        SET uzb_message = :uzb_message
        WHERE id = 1
        """), {'uzb_message': uzb_message})
        await connect.commit()


async def get_all_descriptions():
    async with async_session() as connect:
        data = await connect.execute(text("""
        SELECT uzb_message, rus_message, eng_message FROM about_us
        WHERE id = 1
        """))
        descs = data.fetchone()
        return descs


async def update_contacts(contacts):
    async with async_session() as connect:
        await connect.execute(text("""
            UPDATE contacts
            SET message = :message
            WHERE id = 1
            """), {'message': contacts})
        await connect.commit()


async def delete_category_from_table(category_id):
    async with async_session() as connect:
        await connect.execute(text("""
        DELETE FROM categories WHERE id = :id;
        """), {'id': category_id})
        await connect.commit()


async def insert_good_to_table(title, description, category_id, price, photo):
    async with async_session() as connect:
        await connect.execute(text("""
        INSERT INTO goods(title, description, category_id, price, photo)
        VALUES (:title, :description, :category_id, :price, :photo)
        """), {'title': title, 'description': description, 'category_id': category_id, 'price': price, 'photo': photo})
        await connect.commit()


async def get_goods_by_category(category_id):
    async with async_session() as connect:
        goods = await connect.execute(text("""
        SELECT title, id FROM goods
        WHERE category_id = :category_id
        """), {'category_id': category_id})
        data = [good for good in goods.fetchall()]
        return data


async def get_good(good_id):
    async with async_session() as connect:
        goods = await connect.execute(text("""
        SELECT title, description, price, photo, category_id FROM goods
        WHERE id = :id
        """), {'id': good_id})
        data = goods.fetchone()
        return data


async def change_good_title(title, good_id):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE goods
        SET title = :title
        WHERE id = :id
        """), {'title': title, 'id': good_id})
        await connect.commit()


async def change_good_description(description, good_id):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE goods
        SET description = :description
        WHERE id = :id
        """), {'description': description, 'id': good_id})
        await connect.commit()


async def change_good_photo(photo, good_id):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE goods
        SET photo = :photo
        WHERE id = :id
        """), {'photo': photo, 'id': good_id})
        await connect.commit()


async def change_good_category(category_id, good_id):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE goods
        SET category_id = :category_id
        WHERE id = :id
        """), {'category_id': category_id, 'id': good_id})
        await connect.commit()


async def change_good_price(price, good_id):
    async with async_session() as connect:
        await connect.execute(text("""
        UPDATE goods
        SET price = :price
        WHERE id = :id
        """), {'price': price, 'id': good_id})
        await connect.commit()


async def delete_good(good_id):
    async with async_session() as connect:
        await connect.execute(text("""
        DELETE FROM goods WHERE id = :id
        """), {'id': good_id})
        await connect.commit()


async def get_consumer_data(consumer_id):
    async with async_session() as connect:
        consumer = await connect.execute(text("""
        SELECT telegram_name, full_name, contact
        FROM consumers
        WHERE telegram_id = :telegram_id
        """), {'telegram_id': consumer_id})
        return consumer.fetchone()
