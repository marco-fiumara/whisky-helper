import express, { Application, Request, Response, NextFunction } from 'express';
import swaggerJsDoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
import swaggerOptions from './src/config/swagger';
import * as dotenv from 'dotenv';

// Read from .env file
dotenv.config();

const swaggerDocs = swaggerJsDoc(swaggerOptions);

const app: Application = express();
const port = Number.parseInt(process.env.PORT || '5000');

// Api docs
app.use('/api', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

/**
 *
 */
app.use('/', (req: Request, res: Response, next: NextFunction) => {
    res.status(200).send({ data: 'She works mate!' });
});

// Start server
app.listen(port, () => console.log(`Server is listening on port ${port}!`));
