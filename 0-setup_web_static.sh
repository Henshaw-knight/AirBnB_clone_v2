#!/usr/bin/env bash
# Bash script that sets up the web servers for the deployment of web_static

# install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
sudo apt-get -y update
sudo apt-get -y install nginx
fi


# Create necessary folders
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /datat/web_static/shared

# Create HTML file with simple content
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    Hello World!
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Delete symbolic link if it already exists
if [ -L "/data/web_static/current" ]; then
	rm -f /data/web_static/current
fi

# Create symbolic link
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i "/server_name _;/a\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

# Restart nginx server
sudo service nginx restart
