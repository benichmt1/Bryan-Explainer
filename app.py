from flask import Flask
import wikipedia

app = Flask(__name__)


@app.route('/')
@app.route('/<query>')
def index(query=''):
    result = check_query(query)

    return result


def check_query(query):
    try:
        result = wikipedia.summary(query)
    except wikipedia.exceptions.DisambiguationError as error:
        return suggest_queries(error.options)

    return result


def suggest_queries(options):
    suggested_queries = get_suggested_options(options, 5)
    suggested_response = "You must be a little more precise \n{}".format(
        get_suggested_string(suggested_queries))

    return suggested_response


def get_suggested_options(result, max_length):
    result = result[:max_length]

    return result


def get_suggested_string(query):
    suggested = ''
    bullet_icon = ' :black_small_square:'

    for element in query:
        suggested += "{} {}\n".format(bullet_icon, element)

    return suggested


if __name__ == "__main__":
    app.run(debug=True)
