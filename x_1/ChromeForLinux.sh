# install google chrome
wget  -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get -y update
apt-get install -y google-chrome-stable

# install chromedriver
apt-get install -yqq unzip
wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
unzip -o /tmp/chromedriver.zip chromedriver -d /usr/local/bin/















# apt-get update -qqy
# name isnt: chromium-browser
# apt-get install -qqy libgconf-2-4 libglib2.0-0 libnss3 libx11-6 chromium  xvfb gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 lsb-release xdg-utils 


# echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# apt-get -qqy install google-chrome-stable
# rm -rf /etc/apt/sources.list.d/google-chrome.list
# rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# mkdir -p /var/www/logs


# wget --nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# dpkg -i google-chrome-stable_current_amd64.deb
# apt-get install -y -f


# apt-get install -qqy unzip
# wget -qnc https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip
# unzip -qqn chromedriver_linux64.zip


# cp -f chromedriver /usr/local/bin/chromedriver
# chmod +x /usr/local/bin/chromedriver


# cp -f chromedriver /usr/local/share/chromedriver
# ln -sf /usr/local/share/chromedriver /usr/local/bin/chromedriver
# ln -sf /usr/local/share/chromedriver /usr/bin/chromedriver
# chmod +x /usr/local/share/chromedriver


# wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get update -qqy && \
#     apt-get -qqy install google-chrome-stable && \
#     rm /etc/apt/sources.list.d/google-chrome.list && \
#     rm -rf /var/lib/apt/lists/* /var/cache/apt/*