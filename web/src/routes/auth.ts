import express from "express";
import { getUser } from "../cotrollers/auth";

const router = express.Router();

router.get("/user", getUser);

export default router;
