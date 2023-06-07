import model
from flask import Flask
from flask import render_template, request, redirect, url_for
import requests
from pymongo import MongoClient

app = Flask(__name__)
user = {
    'tickers': [],
    'shares': []
}

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
    global user
    if request.method == 'GET':
        return render_template('addPortfolio.html')
    else:
        # TODO: change the way in which we obtain the data from the user (simplify request form)
        user = {
            'tickers': [
                request.form['ticker1'],
                request.form['ticker2'],
                request.form['ticker3'],
                request.form['ticker4'],
                request.form['ticker5']
            ], # THIS WILL BE A LIST
            'shares': [
                request.form['share1'], 
                request.form['share2'], 
                request.form['share3'], 
                request.form['share4'], 
                request.form['share5']
                ] # THIS WILL BE A LIST OF INTEGERS EQUAL TO THE NUMBER OF ASSETS
        }
        print("first test - " + str(user))
        return redirect('/results')

# RESULTS PAGE OF CARDS
@app.route('/results', methods = ['GET'])
def results():
    global user
    print("second test -" + str(user))
#     # method to obtain tickers from portfolio
    stocks = model.cardCreation(user['tickers'], user['shares'])
    return render_template('view.html', stocks = stocks) # TODO: add stocks
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)