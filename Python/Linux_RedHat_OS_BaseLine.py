import paramiko

def configure_security_baseline(ip, username, password):
    # Create a new SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    client.connect(ip, username=username, password=password)

    # List of commands to configure security baseline
    commands = [
        'sudo yum update -y',  # Update all packages
        'sudo yum install -y firewalld',  # Install firewalld
        'sudo systemctl start firewalld',  # Start firewalld
        'sudo systemctl enable firewalld',  # Enable firewalld to start on boot
        'sudo setenforce 1',  # Enable SELinux
        'sudo systemctl disable sshd',  # Disable SSH to prevent remote logins
        # Add more commands as needed
    ]

    # Execute each command
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

    # Close the connection
    client.close()

# Use the function
configure_security_baseline('192.168.1.1', 'root', 'password')
