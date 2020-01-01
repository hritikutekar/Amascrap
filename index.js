var fs = require("fs");

var express = require("express");
var app = express();

let { PythonShell } = require("python-shell");

app.listen(process.env.PORT || 3000, function() {
  console.log("server running on port " + process.env.PORT);
});

app.get("/", homePage);
app.get("/run", run);

function homePage(req, res) {
  res.statusCode = 200;
  res.setHeader("Content-Type", "text/html");
  fs.readFile("./index.html", null, function(error, data) {
    if (error) {
      res.statusCode = 404;
      res.end("File not found");
    } else {
      res.end(data);
    }
  });
}

function run(req, res) {
  // res.statusCode = 200;
  // res.setHeader("Content-Type", "text/html");

  // var options = {
  //   mode: "text",
  //   encoding: "utf8",
  //   pythonOptions: ["-u"],
  //   scriptPath: "./",
  //   args: ["https://www.amazon.in/Redmi-7A-Matte-Blue-Storage/dp/B07X3P1DR3"],
  //   pythonPath: "/usr/bin/python3"
  // };

  // var test = new PythonShell("test.py", options);
  // test.on("message", function(message) {
  //   data = message;
  //   res.write(data);
  // });

  res.statusCode = 200;
  res.setHeader("Content-Type", "text/html");

  var spawn = require("child_process").spawn;

  var process = spawn("python3", ["./test.py", req.query.url]);

  process.stdout
    .on("data", function(data) {
      res.write(data);
    })
    .on("end", () => {
      res.end();
    });
}
