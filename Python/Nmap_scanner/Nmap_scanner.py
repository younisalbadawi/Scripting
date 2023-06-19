import nmap
import requests

# Define the IP range
ip_range = "10.0.0.0/24"

# Initialize the port scanner
nm = nmap.PortScanner()

# Scan the network for hosts
nm.scan(hosts=ip_range, arguments='-p 1-65535')

# Open the output file
with open('output.txt', 'w') as f:
    # Loop through all hosts that are up
    for host in nm.all_hosts():
        f.write(f"Host: {host}\n")

        # List all open ports
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                if nm[host][proto][port]['state'] == 'open':
                    f.write(f"Port : {port} is open\n")

        # Try to connect to the web server and get the Server header
        try:
            response = requests.get(f"http://{host}", timeout=5)
            if 'Server' in response.headers:
                f.write(f"Web server: {response.headers['Server']}\n")
            else:
                f.write("Could not determine web server\n")
        except requests.exceptions.RequestException:
            f.write("Could not connect to web server\n")
