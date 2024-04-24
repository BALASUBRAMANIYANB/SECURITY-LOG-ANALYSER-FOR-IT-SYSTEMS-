from flask import Flask, render_template
import os

app = Flask(__name__)

# Function to read the content of a text file and return it as a list of lines
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        return content
    except Exception as e:
        return [f"Error reading file: {e}"]

# Define route to display the text file content
@app.route('/')
def show_text_file_content():
    file_path = 'home/lyca/syslog.txt'  # Update this with the path to your text file
    content = read_text_file(file_path)
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
