const router = require("express").Router();
const { cluster } = require("../data/mockData");

router.get("/", (req, res) => {
  res.json(cluster);
});

module.exports = router;