from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "< h1 > Home Page !!< /h1 >"

@app.route("/about")
def about():
    return "< h1 > About us Page !!< /h1 >"

if __name__ == '__main__':
    app.run(debug = 'True')