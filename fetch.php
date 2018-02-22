<?php
//fetch tweet
require_once('mysql.inc.php');    # MySQL Connection Library
$db = new myConnectDB();          # Connect to MySQL

if (mysqli_connect_errno()) {
  echo "<h5>ERROR: " . mysqli_connect_errno() . ": " . mysqli_connect_error() . " </h5><br>";
}

//put into anntoatedDAta
if($_GET['insert'] == 'true') {
  // $tweet = $_GET['tweet'];
  $ID = $_GET['id'];
  $delTweet = $_GET['tweet'];

  $delTweet = str_replace('\'', '',$delTweet);
  $delTweet = str_replace('#', '',$delTweet);
  $delTweet = str_replace('"', '',$delTweet);
  // $delTweet = str_replace('(', '',$delTweet);
  // $delTweet = str_replace(')', '',$delTweet);


  $classification = $_GET['sentiment'];
  $query = "INSERT INTO annotated_Data (publicThought, classification) VALUES('$delTweet','$classification')";

  //prepare and execute sql query
  $stmt = $db->stmt_init();
  $stmt->prepare($query);
  $success = $stmt->execute();

  //check for errors
  if (!$success || $db->affected_rows == 0) {
    echo "<h5>ERROR: " . $db->error . " for query *$query*</h5><hr>";
  }

  $delete = "DELETE FROM rawTwats WHERE ID='$ID'";

  mysqli_query($db,$delete);
}

//get from rawTwats, c1 is ID, c2 is tweet
//selects random tweet to handle multiple users on site at once
$query = "SELECT * FROM rawTwats ORDER BY RAND() LIMIT 1";

//prepare and execute sql query
$stmt = $db->stmt_init();
$stmt->prepare($query);
$success = $stmt->execute();

//check for errors
if (!$success || $db->affected_rows == 0) {
  echo "<h5>ERROR: " . $db->error . " for query *$query*</h5><hr>";
}

//store results and increment ID
$stmt->store_result();
$insert_id = $stmt->insert_id;

// Retrieve the number of rows returned by the query
$num_rows = $stmt->num_rows;

//bind results so we can access rows
$stmt->bind_result($Tweet,$ID);
$stmt->fetch();
$Tweet = str_replace('\'', '',$Tweet);
$Tweet = str_replace('#', '',$Tweet);
$Tweet = str_replace('"', '',$Tweet);
echo "$Tweet $ID";
// echo "$insert_id";
// return $Tweet;

$db->close();

?>
