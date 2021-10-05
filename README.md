# Django-Office-Management
A simple office management system using Django

# Features
1. Own account management
2. Inventory management
3. Leave management
4. Asset management (in progress)

# Installation
Requirement:
* for anaconda: conda install -c anaconda django
1. pip install django-bootstrap-v5
2. pip install django mysqlclient

Linux:
1. sudo apt install apache2
2. sudo apt install mysql-server
3. sudo mysql_secure_installation
4. sudo apt install php libapache2-mod-php php-mysql
5. sudo apt install phpmyadmin php-mbstring gettext
6. sudo phpenmod mbstring
7. sudo systemctl restart apache2

Configuring root(optional):
1. sudo mysql
2. SELECT user,authentication_string,plugin,host FROM mysql.user;
3. ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '*****';
4. FLUSH PRIVILEGES;
5. mysql -u root -p
6. CREATE USER 'saikat'@'localhost' IDENTIFIED BY 'password';
7. GRANT ALL PRIVILEGES ON *.* TO 'saikat'@'localhost' WITH GRANT OPTION;
8. exit

Apache remote access:
1. sudo ufw app list
2. sudo ufw allow in "Apache"
3. sudo ufw status

Troubleshooting:
1. sudo gedit /etc/apache2/apache2.conf
2. Add "Include /etc/phpmyadmin/apache.conf"
3. sudo service apache2 restart

# Operation
1. To make an inventory approver account, it should have canApproveInventory permission in Profile table. (can be updated from admin panel or DB)
2. To make a inventory distributor account, it should have canDistributeInventory permission in Profile table. (can be updated from admin panel or DB)
3. To make a leave approver account, it should have canApproveLeave permission in Profile table. (can be updated from admin panel or DB)

