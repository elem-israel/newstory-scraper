import { Request, Response } from "express";
import { BlobServiceClient } from "@azure/storage-blob";
import * as celery from "celery-node";

const blobServiceClient = BlobServiceClient.fromConnectionString(
  process.env.AZURE_STORAGE_CONNECTION_STRING as string
);
const containerClient = blobServiceClient.getContainerClient(
  process.env.CONTAINER_NAME as string
);


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

export async function getProfile(req: Request, res: Response) {
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
}
