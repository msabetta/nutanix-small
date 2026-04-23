const router = require("express").Router();
const { vms } = require("../data/mockData");

router.get("/", (req, res) => {
  res.json(vms);
});

router.post("/", (req, res) => {
  const newVm = { id: Date.now(), ...req.body };
  vms.push(newVm);
  res.json(newVm);
});

module.exports = router;