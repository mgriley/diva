from diva import Diva
app = Diva()

@app.view('foo')
def foo():
    return [1, 2, 3]

if __name__ == '__main__':
    app.run(debug=True)
