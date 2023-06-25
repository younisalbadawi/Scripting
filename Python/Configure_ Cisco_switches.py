from netmiko import ConnectHandler

def configure_switch(ip, username, password, vlan_id, interface):
    # Define device parameters
    device = {
        'device_type': 'cisco_ios',
        'ip':   ip,
        'username': username,
        'password': password,
    }

    # Establish SSH connection
    connection = ConnectHandler(**device)

    # Configure VLAN
    connection.send_command('enable')
    connection.send_command('conf t')
    connection.send_command(f'vlan {vlan_id}')
    connection.send_command('exit')

    # Configure port security
    connection.send_command(f'interface {interface}')
    connection.send_command('switchport mode access')
    connection.send_command(f'switchport access vlan {vlan_id}')
    connection.send_command('switchport port-security')
    connection.send_command('switchport port-security maximum 1')
    connection.send_command('switchport port-security violation restrict')
    connection.send_command('switchport port-security mac-address sticky')
    connection.send_command('end')

    # Close SSH connection
    connection.disconnect()

# List of switches
switches = [
    {'ip': '192.168.1.1', 'username': 'admin', 'password': 'password', 'vlan_id': '10', 'interface': 'GigabitEthernet0/1'},
    {'ip': '192.168.1.2', 'username': 'admin', 'password': 'password', 'vlan_id': '20', 'interface': 'GigabitEthernet0/2'},
    # Add more switches as needed
]

# Use the function on each switch
for switch in switches:
    configure_switch(switch['ip'], switch['username'], switch['password'], switch['vlan_id'], switch['interface'])
