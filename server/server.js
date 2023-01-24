const express = require("express");
const cors = require("cors");
// const cookieParser = require('cookie-parser');

require("dotenv").config();
const { EPORT } = process.env;

const app = express();
const PORT = EPORT || 3000;

app.use(
  cors({
    origin: `http://localhost:3000`,
    credentials: true,
  })
);

app.use(express.json());

const companyRouter = require("./routes/company");
app.use("/company", companyRouter);

app.listen(PORT, () => {
  console.log(`App is now listening for request on http://localhost:${PORT}`);
});
