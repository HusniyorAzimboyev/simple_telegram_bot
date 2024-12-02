from telegram.ext import MessageHandler,CommandHandler,Filters,Updater
from telegram import ReplyKeyboardMarkup,KeyboardButton
import sqlite3
from contextlib import closing
from crud_oop import BaseCRUD

token = '7477170282:AAG86MRRcCI5fwmZKvmNkxruTf2SLacGGNY'

def show_info(update,context):
    with closing(sqlite3.connect("husniyors_bot_database.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users;")
        result = cursor.fetchall()
    result2 = []
    for i in result:
        result2.append(str(i))
    result_final = "\n".join(result2)
    update.message.reply_text(text=result_final)
def create_phone_number(id,number):
    with closing(sqlite3.connect("husniyors_bot_database.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE users SET
        phone_number = ?
        WHERE id=?;
        """,(number,id))
def create_user(id,username):
    with closing(sqlite3.connect("husniyors_bot_database.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO users(id,username)
        VALUES (?,?);
        """,(id,username))
        connection.commit()
def kara_jadvali(son):
    rasult = ""
    resultlist=[]
    index = 1
    for i in range(10):
        resultlist.append(f'{i + 1} * {index} = {(i+1)*index}')
        index+=1
    result = "\n".join(resultlist)
    return result
def start_message(update,context):
    update.message.reply_text(text="Hi, welcome to Husnior's Ai bot!")
    print("id: ",update.message.from_user.id," name: ",update.message.from_user.first_name)
    id = update.message.from_user.id
    username = update.message.from_user.name
    create_user(id,username)
def menu(update,context):
    buttons = [[
        KeyboardButton(text="Location", request_location=True),
        KeyboardButton(text="Contact", request_contact=True)],[
        KeyboardButton(text="/multiple_table")]
    ]
    update.message.reply_text(
        text="Menu",
        reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True,one_time_keyboard=False)
    )

def kara_jadvalisend(update,context):
    kara = kara_jadvali(update.message.text)
    update.message.reply_text(text=kara)

def message(update,context):
    update.message.reply_text(text=f"Your message is {update.message.text}")

def location(update,context):
    location = update.message.location
    context.bot.send_message(chat_id=1779062204,text=f'User: {update.message.from_user.name},id: {update.message.from_user.id} sent location below👇')
    context.bot.send_location(chat_id=1779062204,latitude=location.latitude,longitude=location.longitude)
def contact(update,context):
    phone_number = update.message.contact.phone_number
    context.bot.send_message(chat_id=1779062204,text=f"{update.message.from_user.name}: sent phone number: {phone_number}")
    create_phone_number(update.message.from_user.id,phone_number)

def main():
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(command="start",callback=start_message))
    dispatcher.add_handler(CommandHandler(command="menu",callback=menu))
    dispatcher.add_handler(CommandHandler(command="multiple_table",callback=kara_jadvalisend))
    dispatcher.add_handler(CommandHandler(command="showinfo",callback=show_info))
    dispatcher.add_handler(MessageHandler(Filters.text,callback=message))
    dispatcher.add_handler(MessageHandler(filters=Filters.location,callback=location))
    dispatcher.add_handler(MessageHandler(filters=Filters.contact,callback=contact))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

