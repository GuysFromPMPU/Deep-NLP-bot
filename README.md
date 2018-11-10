```
set FLASK_APP=main.py
set FLASK_DEBUG=1
set FLASK_ENV=development
flask run --host="::"
./ngrok http 5000
```


requirements:
```
pip install pymorphy2[fast]
pip install coloredlogs
pip install humanize
```

flask ssl:
[best](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)
[docs1](http://flask.pocoo.org/snippets/111/)
[docs2](http://werkzeug.pocoo.org/docs/0.14/serving/)
[run with cert](https://stackoverflow.com/questions/48467835/run-flask-dev-server-over-https-using-cli)
[Flask-SSLify](https://github.com/kennethreitz/flask-sslify)