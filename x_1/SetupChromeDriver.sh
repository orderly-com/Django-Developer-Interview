wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
sudo apt-get install xvfb 

wget https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip
sudo apt-get install unzip
unzip chromedriver_linux64.zip


sudo mv -f chromedriver /usr/local/share/chromedriver

sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

chmod a+x /usr/local/share/chromedriver
