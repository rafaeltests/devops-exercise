from flask import Flask, jsonify
from multiprocessing import Value

counter = Value('i', 0)
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!!!"

@app.route('/post', methods = ["POST"])
def post():
    with counter.get_lock():
         counter.value += 1
    return "a new POST!"
    
@app.route('/get', methods = ["GET"])
def get():
    return jsonify(count=counter.value)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
