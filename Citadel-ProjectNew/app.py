import model
from flask import Flask
from flask import render_template, request, redirect, url_for
import requests
from pymongo import MongoClient
import os
import openai
openai.api_key = "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"

app = Flask(__name__)

# MONGO DB CONFIGURATION TODO: USERNAME/PASSWORD GENERATION
username = "admin"
password = "y4YAl4HYf62iXkeT"
url = f"mongodb+srv://{username}:{password}@cluster0.3oovgyc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

db = client["portfolio"]
collection = db.stocks
user = {
    'tickers': [],
    'shares': []
}

# HOME PAGE
@app.route("/", methods = ['GET'])
@app.route('/home', methods = ['GET'])
def show_home():
    return render_template("index.html")


# USER INPUTS PAGE (INPUT STOCK INFORMATION)
@app.route('/asset-inputs', methods = ['GET', 'POST'])
def input_stocks():
    global user
    if request.method == 'GET':
        return render_template('addPortfolio.html')
    else:
        # TODO: change the way in which we obtain the data from the user (simplify request form)
        user['tickers'].extend(request.form.getlist('ticker'))
        user['shares'].extend(request.form.getlist('share'))
        # user = {
        #     'tickers': request.form.getlist('ticker'), # THIS WILL BE A LIST
        #     'shares': request.form.getlist('share') # THIS WILL BE A LIST OF INTEGERS EQUAL TO THE NUMBER OF ASSETS
        # }
        print("first test - " + str(user))
        stocks, total = model.cardCreation(user['tickers'], user['shares'])
        return render_template('/view.html', stocks = stocks, total = total)

# RESULTS PAGE OF CARDS TODO: ADD POST METHOD FOR REMOVAL/ADDING
@app.route('/results', methods = ['GET', 'POST'])
def results():
    # method to obtain tickers from portfolio
    if request.method == 'GET':
        stocks, total = model.cardCreation(user['tickers'], user['shares'])
        print(stocks)
        return render_template('view.html', stocks = stocks, total = total)
    else:
        removeShareNum = request.form.get("removeVal")
        ticker = request.form.get("tickerName")
        print('pulled ticker is')
        print(ticker)
        print("end pulled ticker test")
        user['tickers'], user['shares'] = model.remove_shares(user['tickers'], user['shares'], ticker, int(removeShareNum))
        stocks, total = model.cardCreation(user['tickers'], user['shares'])
        return render_template('view.html', stocks = stocks, total = total)

# CHATBOT PAGE
@app.route("/chatbot", methods=['GET', 'POST'])
def stockbot():
    if request.method == 'POST':
        question = request.form['question']
        response = openai.Completion.create(model="text-davinci-003", prompt=question, temperature=0, max_tokens=25)
        stockBot_response = response.choices[0]["text"]
        return render_template("chatbot.html", stockBot_response=stockBot_response)
    return render_template("chatbot.html")
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
