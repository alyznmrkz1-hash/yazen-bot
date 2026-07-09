import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

PHONE = "0938877023"


def main_keyboard(lang: str = "ar") -> InlineKeyboardMarkup:
    if lang == "en":
        buttons = [
            [InlineKeyboardButton(text="🛒 Products", callback_data="products_en")],
            [InlineKeyboardButton(text="📞 Contact", callback_data="contact_en")],
            [InlineKeyboardButton(text="🇸🇾 العربية", callback_data="home_ar")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="🛒 المنتجات", callback_data="products_ar")],
            [InlineKeyboardButton(text="📞 التواصل", callback_data="contact_ar")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="home_en")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_keyboard(lang: str = "ar") -> InlineKeyboardMarkup:
    text = "⬅️ Back" if lang == "en" else "⬅️ رجوع"
    data = "home_en" if lang == "en" else "home_ar"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=data)]])


@dp.message(CommandStart())
async def start(message: Message):
    text = (
        "أهلًا بك في بوت اليزن 👋\n\n"
        "اختر من الأزرار التالية:\n\n"
        "Welcome to Yazen Bot 👋\n"
        "Choose from the buttons below:"
    )
    await message.answer(text, reply_markup=main_keyboard("ar"))


@dp.callback_query(F.data == "home_ar")
async def home_ar(callback: CallbackQuery):
    await callback.message.edit_text(
        "أهلًا بك في بوت اليزن 👋\n\nاختر الخدمة المطلوبة:",
        reply_markup=main_keyboard("ar"),
    )
    await callback.answer()


@dp.callback_query(F.data == "home_en")
async def home_en(callback: CallbackQuery):
    await callback.message.edit_text(
        "Welcome to Yazen Bot 👋\n\nChoose the service you need:",
        reply_markup=main_keyboard("en"),
    )
    await callback.answer()


@dp.callback_query(F.data == "products_ar")
async def products_ar(callback: CallbackQuery):
    text = (
        "🛒 المنتجات المتوفرة لدى اليزن:\n\n"
        "• شحن ألعاب\n"
        "• شحن تطبيقات\n"
        "• اشتراكات تطبيقات\n"
        "• خدمات رقمية\n"
        "• منتجات وخدمات أخرى حسب الطلب\n\n"
        f"📞 للتواصل: {PHONE}"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard("ar"))
    await callback.answer()


@dp.callback_query(F.data == "products_en")
async def products_en(callback: CallbackQuery):
    text = (
        "🛒 Yazen Products:\n\n"
        "• Game top-up\n"
        "• App top-up\n"
        "• App subscriptions\n"
        "• Digital services\n"
        "• Other products and services on request\n\n"
        f"📞 Contact: {PHONE}"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard("en"))
    await callback.answer()


@dp.callback_query(F.data == "contact_ar")
async def contact_ar(callback: CallbackQuery):
    await callback.message.edit_text(f"📞 للتواصل مع اليزن:\n\n{PHONE}", reply_markup=back_keyboard("ar"))
    await callback.answer()


@dp.callback_query(F.data == "contact_en")
async def contact_en(callback: CallbackQuery):
    await callback.message.edit_text(f"📞 Contact Yazen:\n\n{PHONE}", reply_markup=back_keyboard("en"))
    await callback.answer()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
