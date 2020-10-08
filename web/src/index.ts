import express, { Request, Response } from "express";
import queue from "./routes/queue";
import auth from "./routes/auth";
import { installKeycloak, keycloak } from "./keycloak";
import bodyParser from "body-parser";

const port = process.env.PORT || 3000;

const app = express();

app.get("/", function (req: Request, res: Response) {
  res.send("Hello World");
});

if (
  process.env.NODE_ENV === "production" ||
  Number.parseInt(process.env.USE_AUTH)
) {
  installKeycloak(app);
  app.use(keycloak.protect());
}

app.use(bodyParser.json());
app.use(keycloak.protect("user"));
app.use("/queue", queue);
app.use("/auth", auth);
app.listen(port, () => console.log(`server listening on port ${port}`));
