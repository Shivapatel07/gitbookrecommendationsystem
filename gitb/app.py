from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from recommender import hybrid_recommend, popular_books

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the dataset
df = pd.read_csv("Filtered_Popular_Books.csv")

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'], books=popular_books())
    return redirect(url_for('login'))

@app.route('/recommend', methods=['POST'])
def recommend():
    book_name = request.form['book_name'].lower().strip()
    try:
        recommendations = hybrid_recommend(book_name)
    except:
        recommendations = []

    if not recommendations:
        error = f"No recommendations found for '{book_name}'"
        return render_template('home.html', username=session.get('username'), error=error, books=popular_books())

    return render_template('recommendations.html', recommendations=recommendations, input_book=book_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Signup logic can be expanded here
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
