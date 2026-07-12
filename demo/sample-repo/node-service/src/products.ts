import { wrapResponse } from "./types";

export interface Product {
  id: number;
  name: string;
  price: number;
}

const products: Product[] = [
  { id: 1, name: "Widget", price: 9.99 },
  { id: 2, name: "Gadget", price: 19.99 },
  { id: 3, name: "Gizmo", price: 29.99 },
];

export function getProduct(id: number): Product | undefined {
  return products.find((p) => p.id === id);
}

export function listProducts(): Product[] {
  return products;
}

export function productResponse(id: number) {
  const product = getProduct(id);
  return wrapResponse(product ?? null);
}
