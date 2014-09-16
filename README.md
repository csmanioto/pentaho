pentaho
=======
Docker
  => Docker files for buinding a new containter of pentaho(Biserver, PDI, etc)
  
  Download de file and rename to Dockefile:
  mv BiServer.dockfile Dockefile
  docker build ...
Tools
  => AutoInstall for plugin in biserver:
    install_plugins.py -p cdf-pentaho -b /opt/pentaho/biserver-ce/
