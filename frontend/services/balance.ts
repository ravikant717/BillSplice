import api from "@/lib/axios";

export async function getBalances(groupId: string) {
  const response = await api.get(`/expenses/groups/${groupId}/balances`);

  return response.data;
}
