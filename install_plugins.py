import requests, zipfile,os.path

JENKINS = "http://ci.pentaho.com/job"
JENKINS_TRUNK = "lastSuccessfulBuild/artifact"
TMP_FOLDER = "/tmp"
#

def makeFolder (folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
    except IOError as e:
        print("makeFolder: " + e)


def removeFolder(folder):
    try:
        for path in (os.path.join(folder,f) for f in os.listdir(folder)):
            if os.path.isdir(path):
                print("Removing ", folder)
                removeFolder(folder)
            else:
                os.unlink(path)
                os.rmdir(folder)
    except IOError as e:
            print(e)

def unzip(source_filename, dest_dir):
    try:
        with zipfile.ZipFile(source_filename) as zf:
            for member in zf.infolist():
                # Path traversal defense copied from
                # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
                words = member.filename.split('/')
                path = dest_dir
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''): continue
                    path = os.path.join(path, word)
                zf.extract(member, path)
    except IOError as e:
        print("unzip: " + e)


def plugin_select(plugin_name):

    """
    Dict with five index
    'plugin':
    'pluginalias':
    'url':
    'file':
    'version':
    """

    dict = [{'plugin': 'marketplace', 'pluginalias': 'marketplace',    'url': 'http://ci.pentaho.com/job/marketplace/lastSuccessfulBuild/artifact/dist/', 'file': 'marketplace-TRUNK-SNAPSHOT.zip', 'version': 'trunk'},
            {'plugin': 'cdf-pentaho', 'pluginalias': 'cdf', 'url': 'http://ci.pentaho.com/job/pentaho-cdf-pentaho/lastSuccessfulBuild/artifact/cdf-pentaho/dist/', 'file': 'pentaho-cdf-TRUNK-SNAPSHOT.zip', 'version': 'trunk'},
            {'plugin': 'cda-pentaho', 'pluginalias': 'cda', 'url': 'http://ci.pentaho.com/job/pentaho-cdf-pentaho/lastSuccessfulBuild/artifact/cda-pentaho/dist/', 'file': 'cda-TRUNK-SNAPSHOT.zip', 'version': 'trunk'},
            {'plugin': 'cde-pentaho', 'pluginalias': 'cde', 'url': 'http://ci.pentaho.com/job/pentaho-cde-pentaho/lastSuccessfulBuild/artifact/cde-pentaho/dist/', 'file': 'pentaho-cdf-dd-TRUNK-SNAPSHOT.zip', 'version': 'trunk'},
            {'plugin': 'cgg-pentaho', 'pluginalias': 'cgg', 'url': 'http://ci.pentaho.com/job/pentaho-cgg-pentaho/lastSuccessfulBuild/artifact/cgg-pentaho/dist/', 'file': 'cgg-TRUNK-SNAPSHOT.zip', 'version': 'trunk'},
            {'plugin': 'cfr-pentaho', 'pluginalias': 'cfr', 'url': 'http://ci.pentaho.com/job/pentaho-cfr-pentaho/lastSuccessfulBuild/artifact/cfr-pentaho/dist/', 'file': 'cfr-TRUNK-TRUNK-SNAPSHOT.zip','version': 'trunk' },
            {'plugin': 'sparkl', 'pluginalias': 'sparkl',   'url': 'http://ci.pentaho.com/job/SparkllastSuccessfulBuild/artifact/dist/', 'file': 'sparkl-TRUNK-SNAPSHOT.zip', 'version': 'TRUNK'},
            {'plugin': 'saiku', 'pluginalias': 'saiku',     'url': 'http://meteorite.bi/downloads/', 'file': 'saiku-plugin-2.6.zip', 'version': 'stable'}]

    for key in dict:
        if (key["plugin"] == plugin_name)  or (key["pluginalias"] == plugin_name):
            return key


def download(url, dst_filename, output_folder):
    """
    :param url: Full URL of object
    :param dst_filename:  Name of downloaded file in the system
    :param output_folder: Folder to download
    :return: full path of file downloaded
    """
    if output_folder == None:
        full_output = dst_filename
    else:
        full_output = output_folder + '/' + dst_filename

    try:
        response = requests.get(url, stream=True)
        print("Download " + url + " on " + full_output)
        if response.status_code == 200:
            print("Starting download...")
            with open(full_output, 'wb') as f:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        return full_output
    except requests.ConnectionError as e:
        print("download: ", e)


def installPlugin (plugin_name, tmp_folder, biserver_folder):
    """
    :param plugin_name: Plugin ou Plugin ALias for install
    :param tmp_folder:  TMP DIR for download
    :param biserver_folder: Folder of instation of biserver
    :return: OK or FAILED
    """
    try:
        selected_dict =  {}
        selected_dict = plugin_select(plugin_name)
        plugin_name = selected_dict["plugin"]
        plugin_url = selected_dict["url"] + selected_dict["file"]
        _system_folder = biserver_folder + 'pentaho-solutions/system'
        downloaded_file = download(plugin_url, 'plugin.zip', makeFolder(tmp_folder + '/' + plugin_name ))


       # removeFolder(_system_folder + '/' + plugin_name)
       # unzip(downloaded_file, _system_folder)
    except Exception as e:
        print("InstallPluing: ", e)



installPlugin("marketplace", "/tmp/pytinstall", "/opt/pentaho/biserver-ce/")