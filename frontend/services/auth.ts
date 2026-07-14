import api from "@/lib/axios";

export async function login(email: string, password: string) {
  const body = new URLSearchParams();

  body.append("username", email);
  body.append("password", password);

  const response = await api.post(
    "/auth/login",
    body,
    {
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
}

export async function register(data: {
  name: string;
  email: string;
  password: string;
}) {
  const response = await api.post(
    "/auth/register",
    data
  );

  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get("/auth/me");

  return response.data;
}

export async function logout() {
  await api.post("/auth/logout");
}