import { describe, expect, it } from "vitest";
import { methodColor, riskColor } from "@/lib/utils";

describe("utils", () => {
  it("returns correct risk colors", () => {
    expect(riskColor(80)).toContain("red");
    expect(riskColor(50)).toContain("amber");
    expect(riskColor(10)).toContain("emerald");
  });

  it("returns method badge classes", () => {
    expect(methodColor("GET")).toContain("emerald");
    expect(methodColor("POST")).toContain("blue");
    expect(methodColor("DELETE")).toContain("red");
  });
});
