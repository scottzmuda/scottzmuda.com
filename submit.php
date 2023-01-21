<?php
//Validate the form data
if(empty($_POST['title']) || empty($_POST['description']) || empty($_POST['writing'])){
    echo "Please fill all the fields";
    exit;
}

//Connect to the database
$servername = "db-mysql-scott-do-user-12091905-0.b.db.ondigitalocean.com";
$username = "scottzmuda";
$password = "AVNS_wNEmYo_o8obEIcD69Km";
$dbname = "website";
$port = "25060"

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname, $port);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//Get the form data
$title = $_POST['title'];
$description = $_POST['description'];
$writing = $_POST['writing'];

//Insert data into the table
$sql = "INSERT INTO creations (title, description, writing) VALUES ($title, $description, $writing)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("sss", $title, $description, $writing);
$stmt->execute();

//Check if data was inserted successfully
if($stmt->affected_rows === 1){
    echo "Data inserted successfully";
}else{
    echo "Error: " . $stmt->error;
}

$stmt->close();
$conn->close();