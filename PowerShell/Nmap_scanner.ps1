# Define the IP range
$ip_range = 1..254 | ForEach-Object { "10.0.0.$_" }

# Define the port range
$port_range = 1..65535

# Initialize the output file
$outputFile = "output.txt"

# Loop through all hosts in the IP range
foreach ($ip in $ip_range) {
    # Loop through all ports in the port range
    foreach ($port in $port_range) {
        # Test the connection to the current IP and port
        $connection = Test-NetConnection -ComputerName $ip -Port $port -WarningAction SilentlyContinue

        # If the connection is successful, write the IP and port to the output file
        if ($connection.TcpTestSucceeded) {
            Add-Content -Path $outputFile -Value "Host: $($connection.ComputerName)"
            Add-Content -Path $outputFile -Value "Port : $($connection.RemotePort) is open"

            # Try to connect to the web server and get the Server header
            try {
                $response = Invoke-WebRequest -Uri "http://$ip" -TimeoutSec 5 -UseBasicParsing
                if ($response.Headers.Server) {
                    Add-Content -Path $outputFile -Value "Web server: $($response.Headers.Server)"
                } else {
                    Add-Content -Path $outputFile -Value "Could not determine web server"
                }
            } catch {
                Add-Content -Path $outputFile -Value "Could not connect to web server"
            }
        }
    }
}
