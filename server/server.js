const express = require('express');

require('dotenv').config();
const { EPORT } = process.env;

const app = express();
const PORT = EPORT || 3000;

app.use(express.json());

const companyRouter = require('./routes/company');
app.use('/company', companyRouter)


app.listen(PORT, () => {
    console.log(`App is now listening for request on http://localhost:${PORT}`);
})