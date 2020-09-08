import express, { Router, Request, Response } from 'express';
const router: Router = express.Router();

router.get('/', (req: Request, res: Response) => {
    res.send({ data: 'Home worked' });
});

router.get('/test', (req: Request, res: Response) => {
    res.send({ data: 'Home/test worked' });
});

export default router;
