from diva import Diva

app = Diva()

@app.view('bar')
def bar():
    return [4, 5, 6]

@app.view('bar_2')
def bar_2():
    return [7, 8, 9]

if __name__ == '__main__':
    app.run(debug=True)
