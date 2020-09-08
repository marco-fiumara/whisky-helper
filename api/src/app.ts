import express, { Application } from 'express';
import * as dotenv from 'dotenv';
import routes from './startup/routes';

// Read from .env file
dotenv.config();

const app: Application = express();
const port = Number.parseInt(process.env.PORT || '5000');

app.use('/', routes);

// Start server
app.listen(port, () => console.log(`Server is listening on port ${port}!`));
