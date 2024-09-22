import asyncio
from telegram.ext import Application, CommandHandler
from datetime import datetime, timedelta

# Store user data
user_data = {}

# Define constants
TOTAL_UNITS = 11054  # Total tokens in 24 hours
SECONDS_IN_A_DAY = 24 * 60 * 60
TOKENS_PER_SECOND = TOTAL_UNITS / SECONDS_IN_A_DAY  # Tokens distributed per second

# /start command handler
async def start(update, context):
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {
            "balance": 0,
            "last_mined_time": datetime.now()
        }
        await update.message.reply_text("Welcome to Hamster Kombat Airdrop! Mining will start immediately.")
        # Start the mining process for the user
        asyncio.create_task(mine_tokens(user_id))
    else:
        await update.message.reply_text("You're already participating in the mining process.")

# Mining function that distributes tokens every second
async def mine_tokens(user_id):
    while True:
        # Calculate how much time has passed since the last mining event
        current_time = datetime.now()
        last_mined_time = user_data[user_id]["last_mined_time"]
        time_difference = (current_time - last_mined_time).total_seconds()
        
        # Update the balance based on the time that has passed
        user_data[user_id]["balance"] += TOKENS_PER_SECOND * time_difference
        user_data[user_id]["last_mined_time"] = current_time
        
        # Wait for 1 second before mining again
        await asyncio.sleep(1)

# /balance command handler
async def balance(update, context):
    user_id = update.effective_user.id
    
    if user_id in user_data:
        balance = user_data[user_id]["balance"]
        await update.message.reply_text(f"Your current balance is {balance:.2f} Hamster Kombat tokens.")
    else:
        await update.message.reply_text("You haven't started mining yet. Use /start to begin.")

def main():
    # Initialize the Application
    application = Application.builder().token("7727434738:AAFkRWoY4w9S8mD62UQ7gGijjPwEKKaYNPg").build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
