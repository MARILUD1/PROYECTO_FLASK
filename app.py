from flask import Flask, render_template

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para la página "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)