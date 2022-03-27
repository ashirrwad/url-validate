import os
import requests
from flask import Flask, render_template,request
from bs4 import BeautifulSoup
from urllib.parse import urlparse


search_urls = ['https://www.veteranstoday.com/about-vt/',"https://www.google.com/search?q=",'https://lenta.ru/'
,'https://infowars.com/','https://robertspencer.org/','https://jihadwatch.org']
app = Flask(__name__)

def basic_check(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def validate_url(url):
    if basic_check(url) is True:
        for search_result in search_urls:
            if search_result in url:
                return False
        
        return True
    else:
        return False
    
     
def check_quote(url,quote):
    if quote=='':
        return False
    try:
        page = requests.get(url)
    except:
        return False
    soup = BeautifulSoup(page.text, "html.parser")
    if soup.findAll(text=quote):  
        return True
    else:
        return False
@app.route('/',methods=['GET', 'POST'])
def index():
    errors = []
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['url']
            q = request.form['quote']
        except:
            errors.append(
                "Invalid url"
            )
        if validate_url(url) is True:
            if(check_quote(url,q)) is True:
                return render_template('index.html',quote="It is a valid quote, Edit Request applicable")
            else:
                return render_template('index.html',quote="Invalid quote")
        else:
            return render_template('index.html',quote="Invalid URL")

    return render_template('index.html',errors=errors)


if __name__ == '__main__':
    app.run()