from flask import Flask, render_template, request, flash
import dataset
app = Flask(__name__)


db = dataset.connect('sqlite:///test.db')
db.begin()
table = db['std']
articles = db['articles']
users = []

def hello(name, password):
	table.insert(dict(name=name, password=password))
	

def find(name, password):
	x = table.find_one(name=name, password=password)
	return x

def make_list():
	for thing in table:
		users.append(thing)
		return table.all
	return users


def addArticle(title , article):

	try:
		articles.insert(dict(title = title , article = article))
		db.commit()
	except:
		db.rollback()

def getArticles ():
	return articles.all()

@app.route('/', methods = ["post" , "get"])
def home():
	if request.method == "POST":
		name = request.form['name']
		password = request.form['password']

		hello(name, password)
		return render_template('login.html', name=name, password=password)
	else:
		return render_template('reg.html')

@app.route('/login', methods = ['post', 'get'])
def login():
	if(request.method ==  "POST"):
		name = request.form['name']
		passw = request.form['password']
		found = find(name, passw)
		if found == None:
			return "Try Again"
		else:
			make_list()
			return render_template('logged.html', found = found, item = users)

	else : 
		return render_template('login.html')		









@app.route('/add', methods = ["post" , "get"])
def article():
	if request.method == "POST":
		art = request.form['art']
		title = request.form['title']

		addArticle(title, art)
		return render_template('articles.html' , articles = getArticles())
	else:
		return render_template('addArticles.html')







if __name__ == "__main__":
	app.run(port=5050)