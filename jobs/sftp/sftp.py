import paramiko
from django.conf import settings
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException


# Create and return an SSH client instance
def get_ssh_client(hostname, username, password):
    try:
        ssh_client = paramiko.SSHClient()

        if settings.ALLOW_SSH_UNKNOWN_HOSTS:
            # If true, this will permit connection to unknown SSH servers
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Will establish a connection to specified SSH server on port 22
        ssh_client.connect(
            hostname=hostname,
            username=username,
            password=password,
        )

        return ssh_client
    except AuthenticationException:
        print('Authentication failed, please verify your credentials: %s')
        raise AuthenticationException('AuthenticationException: %s')
    except SSHException as sshException:
        print('Unable to establish SSH connection: %s' % sshException)
        raise AuthenticationException('Unable to establish SSH connection: %s' % sshException)
    except BadHostKeyException as badHostKeyException:
        print('Unable to verify server\'s host key: %s' % badHostKeyException)
        raise AuthenticationException('Unable to verify server\'s host key: %s' % badHostKeyException)

# Create and return an SFTP connection client
def get_sftp_client(ssh_client):
    try:
        return ssh_client.open_sftp()
    except Exception as e:
        print('Exception occurred while opening an SFTP connection: ' + e.message)
        raise Exception('Exception occurred while opening an SFTP connection: ' + e.message)
