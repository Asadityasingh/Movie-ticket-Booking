celery -A workers.celery worker -l info


celery -A app.celery beat --max-interval 1 -l info
source .venv/bin/activate
redis-server

ps aux | grep redis
kill <pid>

npm run serve
npm install
python3 app.py