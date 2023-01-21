<?php
$servername = "db-mysql-scott-do-user-12091905-0.b.db.ondigitalocean.com";
$username = "scottzmuda";
$password = "AVNS_wNEmYo_o8obEIcD69Km";
$dbname = "website";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    echo "Connection Successful";
    $conn->close();
?>
