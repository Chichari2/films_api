# MovieDB_WebApp
An educational fullstack project about creating a web interface for account-based personal database management.

![image](https://github.com/user-attachments/assets/b8ab8885-0148-4982-ab39-2ef56442dc41)

## Project features
* Database management: sqlalchemy.orm
* Endpoint routing: Flask
* 3rd party API: OMDb
* Templating / dynamic webpage generation: Jinja2

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

## Feedback

If you have any feedback, feel free to reach out.

| <img src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" alt="gh_logo.png" width="15" height="15"/> | <img src="https://cdn3.iconfinder.com/data/icons/web-ui-3/128/Mail-2-512.png" alt="email_icon.jpg" width="15" height="15"/> |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [@MilosTadic01](github.com/MilosTadic01)                                                                                  | `milosgtadic` at yahoo.com                                                                                                       |


## License

[CC0 1.0 Universal](/LICENSE)
