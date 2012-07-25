import os

from coopy.base import init_persistent_system
from riobus import RioBus

from flask import Flask, jsonify, render_template
from collections import OrderedDict

app = Flask(__name__)

riobus = init_persistent_system(RioBus())

@app.route("/")
def main():
    return render_template('index.html', lines=riobus.lines)
    #return jsonify(riobus.lines)

@app.route("/line/html/<line_id>")
def html_line(line_id):
    line = riobus.lines[line_id]
    return render_template('detail.html', line=line)

@app.route("/line/<line_id>")
def line(line_id):
    return jsonify(riobus.lines[line_id])

@app.route("/search/<nome>")
def search(nome):
    return jsonify(riobus.search_street(nome))

if __name__ == "__main__":
    app.run()
