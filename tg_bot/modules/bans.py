from telegram import MessageEntity
from telegram.ext import run_async, CommandHandler

from tg_bot import dispatcher
from tg_bot.modules.helper_funcs import bot_admin, user_admin, is_user_admin
from tg_bot.modules.users import get_user_id


@run_async
@bot_admin
@user_admin
def ban(bot, update, args):
    chat = update.effective_chat
    message = update.effective_message
    prev_message = message.reply_to_message

    if message.entities and message.parse_entities([MessageEntity.TEXT_MENTION]):
        entities = message.parse_entities([MessageEntity.TEXT_MENTION])
        for e in entities:
            user_id = e.user.id
            break
        else:
            return

    elif len(args) >= 1 and args[0][0] == '@':
        user = args[0]
        user_id = get_user_id(user)
        if not user_id:
            message.reply_text("I don't have that user in my db. You'll be able to interact with them if "
                               "you reply to that person's message instead.")
            return

    elif len(args) >= 1 and args[0].isdigit():
        user_id = int(args[0])

    elif prev_message:
        user_id = prev_message.from_user.id

    else:
        message.reply_text("You don't seem to be referring to a user.")
        return

    if is_user_admin(chat, user_id):
        message.reply_text("I really wish I could ban admins...")
        return
    res = update.effective_chat.kick_member(user_id)
    if res:
        bot.send_sticker(update.effective_chat.id, 'CAADAgADOwADPPEcAXkko5EB3YGYAg')  # banhammer marie sticker
        message.reply_text("Banned!")
    else:
        message.reply_text("Well damn, I can't ban that user.")


@run_async
@bot_admin
def kickme(bot, update):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("I wish I could... but you're an admin.")
        return
    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("No problem.")
    else:
        update.effective_message.reply_text("Huh? I can't :/")


@run_async
@bot_admin
@user_admin
def unban(bot, update, args):
    message = update.effective_message
    prev_message = message.reply_to_message

    if message.entities and message.parse_entities([MessageEntity.TEXT_MENTION]):
        entities = message.parse_entities([MessageEntity.TEXT_MENTION])
        for e in entities:
            user_id = e.user.id
            break
        else:
            return

    elif len(args) >= 1 and args[0][0] == '@':
        user = args[0]
        user_id = get_user_id(user)
        if not user_id:
            message.reply_text("I don't have that user in my db. You'll be able to interact with them if "
                               "you reply to that person's message instead.")
            return

    elif len(args) >= 1 and args[0].isdigit():
        user_id = int(args[0])

    elif prev_message:
        user_id = prev_message.from_user.id

    else:
        message.reply_text("You don't seem to be referring to a user.")
        return

    res = update.effective_chat.unban_member(user_id)
    if res:
        message.reply_text("Yep, this user can join!")
    else:
        message.reply_text("Hm, couldn't unban this person.")


__help__ = """
 - /ban <userhandle>: bans a user. (via handle, or reply)
 - /unban <userhandle>: unbans a user. (via handle, or reply)
 - /kickme: kicks the user who issued the command
 """

KICK_HANDLER = CommandHandler("ban", ban, pass_args=True)
UNKICK_HANDLER = CommandHandler("unban", unban, pass_args=True)
KICKME_HANDLER = CommandHandler("kickme", kickme)

dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(UNKICK_HANDLER)
