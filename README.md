# Python Password Manager

A simple local password manager written in Python and MariaDB. Uses [pbkdf2](https://en.wikipedia.org/wiki/PBKDF2) to derive a 256 bit key from a MASTER PASSWORD and DEVICE SECRET to use with AES-256 for encrypting/decrypting.


# Installation
You need to have python3 to run this on Windows, Linux or MacOS
## Linux
### Install Python Requirements
```
sudo apt install python3-pip
pip install -r requirements
```

### MariaDB
```
sudo apt update
sudo apt install mariadb-server
```
#### Create user 'sp' and grant permissions
**Login to mysql as root**
```
sudo mysql -u root
```
**Create User**
```
CREATE USER 'sp'@localhost IDENTIFIED BY 'password';
```
**Grant privileges**
```
GRANT ALL PRIVILEGES ON *.* TO 'sp'@localhost IDENTIFIED BY 'password';
```

### Pyperclip
[Pyperclip](https://pypi.org/project/pyperclip/) is a python module used to copy data to the clipboard. If you get a "not implemented error", follow this simple fix: https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error


## Run
### Configure

You need to first configure the password manager by choosing a MASTER PASSWORD. This config step is only required to be executed once.
```
python config.py make
```
The above command will make a new configuration by asking you to choose a MASTER PASSWORD.
This will generate the DEVICE SECRET, create db and required tables.

```
python config.py delete
```
The above command will delete the existing configuration. Doing this will completely delete your device secret and all your entries and you will loose all your passwords. So be aware!

```
python config.py remake
```
The above command will first delete the existing configuration and create a fresh new configuration by asking you to choose a MASTER PASSWORD, generate the DEVICE SECRET, create the db and required tables.

### Usage
```
./simplePass.py -h
usage: simplePass.py [-h] [-s NAME] [-u URL] [-e EMAIL] [-l LOGIN] [--length LENGTH] [-c] option

Description

positional arguments:
  option                (a)dd / (e)xtract / (g)enerate

optional arguments:
  -h, --help            show this help message and exit
  -s NAME, --name NAME  Site name
  -u URL, --url URL     Site URL
  -e EMAIL, --email EMAIL
                        Email
  -l LOGIN, --login LOGIN
                        Username
  --length LENGTH       Length of the password to generate
  -c, --copy            Copy password to clipboard
```


### Add entry
```
./simplePass.py add -s mysite -u mysite.com -e hello@email.com -l myusername
```
### Retrieve entry
```
./simplePass.py extract
```
The above command retrieves all the entries
```
./simplePass.py e -s mysite
```
The above command retrieves all the entries whose site name is "mysite"
```
./simplePass.py e -s mysite -l myusername
```
The above command retrieves the entry whose site name is "mysite" and username is "myusername"
```
./simplePass.py e -s mysite -l myusername --copy
```
The above command copies the password of the site "mysite" and username "myusername" into the clipboard
### Generate Password
```
./simplePass.py g --length 15
```
The above command generates a password of length 15 and copies to clipboard
