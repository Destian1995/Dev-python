from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler
from telegram.ext.filters import TEXT

# Инициализация бота Telegram
TOKEN = '************************************************'
bot = Bot(token=TOKEN)


# Функция для обработки сообщений в Telegram
async def handle_message(update: Update, context):
    message_text = update.message.text
    response = send_to_website_and_get_response(message_text)
    await update.message.reply_text(response)


# Функция для отправки данных на сайт и получения ответа
def send_to_website_and_get_response(message_text):
    driver = webdriver.Chrome()

    try:
        # Переход на сайт
        driver.get("https://www.perplexity.ai")

        # Ожидание загрузки текстового поля и кнопки отправки
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea")))
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Submit']")))

        # Находим поле ввода
        textarea = driver.find_element(By.CSS_SELECTOR, "textarea")

        # Симуляция клика на текстовое поле после полной загрузки страницы
        textarea.click()

        # Ввод текста в текстовое поле
        textarea.send_keys(message_text)

        # Добавление пробела, чтобы сымитировать реальный ввод
        textarea.send_keys(" ")

        # Находим кнопку отправки
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit']")

        # Проверяем, доступна ли кнопка отправки (если да, то нажимаем ее)
        if submit_button.is_enabled():
            submit_button.click()
        else:
            # Если кнопка недоступна, попробуем отправить текст с помощью клавиши Enter
            textarea.send_keys(Keys.ENTER)

        # Ожидание 25 секунд для получения ответа
        time.sleep(25)

        # Поиск и копирование ответа
        # Обновленный селектор для ответа
        response_element = driver.find_element(By.CSS_SELECTOR,
                                               "div.relative.default.font-sans.text-base.text-textMain")
        response_text = response_element.text

        return response_text

    finally:
        driver.quit()


# Настройка приложения Telegram
application = Application.builder().token(TOKEN).build()

# Обработчик сообщений
application.add_handler(MessageHandler(TEXT, handle_message))

# Запуск бота
application.run_polling()
