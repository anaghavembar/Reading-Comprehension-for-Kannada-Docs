from flask import Flask, render_template, request
import tfidf
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/Demo")
def tool():
	return render_template("landingPage.html")

@app.route("/KannadaIndex")
def displayKannada():
	return render_template("KannadaIndex.html")

@app.route('/getAnswer',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
	   passage = request.form.get("passage")
	   question = request.form.get("question")
	   tfidfobj = tfidf.Tfidf(passage, question)
	   result,question,ucorpus,lcorpus,vec,listofsim,simofans=tfidfobj.tfidfCalculator()
	   return render_template("getAnswer.html",result = result,question=question,ucorpus=ucorpus,lcorpus=lcorpus,vec=vec,listofsim=listofsim,simofans=simofans)

if __name__ == "__main__":
	app.run(debug=True)
