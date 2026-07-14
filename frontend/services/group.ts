import api from "@/lib/axios";

export async function getGroups() {
  const response = await api.get("/groups");
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
