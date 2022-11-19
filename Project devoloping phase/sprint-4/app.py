from flask import Flask,render_template,request
from newsapi import NewsApiClient
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey


serviceUsername = "50ab9a31-993d-4eaf-abf1-21c6f737b08c-bluemix"
servicePassword = "6864bc1c41f5701310846a0a80700140c138e7c82b8c7f678ce5ab877f8b90b9"
serviceURL = "https://50ab9a31-993d-4eaf-abf1-21c6f737b08c-bluemix:6864bc1c41f5701310846a0a80700140c138e7c82b8c7f678ce5ab877f8b90b9@50ab9a31-993d-4eaf-abf1-21c6f737b08c-bluemix.cloudantnosqldb.appdomain.cloud"

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()

app = Flask(__name__)

@app.route("/news")
def news():
    api_key = '4f625485702d4929a546bcf4eb9d5c79'
    
    newsapi = NewsApiClient(api_key=api_key)

    top_headlines = newsapi.get_top_headlines(sources = "the-verge")
    all_articles = newsapi.get_everything(sources = "the-verge")

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']

    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

        contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template('home.html',all = all)

@app.route("/search",methods = ['POST', 'GET'])
def searchFunct():
    inputText = request.form['nm']
    api_key = '4f625485702d4929a546bcf4eb9d5c79'
    
    newsapi = NewsApiClient(api_key=api_key)

    top_headlines = newsapi.get_top_headlines(sources="bbc-news")
    all_articles = newsapi.get_everything(q=inputText)

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']

    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

        contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template('home.html', all = all)

def addNewUser(userName,userEmail,userPassword):
    jsondata = {}
    jsondata["userName"] = str(userName)
    jsondata["userEmail"] = str(userEmail)
    jsondata["userPassword"] = str(userPassword)

    myDataBase = client['database1']
    newDocument = myDatabase.create_document(jsondata)


def authenticate(userName,userEmail):
    myDataBase = client['database1']
    result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
    if(len(result_collection) == 0):
        return False
    for data in result_collection:
        if data['doc']['userName'] == str(userName):
            return False
        if data['doc']['userEmail'] == str(userEmail):
            return False
    return True

@app.route("/register",methods = ['POST', 'GET'])
def registerUserData():
    userName = request.form.get("un", False)
    userEmail = request.form.get("ue", False)
    userPassword = request.form.get("up", False)
    if(authenticate(userName=userName,userEmail=userEmail)):
        return render_template("index.html")
    addNewUser(userName,userEmail,userPassword)
    return render_template("home.html")

@app.route("/" )
def home():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)
