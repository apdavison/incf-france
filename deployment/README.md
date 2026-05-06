docker build -t incf_france_web .
docker-compose run web python3 manage.py check
docker-compose run web python3 manage.py migrate --no-input
docker-compose run web python3 manage.py loaddata initial_data.json
docker-compose up -d --build
