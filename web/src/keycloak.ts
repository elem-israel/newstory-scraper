import session from "express-session";
import Keycloak from "keycloak-connect";
import { Express } from "express";
import * as fs from "fs";
import { redisClient, redisConfig } from "./redis";
import RedisStore from "connect-redis";

const redisStore = RedisStore(session);
export const memoryStore = new session.MemoryStore();

redisClient.on("error", (err: any) => {
  console.error("Redis error: ", err);
});

const config = fs.existsSync("/etc/keycloak/keycloak.json")
  ? JSON.parse(fs.readFileSync("/etc/keycloak/keycloak.json").toString())
  : null;

export const keycloak = new Keycloak({ store: memoryStore }, config);

export function installKeycloak(app: Express) {
  app.use(
    session({
      secret: process.env.SESSION_SECRET,
      name: "keycloakSessions",
      resave: false,
      saveUninitialized: true,
      cookie: { secure: false }, // Note that the cookie-parser module is no longer needed
      store: new redisStore({
        ...redisConfig,
        client: redisClient,
        ttl: 86400,
      }),
    })
  );
  app.use(keycloak.middleware());
}
