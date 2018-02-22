

<?php
// php annotator
// table = annotated_Data
// columns = publicThought (comment/text)
// classification = int (that will be put in as we annotate)
  // mysql.inc.php - This file will be used to establish the database connection.
  class myConnectDB extends mysqli{
    public function __construct($hostname="midn.cs.usna.edu",
        $user="earnings",
        $password="severnblend",
        $dbname="capstone-earnings"){
      parent::__construct($hostname, $user, $password, $dbname);
    }
  }
?>
