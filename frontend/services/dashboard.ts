import api from "@/lib/axios";

export async function getOverallBalance() {
  const res = await api.get("/expenses/overall-balance");

  return res.data.balance;
}
