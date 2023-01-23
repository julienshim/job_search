const router = require('express').Router();
const paginatedResults = require('../middlewares/paginatedResults');

const pool = require('../config/keys');

router.get('/', paginatedResults('companies'), async (req, res) => {
    res.json(res.paginatedResults);
  });

module.exports = router;