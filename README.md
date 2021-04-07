A dummy/mocking server to inspect incoming HTTP connections. Use it to test/debug Webhooks.

![hyper1080](https://user-images.githubusercontent.com/872296/113930350-89bbbb80-97c7-11eb-92a0-0efc63e72e38.gif)


```bash
$ docker run -it -p 5555:5555 santiagobasulto/hyper
```

### Installation

Using `pip`:

```bash
$ pip install hyper-inspector
```

Using `pipx`:

```bash
$ pipx install hyper-inspector
```

### Usage

```
$ hyper --help
usage: http_inspector [-h] [-r RESPONSE] [-f [ENABLE_FILE_LOGGING]] [-d LOGGING_DIRECTORY] [--log-body [LOG_BODY]] [--ip IP] [--port PORT]

Inspect and debug HTTP requests

optional arguments:
  -h, --help
            Show this help message and exit
  -r, --response [default 200]
            Default response for every incoming request
  -f, --enable-file-logging [default True]
            Enable file logging
  -d, --logging-directory [default .]
            Directory path to store logs
  --log-body [default True]
            Should it log the whole body to the console.
  --ip [default '']
            IP Addr to serve
  --port [default 555]
            Server Port to listen to
```

