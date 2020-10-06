import express from "express";
import { postQueue, getTaskState, retryTask } from "../cotrollers/queue";

const router = express.Router();

router.post("/:queue", postQueue);
router.get("/:queue/:id", getTaskState);
router.post("/retry/:id", retryTask);

export default router;
