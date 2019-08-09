from flask import Flask
from flask import render_template

from app import app
import config

app.config.from_object(config)
#app.run(host='127.0.0.1', port=5000, debug=True)


print(app.config)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
