<!-- //php script to insert into table -->

<?php
$tweet = "#Hello my friend";
echo $tweet. "<br><br>";
$tweet = str_replace('#', '',$tweet);

echo $tweet;
?>
