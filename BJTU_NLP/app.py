import flask
import ChatBot

app = flask.Flask(__name__, static_folder='static')

#define app routes
@app.route("/")
def index():
    return flask.render_template("index.html")
@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = flask.request.args.get('msg')
    print(userText)
    return str(ChatBot.run(userText))

if __name__ == "__main__":
    app.run()