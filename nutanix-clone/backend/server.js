const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

const vmRoutes = require("./routes/vm");
const clusterRoutes = require("./routes/cluster");

app.use("/api/vms", vmRoutes);
app.use("/api/cluster", clusterRoutes);

app.listen(3001, () => {
  console.log("Backend running on http://localhost:3001");
});