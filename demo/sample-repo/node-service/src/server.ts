import express from "express";
import { listProducts, productResponse } from "./products";
import { wrapResponse } from "./types";

const app = express();
const router = express.Router();

app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

router.get("/products", (_req, res) => {
  res.json(wrapResponse(listProducts()));
});

router.get("/products/:id", (req, res) => {
  const id = parseInt(req.params.id, 10);
  res.json(productResponse(id));
});

router.post("/products/search", (req, res) => {
  const query = req.body?.query ?? "";
  const results = listProducts().filter((p) =>
    p.name.toLowerCase().includes(String(query).toLowerCase())
  );
  res.json(wrapResponse(results));
});

app.use("/api", router);

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Demo Express service running on port ${PORT}`);
});

export default app;
