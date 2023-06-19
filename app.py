from flask import Flask, render_template, url_for, request, redirect
from Algoritm import algoritm

app = Flask(__name__)


@app.route("/")
def Home():
    return render_template("home.html")


@app.route("/algoritm", methods=['POST', 'GET'])
def algoritms():
    if request.method == "POST":
        name = request.form['name']
        kol = request.form['kol']
        
        map = algoritm(name, kol)
        map.save("templates/map.html")
        #min_dl=ret_min_values
        return redirect("/rezult")
        # render_template("map.html")
        # return render_template("rezult.html",name=name,kol=kol,pr=pr,map=map)
    else:
        return render_template("algoritm.html")


@app.route("/rezult")
def rezult():
    return render_template("map.html")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

