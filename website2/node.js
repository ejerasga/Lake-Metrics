var http = require('http');
var fs = require('fs')
var hostname = '127.0.0.1';
var port = 3000;
 
var server = http.createServer(function(req, res) {
  console.log('request was made: '+ req.url);
  res.writeHead(200,{'Content-Type': 'text/html'});
  var myReadStraem= fs.createReadStream('c:/Users/OASFOV/Desktop/site/main.html','utf8');
  myReadStraem.pipe(res);
  });
  
 
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`)
})
