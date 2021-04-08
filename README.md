A dummy/mocking server to inspect incoming HTTP connections. Use it to test/debug Webhooks. Provides nice console logging + a dump of every request as a file.

<p align="center">
  <img width="900px" src="https://user-images.githubusercontent.com/872296/114039073-cf749480-9858-11eb-8db9-981f18b9d12c.gif">
</p>

```bash
$ docker run -it -p 5555:5555 -v $(pwd)/logs:/app santiagobasulto/hyper
```

Explanation:
* `-p P1:5555`, `P1` is the local port in your host.
* `-v YOUR_PATH:/app`, `YOUR_PATH` is a volume in your file system to store the logs of the requests.

Logs names have the convention `METHOD.PATH.TIMESTAMP.request.json` and `METHOD.PATH.TIMESTAMP.body.EXTENSION` (if a body is sent). For example, `POST.some.path.1617889344.request.json` and `POST.some.path.1617889344.body.json`

If you don't want to store the logs, don't pass a `-v` option.

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

