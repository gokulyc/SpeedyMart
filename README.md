# SpeedyMart

```bash
    # commands to run

    # clone the repo
    git clone https://github.com/gokulyc/SpeedyMart.git

    # setup pre-commit
    pip install -r requirements-dev.txt
    pre-commit install

    # Flask server
    python main.py


    # test cases
    pytest -s test_app.py

    # start app in docker
    docker compose up -d

    # start app in docker & rebuild images
    docker compose up -d --build

    # stop app in docker & destroy container
    docker compose down
```
