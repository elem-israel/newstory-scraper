import express from "express";
import { getUser } from "../cotrollers/auth";
import { keycloak } from "../keycloak";

const router = express.Router();

router.get("/user", keycloak.protect("user"), getUser);

export default router;
