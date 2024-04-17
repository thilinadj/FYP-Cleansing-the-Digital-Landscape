# For Dev: Command list
## Initiate the virtual environment
```
python -m venv .venv
```

## Activate the virtual environment
### bash command:
```bash
source .venv/Scripts/activate
```
### cmd command:
```cmd
.\.venv\Scripts\activate
```

## Update dependencies
```bash or cmd
pip freeze > requirements.txt
```

## Update dependencies which are in use
```bash or cmd
pipreqs --force
```

## Install dependencies
```bash or cmd
pip install -r requirements.txt
```

## Deactivate the venv
```bash or cmd
deactivate
```