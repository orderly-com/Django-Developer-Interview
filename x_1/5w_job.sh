input=".env"
while IFS= read -r line
do
    export "$line"
done < "$input"
python3.7 -m pipenv run python $projname/manage.py runapscheduler
