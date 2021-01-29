## Module Azure

### Introduction
This module is used to connect local to Microsoft Azure SQL database for later
processing. Functions are encapsulated and used in `app.py`. </br>
</br>
We may change this to Microsoft Azure IoT Hub.

### Dependencies
- [UnicODBC](http://www.unixodbc.org/)
- [FreeTDS](https://www.freetds.org/)
- [PyODBC](https://github.com/mkleehammer/pyodbc)

### Usage
Install packages via `apt` and `pip3`. For your convinence, we have prepared
a `setup.sh` to help you to install the packages and configuration files.
```
chmod +x setup.sh
./setup.sh
```

### Resources
[Connecting Raspberry Pi to Microsoft Azure with Python3](http://mdupont.com/Blog/Raspberry-Pi/azure-python3.html)
