import session from "express-session";
import Keycloak from "keycloak-connect";
import { Express } from "express";

export const memoryStore = new session.MemoryStore();
export const keycloak = new Keycloak({ store: memoryStore });

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
