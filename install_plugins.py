import requests


JENKINS = "http://ci.pentaho.com/job"
JENKINS_TRUNK ="lastSuccessfulBuild/artifact"


def download  (url, dst_filename, output_folder):
	if output_folder == string.empty:
			full_output = dst_filename
	else:
		full_output = output_folder + '/' + dst_filename

    
    response = requests.get(full_url, stream=True)

    if response.status_code == 200:
    	download = r.raw.read()
		with open(full_output, 'w') as f:
        	f.write(download)


make_url = JENKINS + '/' + JENKINS_TRUNK + '/' + 'marketplace-TRUNK-SNAPSHOT.zip'
download (make_url, dst_filename, )