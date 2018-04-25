# Installing cx_Oracle on Linux
```bash
yum install -y wget gcc openssl-devel tar unzip libaio
wget -P /tmp/ https://www.python.org/ftp/python/3.4.5/Python-3.4.5.tgz
tar xzf /tmp/Python-3.4.5.tgz  -C /tmp/
cd /tmp/Python-3.4.5
./configure --enable-optimizations
make altinstall
ln -s  /usr/local/bin/python3.4 /usr/bin/python3
ln -s /usr/local/bin/pip3.4 /usr/bin/pip3
pip3 install cx_Oracle
wget -P /tmp/ http://artifactory.amer.gettywan.com/artifactory/getty-mms/oracle/instantclient-basiclite-linux.x64-12.2.0.1.0.zip;\
mkdir -p /opt/oracle;\
unzip /tmp/instantclient-basiclite-linux.x64-12.2.0.1.0.zip -d /opt/oracle;\
sh -c "echo /opt/oracle/instantclient_12_2 > /etc/ld.so.conf.d/oracle-instantclient.conf";\
ldconfig;\
rm -rf /tmp/instantclient-basiclite-linux.x64-12.2.0.1.0.zip /tmp/Python-3.4.5.tgz
```
