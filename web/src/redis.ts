import redis, { ClientOpts } from "redis";

export const redisConfig: ClientOpts = {
  host: process.env.REDIS_HOST || "localhost",
  password: process.env.REDIS_PASSOWRD || "",
  port: Number.parseInt(process.env.REDIS_PORT) || 6379,
};

export const redisClient = redis.createClient(redisConfig);

redisClient.on("error", (err: any) => {
  console.error("Redis error: ", err);
});
