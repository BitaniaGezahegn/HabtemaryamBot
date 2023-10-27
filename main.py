from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re
import json
import datetime


#Loads Json file and returns a message
def json_loader(key):
    with open('messages.json', 'r') as r:
        json_data = json.load(r)

    return json_data[key]

TOKEN: Final = json_loader('BOT_TOKEN')
BOT_USERNAME: Final = json_loader('BOTUSERNAME')

def get_current_time():
    currunt_date = datetime.datetime.now()
    date = currunt_date.strftime("%B %d,%Y at %I:%M:%S %p")
    time = currunt_date.strftime('%H:%M:%S')
    return [date, time, currunt_date]

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    message_type: str = update.message.chat.type

    if message_type == 'private':
        await update.message.reply_text(json_loader("start"))
    else:
        if BOT_USERNAME not in text:
            return
        await update.message.reply_text(json_loader('private_start'))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    message_type: str = update.message.chat.type

    if message_type != 'private':
        if BOT_USERNAME not in text:
            return
        await update.message.reply_text(json_loader("help"))
    if message_type == 'private':
        await update.message.reply_text(json_loader("help"))

async def holidays_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    message_type: str = update.message.chat.type

    if message_type != 'private':
        if BOT_USERNAME not in text:
            return
    await update.message.reply_text(json_loader("holidays"))

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    message_type: str = update.message.chat.type

    if message_type != 'private':
        if BOT_USERNAME not in text:
            return
    await update.message.reply_text(json_loader("about"))

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    message_type: str = update.message.chat.type
    owner_id = 5282771696
    currunt = get_current_time()[2]
    running_time = currunt - start_time

    if message_type == 'private' and update.message.chat_id == owner_id:
        Ping_Message: str = f"The Bot has been Live for {running_time}"
        await update.message.reply_text(Ping_Message)

    elif message_type == 'private':
        await update.message.reply_html('This Feature is only available only for the bot <a href="https://t.me/elchapo_Et">Creator</a>!')

    if message_type != 'private':
        if BOT_USERNAME in text:
            await update.message.reply_html('This Feature is only available only for the bot <a href="https://t.me/elchapo_Et">Creator</a>!')

#Responses to Messages
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey! Their'

    #if 'how are you' in processed:
    #    return "I am good how are you"

    #make the bot more fun when talked to alone(in private)

    return "Sorry Couldn't Understand what you said click /help for more info."

async def typing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    #context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)


def contains_link(message: str):
    url_expression = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    result: list = re.findall(url_expression, message.lower())
    if result == []:
        return False
    else:
        return True

def contains_embeded_link(message: str):
    anchor_expression = r'<a\s+.*?href\s*=\s*["\']([^"\']+)["\'].*?>'
    result: list = re.findall(anchor_expression, message.lower())
    if result == []:
        return False
    else:
        return result

