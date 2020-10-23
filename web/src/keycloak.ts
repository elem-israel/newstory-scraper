import session from "express-session";
import Keycloak, { Keycloak as KeyCloakClient } from "keycloak-connect";
import { Express } from "express";
import * as fs from "fs";
import { getRedisClient, redisConfig } from "./redis";
import RedisStoreBuilder from "connect-redis";

export let keycloak: KeyCloakClient;

export function installKeycloak(app: Express) {
  const RedisStore = RedisStoreBuilder(session);

  const redisClient = getRedisClient();
  redisClient.on("error", (err: any) => {
    console.error("Redis error: ", err);
  });

  const redisStore = new RedisStore({
    ...redisConfig,
    client: redisClient,
    ttl: 86400,
  } as any);

  const config = fs.existsSync("/etc/keycloak/keycloak.json")
    ? JSON.parse(fs.readFileSync("/etc/keycloak/keycloak.json").toString())
    : null;

  keycloak = new Keycloak({ store: redisStore }, config);

  app.use(
    session({
      secret: process.env.SESSION_SECRET,
      name: "keycloakSessions",
      resave: false,
      saveUninitialized: true,
      cookie: { secure: false }, // Note that the cookie-parser module is no longer needed
      store: redisStore,
    })
  );
  app.use(keycloak.middleware());
}

export function installDevKeycloak(app: Express) {
  const memoryStore = new session.MemoryStore();

  keycloak = new Keycloak({ store: memoryStore });

  app.use(
    session({
      secret: "topSecret",
      resave: false,
      saveUninitialized: true,
      store: memoryStore,
    })
  );
  app.use(keycloak.middleware());
}
