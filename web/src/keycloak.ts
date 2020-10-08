import session from "express-session";
import Keycloak, { Keycloak as KeyCloakClient } from "keycloak-connect";
import { Express } from "express";
import * as fs from "fs";
import { redisClient, redisConfig } from "./redis";
import RedisStoreBuilder from "connect-redis";

export let keycloak: KeyCloakClient;

export function installKeycloak(app: Express) {
  const RedisStore = RedisStoreBuilder(session);
  const memoryStore = new session.MemoryStore();

  redisClient.on("error", (err: any) => {
    console.error("Redis error: ", err);
  });

  const config = fs.existsSync("/etc/keycloak/keycloak.json")
    ? JSON.parse(fs.readFileSync("/etc/keycloak/keycloak.json").toString())
    : null;

  keycloak = new Keycloak({ store: memoryStore }, config);

  app.use(
    session({
      secret: process.env.SESSION_SECRET,
      name: "keycloakSessions",
      resave: false,
      saveUninitialized: true,
      cookie: { secure: false }, // Note that the cookie-parser module is no longer needed
      store: new RedisStore({
        ...redisConfig,
        client: redisClient,
        ttl: 86400,
      } as any),
    })
  );
  app.use(keycloak.middleware());
}
