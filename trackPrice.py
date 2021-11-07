from selenium import webdriver
import pandas as pd
import telebot

productName = ''
siteUrl = ''
xpath = ''
modelPrice = ''
tBotToken = ''
tChatId = ''

#Getting element from website
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
driver.get (siteUrl)
price = driver.find_elements_by_xpath(xpath)[0]

if (price.text != modelPrice):
    #Sent to telegram chat
    bot = telebot.TeleBot(tBotToken)
    markup = telebot.types.InlineKeyboardMarkup()
    buttonToUrl = telebot.types.InlineKeyboardButton(text='Take me there', url=siteUrl)
    markup.add(buttonToUrl)
    bot.send_message(tChatId, productName + ' price was changed, new price is ' + price.text, reply_markup=markup)
