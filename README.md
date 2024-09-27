# MovieDB_WebApp
an educational fullstack project about creating a web interface for a personal database management via CRUD.

## Installation

> [!NOTE]
> These installation steps portray a generic case on UNIX-like systems (Linux, Mac OS).

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

## Usage/Examples

Run the app.
```bash
python app.py
```

Visit the now locally hosted homepage via any browser.
```
https://127.0.0.1:5000
```

> [!NOTE]
> If you wish to start your own database from scratch, delete the demo file `library.sqlite` in directory `data/`
