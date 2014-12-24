import easywebdav


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

    def connect(self):
        try:
            self.w.download('lala', 'lala')
            print('OK')
        except:
            print('Did not work')

        self.w.session.close()

if __name__ == '__main__':
    print('Testing Cloud Storage')

    # Get host and credentials from secret file
    from secrets import mycloud as c

    cb = CloudBackup(c)
    cb.connect()
