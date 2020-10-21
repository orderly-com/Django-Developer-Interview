source .env
# echo $projname
# echo $appnames

python $projname/manage.py makemigrations $appnames
python $projname/manage.py migrate