import { Request, Response } from "express";

export function getUser(req: Request & { kauth: any }, res: Response) {
  console.log(res.locals);
  console.log(req);
  res.send(req.kauth.grant.access_token.content.preferred_username);
}
