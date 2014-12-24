
import paramiko
from secrets import rpi_boiler


""" Deploy the project to all network connected devices.

Used to update all files on distributed devices when developing.

Documentation:
 * http://jessenoller.com/blog/2009/02/05/ssh-programming-with-paramiko-completely-different
 * http://blog.frd.mn/how-to-set-up-proper-startstop-services-ubuntu-debian-mac-windows/

Steps not done by the script:
 * Setup Debian service on RPi boiler
   # sudo wget https://raw.github.com/d4v1dw388/service-daemons/master/debian -O /etc/init.d/hap-log-boiler
   # sudo nano /etc/init.d/hap-log-boiler
   # sudo chmod +x /etc/init.d/hap-log-boiler
   # sudo update-rc.d hap-log-boiler defaults
   # sudo service hap-log-boiler start

"""
class Deploy:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            rpi_boiler['host'],
            username=rpi_boiler['username'],
            password=rpi_boiler['password'])
        pass

    def deploy(self):
        # Stop service
        stdin, stdout, stderr = self.ssh.exec_command("sudo service hap-log-boiler stop")
        print(stdout.readlines())
        print(stderr.readlines())

        # Deploy log-boiler.py to hap-deployed on RPi
        ftp = self.ssh.open_sftp()
        filelist = ['log-boiler.py', 'cloud-backup.py']
        for f in filelist:
            ftp.put(f, 'hap-deployed/' + f)
        ftp.close()

        # Start service
        stdin, stdout, stderr = self.ssh.exec_command("sudo service hap-log-boiler start")
        print(stdout.readlines())
        print(stderr.readlines())


if __name__ == '__main__':
    print('Testing Deploy')
    d = Deploy()
    d.deploy()
