import { Request, Response } from "express";
import { v4 } from "uuid";
import axios from "axios";

import * as celery from "celery-node";

const FLOWER_URL = process.env.FLOWER_URL;

const baseCeleryConf = [
  process.env.CELERY_BROKER_URL,
  process.env.CELERY_RESULT_BACKEND,
];

const queues: any = {
  upload: celery.createClient(...baseCeleryConf, "upload"),
  profile: celery.createClient(...baseCeleryConf, "profile"),
};

export function postQueue(req: Request, res: Response) {
  const id = v4();
  const { queue } = req.params;
  const { args = [], kwargs = {} } = req.body;
  const queueName = queue.replace("tasks.", "");
  queues[queueName].sendTask(queue, args, kwargs, id);
  res.send(id);
}

export function getTaskState(req: Request, res: Response) {}

export async function retryTask(req: Request, res: Response) {
  const { id } = req.params;
  console.log("getting task data");
  const data: any = await axios
    .get(`${FLOWER_URL}/api/task/info/${id}`)
    .then(({ data }: any) => data);
  const newId = v4();
  const queueName = data.name.replace("tasks.", "");
  queues[queueName].sendTask(
    data.name,
    JSON.parse(data.args.replace(/'/g, '"')),
    JSON.parse(data.kwargs.replace(/'/g, '"')),
    newId
  );
  console.log("retrying with new id");
  return res.send(newId);
}
