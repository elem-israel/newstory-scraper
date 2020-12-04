import express from "express";
import { postQueue, getTaskState } from "../cotrollers/queue";

const router = express.Router();

router.post("/:queue", postQueue);
router.get("/:queue/:id", getTaskState);

export default router;
