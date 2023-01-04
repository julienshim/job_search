const router = require('express').Router();

const pool = require('../config/keys');

router.get('/', async (req, res) => {
    try {
        const allCompanies = await pool.query(
            'SELECT * FROM company ORDER BY company_name;'
        )
        res.send(allCompanies)
    } catch (err) {
        res.sendStatus(500)
    }
})

module.exports = router;