def get_chat_admins(admins):
    admin_list: list = []
    for admin in admins:
        admin_list.append(admin.user.id)
    return admin_list

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message_type: str = update.message.chat.type
        text: str = update.message.text
        group_user_id = update.message.chat.id
        user_name = update.message.from_user.username
        user_id = update.message.from_user.id
        message_id = update.message.message_id
        chat_id = update.message.chat.id
        is_admin = False
        MAIN_CHANNEL_ID = -1001446571420
        MAIN_GROUP_ID = -1001658864142
        Group_Anonumous_Bot = 1087968824
        from_main = False
        has_embeded_link = contains_embeded_link(update.message.text_html)
        control_bot_username = "@control_main_bot"
        control_comm_id = '-1001905152880'
    except Exception as e:
        if str(e) == "'NoneType' object has no attribute 'chat'":
            return print('Message from Communication Channel ... ignoring message')
        #print(f'Failed to get variables in the handle_message function specifical detail: {e}')

    try:
        administrators = await context.bot.get_chat_administrators(chat_id)
        admins = get_chat_admins(administrators)
    except:
        pass
    currunt_date = datetime.datetime.now()
    date = currunt_date.strftime("%B %d,%Y at %I:%M:%S %p")
    response: str = handle_response(text)
    #print(f'User ({update.message.chat.id}) in {message_type}: "{text}"', group_user_id)

    try:
        with open('log.txt', 'a') as f:
            f.write(f'User: ({update.message.chat.id}) User_name: {update.message.chat.username} in {message_type} on {date}: "{text}"\n\t"Bot:", {response}\n\n')
    except:
        try:
            with open('log.txt', 'a') as f:
                f.write(f'User: ({update.message.chat.id}) User_name: {update.message.chat.username} in {message_type} on {date}: "{text.encode}"\n\t"Bot:", {response}\n\n')
        except:
            print("Couldn't Log Message")
    #print(f'User: ({update.message.chat.id}) User_name: {update.message.chat.username} in {message_type} on {date}: "{text}"\n    "Bot:", {response}\n\n')

    if message_type == 'group' or message_type == 'supergroup':
        # Check where the message is from
        if str(group_user_id) == str(MAIN_GROUP_ID):
            for id in admins:
                if str(user_id) == str(id) or str(user_id) == str(Group_Anonumous_Bot): #Check if Admin...
                        is_admin = True
                #Check id admin
                if not is_admin:
                    #Check if Message has embedded Link
                    if has_embeded_link != False:
                        #Check if the link is the channels link
                        for link in has_embeded_link:
                            # Check if embeded link is main channel link
                            if link == 'http://t.me/habtemaryam26':
                                pass
                            else:
                                try:
                                    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                                    # Send message to the control Bot
                                    control_msg = f'''{control_bot_username}\nchat_id: {chat_id}\nusername: {user_name}\nmessage: [{text}]\nmessage_id: {message_id}\nreason: 0'''
                                    return await context.bot.send_message(chat_id=control_comm_id, text=control_msg)
                                except Exception as e:
                                    await context.bot.send_message(chat_id=control_comm_id, text=e)
            
            # Check if Message is Forwarded
            if update.message.forward_from_chat != None or update.message.forward_from != None:
                # Check if User id Admin
                try:
                    if str(update.message.forward_from_chat.id) == str(MAIN_CHANNEL_ID):
                        from_main = True
                except:
                    pass
                for id in admins:
                    if str(user_id) == str(id) or str(user_id) == str(Group_Anonumous_Bot): #Check if Admin...
                        is_admin = True

                if not is_admin and not from_main: #id not main channel
                    try:
                        control_msg = f'''{control_bot_username}\nchat_id: {chat_id}\nusername: {user_name}\nmessage: [{text}]\nmessage_id: {message_id}\nreason: 1'''
                        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                        return await context.bot.send_message(chat_id=control_comm_id, text=control_msg)
                    except Exception as e:
                        await context.bot.send_message(chat_id=control_comm_id, text=e)
            
            #Check if Message Has Link
            has_link = contains_link(message=text.lower())
            if has_link:
                for id in admins:
                    if str(user_id) == str(id) or str(user_id) == str(Group_Anonumous_Bot): #Check if Admin...
                        is_admin = True

                if not is_admin: #
                    try:
                        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
                        control_msg = f'''{control_bot_username}\nchat_id: {chat_id}\nusername: {user_name}\nmessage: [{text}]\nmessage_id: {message_id}\nreason: 2'''
                        return await context.bot.send_message(chat_id=control_comm_id, text=control_msg)
                    except Exception as e:
                        await context.bot.send_message(chat_id=control_comm_id, text=e)
                    # Self Distruct Message
                    # maybe build another bot to delete the message after a specified ammount of time if and only if the message was from the bot.
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)

        else:
            return
    else:
        response: str = handle_response(text)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(context.error) == "cannot access local variable 'text' where it is not associated with a value":
        return
    print(f'Caused error {context.error}')

if __name__ == '__main__':

    print('Starting Program ...')

    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('holidays', holidays_command))
    app.add_handler(CommandHandler('about', about_command))
    app.add_handler(CommandHandler('ping', ping_command))

    #MEssages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    #Errors
    app.add_error_handler(error)

    #Polling
    print('Polling ...')
    start_time = datetime.datetime.now()
    app.run_polling(poll_interval=5)