from flask import Flask, render_template, request, redirect
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

try:
    client = MongoClient("mongodb://localhost:27017")
    db = client["UserInfo"]
    collection = db["Info"]
except pymongo.errors.ConnectionError as e:
    print(f"Could not connect to MongoDB: {e}")


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        if request.method == 'POST':
            data = request.form.to_dict()
            new_user = {
                "email": data['email'],
                "subject": data['subject'],
                "message": data['message']
            }
            # Insert the new user data into MongoDB
            collection.insert_one(new_user)
            return redirect('/thankyou.html')
        else:
            return 'Invalid request method.', 405
    except Exception as e:
        return f'Something went wrong: {e}', 500


if __name__ == '__main__':
    app.run(debug=True)
