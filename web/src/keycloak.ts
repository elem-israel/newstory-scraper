import session from "express-session";
import Keycloak from "keycloak-connect";
import { Express } from "express";
import * as fs from "fs";

export const memoryStore = new session.MemoryStore();

const config = fs.existsSync("/etc/keycloak.json")
  ? JSON.parse(fs.readFileSync("/etc/keycloak.json").toString())
  : null;

export const keycloak = new Keycloak({ store: memoryStore }, config);

export function installKeycloak(app: Express) {
  app.use(
    session({
      secret: "mySecret",
      resave: false,
      saveUninitialized: true,
      store: memoryStore,
    })
  );
  app.use(keycloak.middleware());
}
