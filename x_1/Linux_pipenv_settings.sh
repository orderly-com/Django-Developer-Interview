input=".env"
while IFS= read -r line
do
    export "$line"
done < "$input"



pipenv____________="python3.7 -m pipenv "

pipenv_shell______=$pipenv____________"shell"
pipenvrun_________=$pipenv____________"run "

pipenv_run_manage_=$pipenvrun_________"python $projname/manage.py "


pipenv_rm_________=$pipenv____________"--rm" 
pipenv_install____=$pipenv____________"install" 
makemigrations____=$pipenv_run_manage_"makemigrations $appnames" 
migrate___________=$pipenv_run_manage_"migrate" 
runserver_________=$pipenv_run_manage_"runserver"
qcluster__________=$pipenv_run_manage_"qcluster"
create_super_user_="python $projname/manage.py ""createsuperuser"



echo ""


echo 0: $pipenv_rm_________
echo 1: $pipenv_install____
echo 2: $makemigrations____ '\n & '$migrate___________
echo ""




echo "(manual)" $pipenv_shell______
echo "(manual)" $create_super_user_
echo ""



echo 3: $qcluster__________
echo 4: $runserver_________
echo ""




read -p " which ? " step
case $step in 
    0 ) 
        echo $pipenv_rm_________ | bash -x
        ;;
    1 )
        echo $pipenv_install____ | bash -x
        ;;
    2 )
        echo $makemigrations____ | bash -x
        echo $migrate___________ | bash -x
        ;;
    3 )
        echo $qcluster__________ | bash -x
        ;;
    4 )
        echo $runserver_________ | bash -x 
        ;;
    * )
        echo "       ? \e[30;47mWHAT\e[0m ?"
esac
