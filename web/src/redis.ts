import redis, { ClientOpts } from "redis";

export const redisConfig: ClientOpts = {
  host: process.env.REDIS_HOST || "localhost",
  password: process.env.REDIS_PASSWORD || "",
  port: Number.parseInt(process.env.REDIS_PORT) || 6379,
};

export const getRedisClient = () => redis.createClient(redisConfig);
