# Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: \venv\scripts\activate
pip install -r requirements.txt
```

# Run
then you can run the app:
```bash
python app.py
```

# Test
You will need to download the correct version of Chromedriver for your version of Chrome and put it in the same folder as your python.exe
```bash
pip install -r tests/requirements.txt
pytest  -v
```