Make the script executable:

chmod +x apache2config.py

move script to usr/local/bin directory - remember to drop the .py extension

Update control file in DEBIAN directory

Build .deb package with: 
dpkg-deb --build apache2config_1.0-1
(Change version number as needed)

Can then install .deb as normal and run app with 'apache2config'.