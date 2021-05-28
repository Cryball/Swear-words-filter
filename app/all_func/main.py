from flask import Flask, request
from function_filter import filter


# Далее код для WebApi
app = Flask(__name__)


@app.route('/', methods=['GET'])
def form_example():
    return '''
           <form method="POST">
               <div>
                    <label>Введите текст для фильтрации: <input type="text" name="text"></label>
               </div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/', methods=['POST'])
def form_example1():
    text = request.form.get('text')
    result = filter(text)
    return result


if __name__ == '__main__':
    Flask.run(app, port=5000, host="0.0.0.0")
