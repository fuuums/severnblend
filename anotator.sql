/***
 *** This is how to create a data table. varchar array of chars, string
 ***/
CREATE TABLE Anotator (
  Tweet varchar(255),
  Source varchar(255),
  Sentiment varchar(255)

);

/***
 *** This is the syntax to insert a new line to the table.
 *** It can intake vars, must be comma separated
 ***/
INSERT INTO Anotator
VALUES ("walker is dope", "God", "fantastic");

/***
 *** SELECT prints out desired column. * like other languages,
 *** prints everything. for a specific column say the name,
 *** example, just the tweet would be
 *** SELECT Tweet FROM Anotator
 ***/
SELECT * FROM Anotator;
