from flask import Flask

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


app.run(debug=True)
