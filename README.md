<p align="center"> ### HTTPS File Transfer Server </p>

```bash
./launch.sh
```

<p align="center"> #### Requirements </p>

###### TwistedWeb
```bash
sudo apt-get install python-twisted
```
or
```bash
pip install twisted
```


###### Credentials for encryption

Use 
```bash
#!/bin/bash
# Generates SSL certificate and RSA key

openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
openssl rsa -passin pass:x -in server.pass.key -out server.key
rm server.pass.key

openssl req -new -subj "/C=SE/ST=XX/L=XX/O=XX/CN=localhost" -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt 
```
to generate the credentials. Place them in a directory called "keys"


