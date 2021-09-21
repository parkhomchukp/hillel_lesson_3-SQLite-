from flask import Flask
from webargs import fields
from marshmallow import validate
from webargs.flaskparser import use_kwargs

import db
import utils

app = Flask(__name__)


@app.route('/')
def home():
    return 'SUCCESS'


@app.route('/customers')
@use_kwargs(
    {
        "first_name": fields.Str(
            required=False,
            missing=None,
            validate=[validate.Regexp('^[0-9]*')]
        ),
        "last_name": fields.Str(
            required=False,
            missing=None,
            validate=[validate.Regexp('^[0-9]*')]
        ),
    },
    location="query",
)
def get_customers(first_name, last_name):
    query = 'select * from customers'

    fields = {}
    if first_name:
        fields["FirstName"] = first_name

    if last_name:
        fields["LastName"] = last_name

    if fields:
        query += ' WHERE ' + ' AND '.join(f'{k}="{v}"' for k, v in fields.items())

    records = execute_query(query)
    result = format_records(records)
    return result


@app.route('/unique_names')
def get_unique_names():
    query = 'SELECT FirstName FROM customers'
    records = db.execute_query(query)
    unique_names = list()
    for name in records:
        if name not in unique_names:
            unique_names.append(name)
    result = str(len(unique_names))
    return result


@app.route('/tracks_count')
def get_tracks_count():
    query = 'SELECT TrackId FROM tracks ORDER BY TrackId DESC'
    records = db.execute_query(query)
    result = str(records[0])
    return result


app.run(debug=True)
