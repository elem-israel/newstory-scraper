import { BlobServiceClient } from "@azure/storage-blob";
import { AsyncResult } from "celery-node/dist/app/result";
import express, { Request, Response } from "express";
import * as celery from "celery-node";
import { v4 } from "uuid";
import queue from "./routes/queue";
import auth from "./routes/auth";
import { installKeycloak, keycloak } from "./keycloak";
import bodyParser from "body-parser";

const port = process.env.PORT || 3000;

const app = express();
const blobServiceClient = BlobServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING as string
);
const containerClient = blobServiceClient.getContainerClient(
  process.env.CONTAINER_NAME as string
);
const client = celery.createClient(
  process.env.CELERY_BROKER_URL,
  process.env.CELERY_RESULT_BACKEND
);

app.get("/", function (req: Request, res: Response) {
  res.send("Hello World");
});

app.get("/echo/:text", function (req: Request, res: Response) {
  const id = v4();
  const { text } = req.params;
  client.sendTask("tasks.echo", [text], {}, id);
  res.send("sent");
});

app.get("/scrape/:user", function (req: Request, res: Response) {
  const id = v4();
  const { user } = req.params;
  client.sendTask("tasks.profile", [user], {}, id);
  res.send(id);
});

app.get("/status/:id", function (req: Request, res: Response) {
  const { id } = req.params;
  new AsyncResult(id, client.backend)
    .get(1000)
    .then((result) => res.send(result))
    .catch((err) => {
      err.message.includes("TIMEOUT") ? res.send("pending") : res.send(err);
    });
});

async function streamToString(
  readableStream: NodeJS.ReadableStream
): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: any = [];
    readableStream.on("data", (data) => {
      chunks.push(data.toString());
    });
    readableStream.on("end", () => {
      resolve(chunks.join(""));
    });
    readableStream.on("error", reject);
  });
}

app.get("/profile/:username", async function (req: Request, res: Response) {
  const { username } = req.params;
  const path = `${username}/profile.json`;
  console.log("getting ${path}");
  const blockBlobClient = containerClient.getBlockBlobClient(path);
  console.log("downloading ${path}");
  const downloadBlockBlobResponse = await blockBlobClient
    .download(0)
    .then((res) => streamToString(res.readableStreamBody));
  console.log(downloadBlockBlobResponse);
  return res.send(JSON.parse(downloadBlockBlobResponse));
});

if (
  process.env.NODE_ENV === "production" ||
  Number.parseInt(process.env.USE_AUTH)
) {
  installKeycloak(app);
  app.use(keycloak.protect());
}

app.use(bodyParser.json());
app.use("/queue", queue);
app.use("/auth", auth);
app.listen(port, () => console.log(`server listening on port ${port}`));
