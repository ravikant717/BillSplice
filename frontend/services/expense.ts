import api from "@/lib/axios";
import { Expense } from "@/types/expense";
import { PaginatedResponse } from "@/types/pagination";

export async function getExpenses(groupId: string, page = 1, pageSize = 5) {
  const response = await api.get<PaginatedResponse<Expense>>(
    `/expenses/groups/${groupId}`,
    { params: { page, page_size: pageSize } },
  );

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
