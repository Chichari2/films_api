# MovieDB_WebApp
An educational fullstack project about creating a web interface for account-based personal database management.


## Project features and technologies overview
* Database management: sqlalchemy.orm
* Endpoint routing: Flask
* 3rd party API: OMDb
* Templating / dynamic webpage generation: Jinja2

## Installation

1. Clone the repository.

        git clone https://github.com/MilosTadic01/MovieDB_WebApp

2. Enter the created directory.

        cd MovieDB_WebApp

3. Create a virtual environment.

        python -m venv .

4. Activate the virtual environment.

        source ./bin/activate

5. Install the required packages for the venv.

        pip install -r requirements.txt

6. Obtain your personal API key from OMDb [here](https://www.omdbapi.com/apikey.aspx).

7. Add your key to your environment

        echo API_KEY=ReplaceThisWithYourKey > .env

> [!NOTE]
> These installation steps portray a generic case on UNIX-like systems (Linux, Mac OS).

## Usage/Examples

Run the app.
```bash
python app.py
```

Visit the now locally hosted homepage via any browser.
```
https://127.0.0.1:5001
```

> [!NOTE]
> If you wish to start your own database from scratch, delete the demo file `library.sqlite` in directory `data/`
