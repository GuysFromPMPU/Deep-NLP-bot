# Bot for Moscow philharmonia
***
[iOS app github repo](https://github.com/magauran/Chaikovsky)
***
How ro run Alice and REST API:
* install requirements from `requirments.txt`
* install [`deeppavlov`](https://github.com/deepmipt/DeepPavlov)
* download `deeppavlov` models
* start `deeppavlov`models:
    * *Windows*:
        ```
        run_pavlov.bat
        ```
    * *Linux*:
        ```
        ./run_pavlov.sh
        ```
* start `flask` app with api (both for Alice, and rest)
    * *Windows*:
        ```
        run_flask.bat
        ```
    * *Linux*:
        ```
        ./run_flask.sh
        ```
* (*optional*) run `ngrok` for localhost tunneling if needed:

```
./ngrok http 5000
```

***
How to run vk bot:
* see `vk-bot` folder

***

If you want to create https certificate this links may be helpful:
* [best](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)
* [docs1](http://flask.pocoo.org/snippets/111/)
* [docs2](http://werkzeug.pocoo.org/docs/0.14/serving/)
* [run with cert](https://stackoverflow.com/questions/48467835/run-flask-dev-server-over-https-using-cli)
* [Flask-SSLify](https://github.com/kennethreitz/flask-sslify)
