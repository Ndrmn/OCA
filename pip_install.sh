
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# db commands
export FLASK_APP=run.py
export FLASK_DEBUG=1
flask db init
flask db migrate
flask db upgrade
flask test
