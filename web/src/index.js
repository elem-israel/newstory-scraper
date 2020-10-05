const { AsyncResult } = require("celery-node/dist/app/result");
const express = require("express");
const app = express();
const celery = require("celery-node");
const { v4 } = require("uuid");

const client = celery.createClient(
  process.env.CELERY_BROKER_URL,
  process.env.CELERY_RESULT_BACKEND
);

client.conf.TASK_PROTOCOL = 1;

app.get("/", function (req, res) {
  res.send("Hello World");
});

app.get("/echo/:text", function (req, res) {
  const id = v4();
  const { text } = req.params;
  client.sendTask("tasks.echo", [text], null, id);
  res.send("sent");
});

app.get("/scrape/:user", function (req, res) {
  const id = v4();
  const { user } = req.params;
  client.sendTask("tasks.profile", [user], {}, id);
  res.send(`<a href="/status/${id}">check status</a>`);
});

app.get("/status/:id", function (req, res) {
  const { id } = req.params;
  new AsyncResult(id, client.backend)
    .get(1000)
    .then((result) => res.send(result))
    .catch((err) => {
      err.message.includes("TIMEOUT") ? res.send("pending") : res.send(err);
    });
});

app.listen(3000, () => console.log("service started"));
