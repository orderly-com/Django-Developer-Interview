input=".env"
while IFS= read -r line
do
    export "$line"
done < "$input"


makemigrations="python3.7 -m pipenv run python $projname/manage.py makemigrations $appnames"
migrate="python3.7 -m pipenv run python $projname/manage.py migrate"


echo $makemigrations | bash -x
echo $migrate | bash -x
