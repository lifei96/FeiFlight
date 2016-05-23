var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'database16',
  password : 'database16',
  database : 'FeiFlight'
});

connection.connect();

connection.query('SELECT * FROM users;', function(err, rows, fields) {
  if (!err)
    console.log('The solution is: ', rows);
  else
    console.log('Error while performing Query.');
});

connection.end();
