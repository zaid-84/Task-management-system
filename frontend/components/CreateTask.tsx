"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type User = {
  id: string;
  name?: string;
  email: string;
};

export default function CreateTask({
  onTaskCreated,
}: {
  onTaskCreated: () => void;
}) {
  const [users, setUsers] = useState<User[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [assignedTo, setAssignedTo] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [error, setError] = useState("");

  const supabase = createClient();

  useEffect(() => {
    loadUsers();
  }, []);

  const getAccessToken = async () => {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    return session?.access_token;
  };

  const loadUsers = async () => {
    try {
      setLoadingUsers(true);

      const token = await getAccessToken();

      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await fetch(`${API_URL}/api/users/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Failed to load users");
      }

      setUsers(data.users || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load users");
    } finally {
      setLoadingUsers(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    setError("");

    if (!title.trim()) {
      setError("Please enter a task title.");
      return;
    }

    if (!assignedTo) {
      setError("Please select a user.");
      return;
    }

    try {
      setLoading(true);

      const token = await getAccessToken();

      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await fetch(`${API_URL}/api/tasks/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
          assigned_to: assignedTo,
          due_date: dueDate
            ? new Date(dueDate).toISOString()
            : null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Failed to create task");
      }

      setTitle("");
      setDescription("");
      setAssignedTo("");
      setDueDate("");

      onTaskCreated();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-task-card">
      <div className="create-task-header">
        <div>
          <p className="create-task-eyebrow">
            NEW TASK
          </p>

          <h2>Create a task</h2>

          <p>
            Assign work and set a deadline.
          </p>
        </div>

        <div className="create-task-icon">
          +
        </div>
      </div>

      <form
        onSubmit={handleCreateTask}
        className="create-task-form"
      >
        <div className="form-group">
          <label htmlFor="task-title">
            Task title
          </label>

          <input
            id="task-title"
            type="text"
            placeholder="e.g. Complete project documentation"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="task-description">
            Description
          </label>

          <textarea
            id="task-description"
            placeholder="Add some details about this task..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="assigned-user">
              Assign to
            </label>

            <select
              id="assigned-user"
              value={assignedTo}
              onChange={(e) =>
                setAssignedTo(e.target.value)
              }
              disabled={loadingUsers}
            >
              <option value="">
                {loadingUsers
                  ? "Loading users..."
                  : "Select a user"}
              </option>

              {users.map((user) => (
                <option
                  key={user.id}
                  value={user.id}
                >
                  {user.name
                    ? `${user.name} (${user.email})`
                    : user.email}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="due-date">
              Due date
            </label>

            <input
              id="due-date"
              type="datetime-local"
              value={dueDate}
              onChange={(e) =>
                setDueDate(e.target.value)
              }
            />
          </div>
        </div>

        {error && (
          <div className="form-error">
            {error}
          </div>
        )}

        <button
          type="submit"
          className="create-task-button"
          disabled={loading}
        >
          {loading ? "Creating task..." : "Create task"}
        </button>
      </form>
    </div>
  );
}