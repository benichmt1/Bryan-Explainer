import os
from flask import Flask, request, Response
import wikipedia

app = Flask(__name__)


@app.route('/slackpedia', methods=['post'])
def slackpedia():
    query = request.values.get('text')
    result = check_query(query)

    return Response(result, content_type='charset=utf-8; text/plain')


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
