import api from "@/lib/axios";
import { Expense } from "@/types/expense";
import { PaginatedResponse } from "@/types/pagination";

export async function getExpenses(
  groupId: string,
  page = 1,
  pageSize = 5,
): Promise<PaginatedResponse<Expense>> {
  const response = await api.get<PaginatedResponse<Expense> | Expense[]>(
    `/expenses/groups/${groupId}`,
    { params: { page, page_size: pageSize } },
  );
  const data = response.data;
  if (Array.isArray(data)) {
    return {
      items: data,
      total: data.length,
      page: 1,
      page_size: data.length,
      pages: 1,
    };
  }
  return {
    items: data?.items ?? [],
    total: data?.total ?? (data?.items ? data.items.length : 0),
    page: data?.page ?? page,
    page_size: data?.page_size ?? pageSize,
    pages: data?.pages ?? 1,
  };
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
