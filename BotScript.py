import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define a function to handle the /start command
def start(update, context):
    # Send a welcome message to the user
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Hello! Welcome to the quiz exam bot. Please click on the link to start the quiz: [https://forms.gle/U9DyLhpsTUyV88ae9]")

# Define a function to handle quiz responses
def quiz_response(update, context):
    # Retrieve the user's name or Telegram handle from the message
    user_name = update.message.from_user.username

    # Authenticate with the Google Sheets API using a service account
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/houssemeddine/TestBot_Final/binaamanhaji-050295eb8daf.json', scope)
    client = gspread.authorize(credentials)

    # Open the responses sheet and retrieve the user's row based on their name or Telegram handle
    sheet = client.open('https://docs.google.com/spreadsheets/d/1KzYCleBQuJ8i7gSJRg0553_2BCZT_iAgpYTXuxFO8Yk/edit?usp=sharing').sheet1
    user_row = sheet.find(user_name).row

    # Retrieve the user's score from the responses sheet and calculate their pass/fail status
    score = int(sheet.cell(user_row, 3).value)
    if score >= 50:
        message = f"Congratulations {user_name}, you passed the quiz with a score of {score}!"
    else:
        message = f"Sorry {user_name}, you failed the quiz with a score of {score}. Please try again."

    # Send a pass/fail message to the user using context.bot.send_message()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=message)

# Set up the bot and start polling for messages
def main():
    # Create a bot object using the HTTP API token
    bot = telegram.Bot(token='6072637768:AAFJ75R-OamAe3yRIpmjFzN9sftTnbkivSw')

    # Create an updater object to handle incoming messages
    updater = Updater(token='6072637768:AAFJ75R-OamAe3yRIpmjFzN9sftTnbkivSw', use_context=True)

    # Set up command handlers for the /start and /help commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))

    # Set up a message handler to handle quiz responses
    updater.dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, quiz_response))

    # Start the bot's polling loop
    updater.start_polling()

    # Run the bot until it is stopped manually
    updater.idle()

if __name__ == '__main__':
    main()
