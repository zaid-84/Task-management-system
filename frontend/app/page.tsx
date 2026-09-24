"use client";

import { createClient } from "@/lib/supabase/client";

export default function Home() {
  const supabase = createClient();

  const handleGoogleLogin = async () => {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
  };

  return (
    <main className="login-page">
      <div className="login-card">
        <div className="login-icon">
          ✓
        </div>

        <h1>TaskFlow</h1>

        <p className="login-subtitle">
          Manage your tasks. Stay organized. Get things done.
        </p>

        <button
          className="google-login-button"
          onClick={handleGoogleLogin}
        >
          <span className="google-icon">G</span>
          Continue with Google
        </button>

        <p className="login-footer">
          Secure authentication powered by Supabase
        </p>
      </div>
    </main>
  );
}