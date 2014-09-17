import requests, zipfile,os, sys, getopt

'''
 *
 * install_plugin.py
 *
 * Copyright (c) 2014, CARLOS EDUARDO SMANIOTO. All rights reserved.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301  USA
 */

 Email: csmanioto@gmail.com

'''

JENKINS = "http://ci.pentaho.com/job"
JENKINS_TRUNK = "lastSuccessfulBuild/artifact"
TMP_FOLDER = "/tmp/pytinstall/"
BISERVER_HOME = "/opt/pentaho/biserver-ce/"

def makeFolder (folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
    except IOError as e:
        print("makeFolder: " + e)

def removeFolder(folder):
    try:
        print("Removing ", folder)
        if (os.path.isdir(folder)):
                for path in (os.path.join(folder,f) for f in os.listdir(folder)):
                    print(path)
                    if os.path.isdir(path):
                        removeFolder(path)
                    else:
                        os.unlink(path)
                os.rmdir(folder)
    except IOError as e:
            print("RemoveFolder", e)
            pass
'''
def unzip(source_filename, dest_dir):
    try:
        print("Unziping  %s on %s" % (source_filename, dest_dir))
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
    except OSError as e:
        print("unzip: ", e)
'''
def Unzip(source_filename, dest_dir):
        zip = zipfile.ZipFile(source_filename,'r')
        zip.extractall(dest_dir)

def extractAll(zipName):
    z = zip(zipName)
    for f in z.namelist():
        if f.endswith('/'):
            os.makedirs(f)
        else:
            z.extract(f)

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
            break
    return dict


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

        if os.path.isfile(full_output):
            os.unlink(full_output)

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
        removeFolder(_system_folder + '/' + plugin_name)
        Unzip(downloaded_file, _system_folder)
        print("Plugin %s installed" % plugin_name)
    except Exception as e:
        print("InstallPluing: ", e)


def displayHelp(exit_status):
    print("--------------")
    plugin = ''
    for key in plugin_select(None):
        plugin = plugin + ' ' +  key["plugin"]

    print("Avaliable plugins: %s" % plugin)
    print("--------------")

    print("install_plugin.py -p plugin_name -b biserver_home -t tmpdir(optional)")
    print("Or full form :) ")
    print("install_plugin.py --plugin=plugin_name --bihome=biserver_home --tmpdir=tmpdir(optional)")

    sys.exit(exit_status)


def main(argv):

    plugin_name = ''
    biserver_home = ''
    tmpdir = ''

    try:
        paramenters, values = getopt.getopt(argv,"hp:b:t:",["help","plugin=","bihome=","tmpdir="])
    except getopt.GetoptError:
        displayHelp(2)

    if len(paramenters) == 0:
        displayHelp(2)


    for opt, arg in paramenters:
         if opt in ('-h', '--help'):
             displayHelp(2)
         if opt in ('-p', '--plugin'):
             plugin_name = arg
         if opt in ('-b', '--bihome'):
             biserver_home = arg
         if opt in ('-t', '--tmpdir'):
             tmpdir = arg

    if (tmpdir == None) or (tmpdir == ''):
           tmpdir= TMP_FOLDER

    if (biserver_home == None) or (biserver_home == ''):
        biserver_home = BISERVER_HOME

    installPlugin(plugin_name, tmpdir, biserver_home)

if __name__ == "__main__":
    main(sys.argv[1:])