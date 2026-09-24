import { createClient } from "@/lib/supabase/client";

const API_URL = "http://127.0.0.1:5000";

export async function syncUser() {
  const supabase = createClient();

  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    throw new Error("No authenticated session");
  }

  const response = await fetch(`${API_URL}/api/users/sync`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${session.access_token}`,
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || "Failed to sync user");
  }

  return data;
}