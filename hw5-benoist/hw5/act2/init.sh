#!/bin/bash
mysql -u root -e "CREATE DATABASE IF NOT EXISTS armbook;"
mysql -u root armbook_packaged < /var/www/html/armbook.sql
