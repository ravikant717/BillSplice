import api from "@/lib/axios";
import { Group } from "@/types/group";
import { PaginatedResponse } from "@/types/pagination";

export async function getGroups(page = 1, pageSize = 5) {
  const response = await api.get<PaginatedResponse<Group>>("/groups", {
    params: { page, page_size: pageSize },
  });
  return response.data;
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
