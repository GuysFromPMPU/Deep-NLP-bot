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
```