import model

from flask import Flask
from flask import render_template, request, redirect, url_for
import requests
from pymongo import MongoClient

app = Flask(__name__)

# MONGO DB CONFIGURATION TODO: USERNAME/PASSWORD GENERATION
username = "admin"
password = "y4YAl4HYf62iXkeT"
url = f"mongodb+srv://{username}:{password}@cluster0.3oovgyc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

db = client["portfolio"]
collection = db.stocks

# HOME PAGE
@app.route("/", methods = ['GET'])
@app.route('/home', methods = ['GET'])
def show_home():
    return render_template("index.html")

# USER INPUTS PAGE (INPUT STOCK INFORMATION)
@app.route('/asset-inputs', methods = ['GET', 'POST'])
def input_stocks():
    if request.method == 'GET':
        return render_template('addPortfolio.html')
    else:
        user = {
            'tickers': request.form('assets'), # THIS WILL BE A LIST
            'shares': request.form('shares') # THIS WILL BE A LIST OF INTEGERS EQUAL TO THE NUMBER OF ASSETS
        }
        return redirect('/results')

# RESULTS PAGE OF CARDS
@app.route('/results', methods = ['GET'])
def results():
    apikey = ""
    # method to obtain tickers from portfolio
    # results = call to model.cardCreation(user['tickers'], user['shares']) (results will be a dictionary)
    return render_template('view.html', results = results)

    
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)