import easywebdav
import os
import datetime


class CloudBackup:
    """Backup files to private cloud storage
    @:param cloud   dictionary with host, port, protocol, username and password
    """

    def __init__(self, cloud):
        # Connect to WebDav
        self.w = easywebdav.connect(
            cloud['host'],
            port=cloud['port'],
            protocol=cloud['protocol'],
            username=cloud['username'],
            password=cloud['password'])

    def test(self):
        try:
            self.w.download('lala', 'lala')
            print('OK')
        except:
            print('Did not work')

    def upload(self, localfiles):
        try:
            remotepath = datetime.datetime.utcnow().isoformat().replace(':', '_')
            self.w.mkdir(remotepath)
        except:
            print('Dir creation did not work')

        for localfile in localfiles:
            try:
                remotefile = os.path.basename(localfile)

                remotefilepath = os.path.join(remotepath, remotefile)
                print('Uploading ' + localfile + ' to ' + remotefilepath)
                self.w.upload(localfile, remotefilepath)
            except:
                print('Did not work')

if __name__ == '__main__':
    print('Testing Cloud Storage')

    # Get host and credentials from secret file
    from secrets import mycloud as c

    cb = CloudBackup(c)

    cb.upload(['/home/pi/hap-deployed/boiler.rrd'])
