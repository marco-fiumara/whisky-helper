import express, { Router } from 'express';
import index from '../routes/index.routes';
import home from '../routes/home.routes.';

const router: Router = express.Router();

router.use('/', index);
router.use('/home', home);

export default router;
