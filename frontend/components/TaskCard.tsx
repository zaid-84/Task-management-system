"use client";

import { createClient } from "@/lib/supabase/client";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type Task = {
  id: string;
  title: string;
  description?: string;
  status: string;
  due_date?: string | null;
  created_at?: string;
  assigned_to?: string;
};

export default function TaskCard({
  task,
  onTaskUpdated,
}: {
  task: Task;
  onTaskUpdated: () => void;
}) {
  const supabase = createClient();

  const handleComplete = async () => {
    try {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) {
        window.location.href = "/";
        return;
      }

      const response = await fetch(
        `${API_URL}/api/tasks/${task.id}/complete`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Failed to complete task"
        );
      }

      onTaskUpdated();
    } catch (error) {
      console.error(error);
      alert(
        error instanceof Error
          ? error.message
          : "Failed to complete task"
      );
    }
  };

  const isCompleted = task.status === "completed";

  const isOverdue =
    !isCompleted &&
    task.due_date &&
    new Date(task.due_date).getTime() < Date.now();

  const formattedDueDate = task.due_date
    ? new Date(task.due_date).toLocaleString([], {
        dateStyle: "medium",
        timeStyle: "short",
      })
    : null;

  return (
    <article
      className={`task-card ${
        isCompleted ? "task-completed" : ""
      } ${isOverdue ? "task-overdue" : ""}`}
    >
      <div className="task-card-top">
        <span
          className={`task-status ${
            isCompleted
              ? "status-completed"
              : "status-pending"
          }`}
        >
          <span className="status-dot"></span>

          {isCompleted ? "Completed" : "Pending"}
        </span>

        {isOverdue && (
          <span className="overdue-badge">
            Overdue
          </span>
        )}
      </div>

      <h3 className="task-title">
        {task.title}
      </h3>

      {task.description && (
        <p className="task-description">
          {task.description}
        </p>
      )}

      <div className="task-meta">
        <div className="task-meta-item">
          <span className="meta-label">
            Due date
          </span>

          <span
            className={
              isOverdue
                ? "meta-value overdue-text"
                : "meta-value"
            }
          >
            {formattedDueDate || "No deadline"}
          </span>
        </div>
      </div>

      {!isCompleted && (
        <button
          className="complete-task-button"
          onClick={handleComplete}
        >
          Mark as completed
        </button>
      )}

      {isCompleted && (
        <div className="completed-message">
          ✓ Task completed
        </div>
      )}
    </article>
  );
}