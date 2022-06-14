# Parser and API for ReadManga.io

## API Endpoint: 

> /ping
### Job Check

```
{
    "status": "pong"
}
```

> /index
### Return json with list anime on index page 

```
[
    {
        "title": "",
        "url": "",
        "image": "",
        "description": "",
        "tags": [
            {
                "url": ,
                "name": ""
            },
        ]
    },
]
```

> /collections
### Return json with list collection on index page 

```
[
    {
        "url": "",
        "name": "",
        "image": ""
    },
]
```

## Install

> git clone {this_url}

> python3 -m venv pvenv

> enter in virtual environment

> pip install -r requirement.txt

> python main.py

### Default port: 8080

Or set environment variable _API_PORT_

__This is a demo project.__