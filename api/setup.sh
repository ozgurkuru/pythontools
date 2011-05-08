#!/usr/bin/bash


cp api.ini /etc/
mkdir -p /var/lib/api/cache
chmod 777 /var/lib/api/cache 
cp repocache.ini /var/lib/api/cache/
cp api.py /usr/bin/api
chmod a+x /usr/bin/api

