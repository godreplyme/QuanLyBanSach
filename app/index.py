from app import app


@app.route("/")
def index():
    print('hello')


if __name__ == '__main__':
    app.run()
