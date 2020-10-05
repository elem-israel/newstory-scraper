const express = require('express')
const app = express()
const celery = require('celery-node');

const client = celery.createClient(
  process.env.CELERY_BROKER_URL,
  process.env.CELERY_RESULT_BACKEND
);

client.conf.TASK_PROTOCOL = 1;

app.get('/', function (req, res) {
  res.send('Hello World')
})

app.get("/add/:a/:b", function (req, res){
	const {a,b} = req.params;
	client.sendTask("tasks.add", [a,b])
	res.send("sent");
})

app.get("/hello", function (req, res){
	client.sendTask("tasks.hello")
	res.send("sent");
})

app.listen(3000)