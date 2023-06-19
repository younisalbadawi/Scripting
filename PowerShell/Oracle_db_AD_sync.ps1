# Load the Oracle client library
Add-Type -Path "C:\path\to\Oracle.ManagedDataAccess.dll"

# Define Oracle connection string
$oracleConnectionString = "Data Source=(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=YourOracleServer)(PORT=YourPort)))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=YourServiceName)));User Id=YourUsername;Password=YourPassword;"

# Create Oracle connection
$oracleConnection = New-Object Oracle.ManagedDataAccess.Client.OracleConnection($oracleConnectionString)

# Open Oracle connection
$oracleConnection.Open()

# Define SQL query to get employee details
$sql = "SELECT * FROM employees"

# Create Oracle command
$command = New-Object Oracle.ManagedDataAccess.Client.OracleCommand($sql, $oracleConnection)

# Execute the command and store the results
$reader = $command.ExecuteReader()

# Loop through the results
while ($reader.Read()) {
    # Get employee details
    $employeeId = $reader["employee_id"]
    $firstName = $reader["first_name"]
    $lastName = $reader["last_name"]
    $email = $reader["email"]

    # Find the corresponding user in Active Directory
    $adUser = Get-ADUser -Filter "EmailAddress -eq '$email'"

    # If the user exists in Active Directory, update their details
    if ($adUser) {
        Set-ADUser -Identity $adUser.SamAccountName -GivenName $firstName -Surname $lastName
    }
}

# Close Oracle connection
$oracleConnection.Close()






# Load the ODBC .NET data provider
Add-Type -TypeDefinition @"
using System;
using System.Data;
using Microsoft.Data.Odbc;

public class OdbcDatabase
{
    public static OdbcDataReader ExecuteQuery(string connectionString, string query)
    {
        OdbcConnection connection = new OdbcConnection(connectionString);
        connection.Open();
        OdbcCommand command = new OdbcCommand(query, connection);
        return command.ExecuteReader(CommandBehavior.CloseConnection);
    }
}
"@

# Define ODBC connection string
$odbcConnectionString = "Driver={Oracle in OraClient11g_home1};Dbq=YourTNSName;Uid=YourUsername;Pwd=YourPassword;"

# Define SQL query to get employee details
$sql = "SELECT * FROM employees"

# Execute the query and store the results
$reader = [OdbcDatabase]::ExecuteQuery($odbcConnectionString, $sql)

# Loop through the results
while ($reader.Read()) {
    # Get employee details
    $employeeId = $reader["employee_id"]
    $firstName = $reader["first_name"]
    $lastName = $reader["last_name"]
    $email = $reader["email"]

    # Find the corresponding user in Active Directory
    $adUser = Get-ADUser -Filter "EmailAddress -eq '$email'"

    # If the user exists in Active Directory, update their details
    if ($adUser) {
        Set-ADUser -Identity $adUser.SamAccountName -GivenName $firstName -Surname $lastName
    }
}

# Close the reader
$reader.Close()
