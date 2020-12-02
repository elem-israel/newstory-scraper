import { Request, Response } from "express";
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: [`${process.env.KAFKA_HOST}:${process.env.KAFKA_PORT}`]
})

export async function postQueue(req: Request, res: Response) {
  const { queue } = req.params;
  const { message="" } = req.body;
  const producer = kafka.producer();
  const kafkaResponse = await producer.send({topic: queue, messages: [message]})
  res.send(kafkaResponse);
}

export function getTaskState(req: Request, res: Response) {}
