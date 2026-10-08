import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
BOT_TOKEN="8629111423:AAEwN-upf3PHsOql_-obq_3L4jOeI8gaYhA"
TOKEN = BOT_TOKEN  # Token serverdagi o'zgaruvchidan olinadi
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchilarning joriy ifodasini saqlash uchun lug'at
user_data = {}

def get_calc_keyboard():
    builder = InlineKeyboardBuilder()
    buttons = [
        "C", "(", ")", "/",
        "7", "8", "9", "*",
        "4", "5", "6", "-",
        "1", "2", "3", "+",
        "0", ".", "="
    ]
    for btn in buttons:
        builder.button(text=btn, callback_data=f"num_{btn}")
    builder.adjust(4)
    return builder.as_markup()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_data[message.from_user.id] = ""
    await message.answer("Kalkulyatordan foydalaning:", reply_markup=get_calc_keyboard())

@dp.callback_query(F.data.startswith("num_"))
async def calc_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    val = call.data.split("_")[1]
    
    current_expr = user_data.get(user_id, "")
    
    if val == "C":
        current_expr = ""
    elif val == "=":
        try:
            # Hisoblash (faqat xavfsiz belgilar)
            clean_expr = current_expr.replace("×", "*").replace("÷", "/")
            current_expr = str(eval(clean_expr)) if clean_expr else "0"
        except Exception:
            current_expr = "Xatolik"
    else:
        if current_expr == "Xatolik":
            current_expr = ""
        current_expr += val
        
    user_data[user_id] = current_expr
    display_text = current_expr if current_expr else "0"
    
    try:
        await call.message.edit_text(f"Natija: **{display_text}**", parse_mode="Markdown", reply_markup=get_calc_keyboard())
    except Exception:
        pass
    await call.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())