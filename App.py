from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        return redirect(url_for("display", question=question))

    return render_template('index.html')

@app.route("/display", methods=['GET', 'POST'])
def display():
    # Get the question from the URL parameters if it's a GET request
    question = request.args.get('question')
    output = ""

    # Handle the form submission if it's a POST request (asking another question)
    if request.method == 'POST':
        question = request.form['question']
        return redirect(url_for('display', question=question))

    if question:
        # Call query.py with the question as an argument
        result = subprocess.run(['python', 'query_vector_database.py', '--prompt', question], capture_output=True, text=True)
        output = result.stdout.strip()

    return render_template('display.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)