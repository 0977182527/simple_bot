import json
from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from main import load_api_key

def load_api_key():
        with open('config.json') as config_file:
            config_data = json.load(config_file)
            return config_data['telegram_api_key']
                
TOKEN : final = load_api_key() #here you place the telegram token
BOT_USER_NAME : final = '@Alghufar_bot'    

async def start_command(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut, que puis-je faire pour toi ?")

async def help_command(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Je suis la pour t'aider !")

async def custom_command(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ceci est la commancde custom")

def handle_response(text : str) -> str:
    
    processed :str = text.lower()
    
    if 'hi' in processed:
        return 'Hey there !'
    
    if 'how are you' in processed:
        return "I'm fine thanks how can i help today ?"
    
    return 'I didn\t understand what your wrote !'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text : str = update.message.text
    print (f'message {message_type}')
    
    #print(f'User ({update.message.chat.i}) in {message_type} : "{text}"')
    
    if message_type == 'group':
        if BOT_USER_NAME in text:
            new_text: str = text.replace(BOT_USER_NAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        
        response: str = handle_response(text)
        
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update : Update, context : ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    print(f'User token{TOKEN}')
    # Cette partie gere les commandes
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    
    #cette partie gere les messages 
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    #cette partie gere toutes les erreurs possible
    app.add_error_handler(error)
    
    app.run_polling(poll_interval=1)