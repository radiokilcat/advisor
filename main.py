import telegram
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler
import json
import spacy

TOKEN = ''

def start(update, context):
    update.message.reply_text("привет")
    return 'ECHO'

def cancel(update, context):
    return ConversationHandler.END


def echo(update, context):
    update.message.reply_text(update.message.text)


def utterance(update, context):
    msg = update.message.text
    nlp = spacy.load('ru_core_news_lg')
    doc = nlp(msg)

    for token in doc:
        token_text = token.text
        token_pos = token.pos_
        token_dep = token.dep_
        token_head = token.head.text
        print(f"{token_text:<12}{token_pos:<10}" \
              f"{token_dep:<10}{token_head:<12}")


    for token in doc:
        if token.dep_ == 'obj':
            update.message.reply_text('Ты чего-то хочешь...')
            return
    update.message.reply_text('Перефразируй')



if __name__ == '__main__':
    with open('tg.json', 'r') as tg:
        config = json.load(tg)
        TOKEN = config['token']

    bot = telegram.Bot(TOKEN)

    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'ECHO': [MessageHandler(Filters.text, utterance)],
            'ADD_INDO': [MessageHandler(Filters.text, utterance)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    disp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

