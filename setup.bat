@echo off
echo Setting up Awesome Portfolio...

mkdir awesome-portfolio
cd awesome-portfolio

python -m venv venv
call venv\Scripts\activate

mkdir templates

echo Flask==2.3.3 > requirements.txt
echo python-dotenv==1.0.0 >> requirements.txt
echo gunicorn==21.2.0 >> requirements.txt
echo flask-cors==4.0.0 >> requirements.txt

pip install -r requirements.txt

echo FLASK_APP=app.py > .env
echo FLASK_ENV=development >> .env
echo SECRET_KEY=dev-secret-key-change-in-production >> .env
echo FLASK_DEBUG=1 >> .env
echo PORT=5000 >> .env

echo Setup complete!
echo Next steps:
echo 1. Copy the app.py code into app.py
echo 2. Copy the HTML files into the templates folder
echo 3. Run: python app.py
echo 4. Visit: http://localhost:5000