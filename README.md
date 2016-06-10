Server for file transfer over HTTPS

Required credentials: 
keys/server.crt 
keys/server.key

You can use 
```bash
#!/bin/bash
# Generates a SSL certificate and an RSA keypair

openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
openssl rsa -passin pass:x -in server.pass.key -out server.key
rm server.pass.key

openssl req -new -subj "/C=SE/ST=XX/L=XX/O=XX/CN=localhost" -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt 

openssl rsa -in server.key -pubout > server.pub 
```
to generate the credentials

Requires python-twisted
