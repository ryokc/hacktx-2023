from flask import Flask

app = Flask(__name__)

@app.route("/purchases")

def purchases():
    return {"purchases": []}



if __name__ == "__main__":
    app.run(debug=True)