import api from "@/lib/axios";
import { Group } from "@/types/group";
import { PaginatedResponse } from "@/types/pagination";

export async function getGroups(page = 1, pageSize = 5): Promise<PaginatedResponse<Group>> {
  const response = await api.get<PaginatedResponse<Group> | Group[]>("/groups", {
    params: { page, page_size: pageSize },
  });
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

export async function createGroup(name: string) {
  const response = await api.post("/groups", {
    name,
  });

  return response.data;
}

export async function joinGroup(inviteCode: string) {
  const response = await api.post("/groups/join", {
    invite_code: inviteCode,
  });

  return response.data;
}

export async function getGroupDetails(groupId: string) {
  const response = await api.get(`/groups/${groupId}`);

  return response.data;
}
