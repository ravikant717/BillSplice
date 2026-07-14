import api from "@/lib/axios";

export async function settle(
  groupId: string,
  toUserId: string,
  amount: number,
) {
  await api.post("/settlements", {
    group_id: groupId,
    to_user_id: toUserId,
    amount,
  });
}
export async function getSettlements(groupId: string) {
  const response = await api.get(`/expenses/groups/${groupId}/settlements`);

  return response.data;
}
