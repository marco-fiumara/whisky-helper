import express, { Router, Request, Response } from 'express';
const router: Router = express.Router();

router.get('/', (req: Request, res: Response) => {
    res.send({ data: 'Index worked' });
});

export default router;
