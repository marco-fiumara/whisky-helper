import { Options } from 'swagger-jsdoc';

const swaggerOptions: Options = {
    swaggerDefinition: {
        info: {
            title: 'Example API',
            description: 'Example API description',
            version: '1.0',
        },
        servers: [{ url: `http://localhost:${process.env.PORT || 5000}` }],
    },
    apis: ['**/*.ts'],
};

export default swaggerOptions;
