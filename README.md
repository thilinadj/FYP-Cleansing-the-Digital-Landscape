# For Dev: Command list
## Initiate the virtual environment
python -m venv .venv

## Activate the virtual environment
### bash command:
source .venv/Scripts/activate
### cmd command:
.\.venv\Scripts\activate

## Update dependencies
pip freeze > requirements.txt

## Install dependencies
pip install -r requirements.txt

## Deactivate the venv
deactivate