import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:3001/api",
});

export const getVMs = () => API.get("/vms");
export const getCluster = () => API.get("/cluster");