import api from "@/lib/axios";

export async function getExpenses(groupId: string) {
  const response = await api.get(`/expenses/groups/${groupId}`);

  return response.data;
}

export async function createExpense(
  groupId: string,
  title: string,
  amount: number,
) {
  const response = await api.post("/expenses", {
    group_id: groupId,
    title,
    amount,
  });

  return response.data;
}

export async function deleteExpense(expenseId: string) {
  const response = await api.delete(`/expenses/${expenseId}`);

  return response.data;
}
