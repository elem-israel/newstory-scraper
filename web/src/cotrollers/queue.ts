import { Request, Response } from "express";
import { Kafka } from "kafkajs";

const kafka = new Kafka({
  clientId: "my-app",
  brokers: [`${process.env.KAFKA_HOST}:${process.env.KAFKA_PORT}`],
});

const producer = kafka.producer();

export async function postQueue(req: Request, res: Response) {
  await producer.connect();
  const { queue } = req.params;
  const { message: value = "" } = req.body;
  const kafkaResponse = await producer.send({
    topic: queue,
    messages: [{ value: JSON.stringify(value) }],
  });
  return res.send(kafkaResponse);
}

export function getTaskState(req: Request, res: Response) {}
