from selenium import webdriver
import pandas as pd
import telebot
import json
import os
import csv
from datetime import date

with open('./config.json','r', encoding='utf8') as configFile:
    conf = json.load(configFile)
arrayStatData = []
arrayStatData.append(str(date.today()))
bot = telebot.TeleBot(conf["telegramBotToken"])
configUpdate = False

#Create statistic file if it does not exist
for product in conf["productsToMonitor"]:
    if product["isEnabled"] != 1:
        continue
    productName = product["productName"]
    productUrl = product["productUrl"]
    productXpath = product["productXpath"]
    productLastPrice = product["productLastPrice"]
    
    #Getting element from website
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    driver.get (productUrl)
    price = driver.find_elements_by_xpath(productXpath)[0]
    arrayStatData.append(price.text)
    
    if price.text != productLastPrice:
        configUpdate = True
        product["productLastPrice"] = price.text 

        #Sent to telegram chat
        markup = telebot.types.InlineKeyboardMarkup()
        buttonToUrl = telebot.types.InlineKeyboardButton(text='Take me there', url=productUrl)
        markup.add(buttonToUrl)
        bot.send_message(conf["telegramChatId"], productName + ' price was changed, new price is ' + price.text, reply_markup=markup)

#Adjust (recreate) config file in case we need to adjust last price
if configUpdate == True:
    with open('./config.json', 'w', encoding='utf8') as configNewFile:
        json.dump(conf, configNewFile, ensure_ascii=False, indent=4)
    configUpdate = False

#write to csv statistic file
with open(conf["csvFile"], 'a') as statFile:
    writer = csv.writer(statFile)
    writer.writerow(arrayStatData)
    statFile.close()