# library-inventory-manager-Lokesh


# Library Manager


Simple command-line library manager in Python.


## Structure
- `library_manager/` - package containing core classes
- `cli/main.py` - command-line interface
- `data/books.json` - storage file created at runtime
- `logs/app.log` - log file


## How to run
1. Create a virtual environment and activate it.
2. Install requirements: `pip install -r requirements.txt` (none required for stdlib-only solution)
3. Run: `python -m cli.main` from project root.


## Notes
- Data is stored in `data/books.json`.
- Logs are stored in `logs/app.log`.
