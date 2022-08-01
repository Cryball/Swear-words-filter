from flask import Flask, request
import function_filter


# Далее код для WebApi
app = Flask(__name__)


@app.route('/', methods=['GET'])
def form_example():
    return '''
           <form method="POST">
               <div>
                    <label>Insert text to filter: <input type="text" style="width: 500px; height: 50px;" name="text"></label>
               </div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/', methods=['POST'])
def form_example1():
    text = request.form.get('text')
    result = function_filter.filter.filter(text)
    return '''
    <div>
        <h1>Text before:</h1>
        <p>''' + text + '''</p>
        <br /><br /><br /><br />
        <h2>Work of code:</h2>
        <p>''' + str(round(result[1], 2)) + ''' s</p>
        <h1>Text after filtration:</h1>
        <p>''' + result[0] + '''</p>
    </div>
    '''


if __name__ == '__main__':
    Flask.run(app, port=5000, host="0.0.0.0")
