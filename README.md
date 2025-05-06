# Django-Office-Management
A simple office management system using Django.

This project is also replicated using different frameworks in frontend and backend. Those projects are,
1. Office-Management-Django-Angular
2. Office-Management-Django-Angualr-JWT
3. Office-Management-.NET-Angular-JWT

# Features
1. Own account management
2. Inventory management
3. Leave management
4. Asset management

# Run
1. conda create --name <env>
2. conda activate <env>
3. python manage.py runserver

# Installation
Requirement:
* for anaconda: conda install -c anaconda django
1. pip install django-bootstrap-v5
2. pip install django mysqlclient
3. For MySQL in windows, install XAMPP. For Linux see section below on "Linux Environment"

# Operation
1. To make an inventory approver account, it should have canApproveInventory permission in Profile table. (can be updated from admin panel or DB)
2. To make an inventory distributor account, it should have canDistributeInventory permission in Profile table. (can be updated from admin panel or DB)
3. To make a leave approver account, it should have canApproveLeave permission in Profile table. (can be updated from admin panel or DB)
4. To make an asset manager account, it should have canManageAsset permission in Profile table. (can be updated from admin panel or DB)

# ---- Linux Environment ----
# Setting up environment
1. sudo apt install apache2
2. sudo apt install mysql-server
3. sudo mysql_secure_installation
4. sudo apt install php libapache2-mod-php php-mysql
5. sudo apt install phpmyadmin php-mbstring gettext
6. sudo phpenmod mbstring
7. sudo systemctl restart apache2

# Configuring root(optional):
1. sudo mysql
2. SELECT user,authentication_string,plugin,host FROM mysql.user;
3. ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '*****';
4. FLUSH PRIVILEGES;
5. mysql -u root -p
6. CREATE USER 'saikat'@'localhost' IDENTIFIED BY 'password';
7. GRANT ALL PRIVILEGES ON *.* TO 'saikat'@'localhost' WITH GRANT OPTION;
8. exit

# Apache remote access:
1. sudo ufw app list
2. sudo ufw allow in "Apache"
3. sudo ufw status

# Troubleshooting:
1. sudo gedit /etc/apache2/apache2.conf
2. Add "Include /etc/phpmyadmin/apache.conf"
3. sudo service apache2 restart

Note:
1. To generate spec list file -> conda list --explicit > <file_name>.txt
2. To generate environment.yml file -> conda env export --name <environment_name> > <file_name>.yml
3. To generate requirements.txt file -> pip freeze > requirements.txt or conda list -e > requirements.txt and to create a new environment pip install -r requirements.txt or conda create --name <env_name> --file requirements.txt
4. to update all packages -> conda update -all
