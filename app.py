from flask import Flask, render_template, request
import DatabaseHelper as dh


app = Flask(__name__)


@app.route('/hello')
def hello():
    
    return render_template('main.html')

@app.route('/', methods=['POST', 'GET'])
def result():
    '''
    Handles what happens when submit is clicked
    '''
    service = dh.getSheetsService()
    
    if request.method == 'POST':

        result = request.form
        logEntry = []
        for key, value in result.items():
            logEntry.append(value)
        dh.addLogEntry(service, logEntry[0])
     
    
    recentActs = dh.getRecentActivities(service) 
    return render_template("main.html", result = recentActs)


if __name__ == '__main__':
    app.run(debug=True)