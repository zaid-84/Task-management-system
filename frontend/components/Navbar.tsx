"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";

export default function Navbar() {
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);

    const supabase = createClient();

    await supabase.auth.signOut();

    window.location.href = "/";
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <a href="/dashboard" className="navbar-brand">
          <span className="navbar-logo">✓</span>
          <span>TaskFlow</span>
        </a>

        <div className="navbar-actions">
          <button
            className="logout-button"
            onClick={handleLogout}
            disabled={loggingOut}
          >
            {loggingOut ? "Logging out..." : "Logout"}
          </button>
        </div>
      </div>
    </nav>
  );
}