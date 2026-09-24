"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import CreateTask from "@/components/CreateTask";
import TaskCard from "@/components/TaskCard";
import Navbar from "@/components/Navbar";

const API_URL = "http://127.0.0.1:5000";

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const supabase = createClient();

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) {
        window.location.href = "/";
        return;
      }

      setUser(session.user);

      const response = await fetch(`${API_URL}/api/tasks/`, {
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Failed to load tasks");
      }

      setTasks(data.tasks || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <main className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading your dashboard...</p>
      </main>
    );
  }

  const pendingTasks = tasks.filter(
    (task) => task.status === "pending"
  ).length;

  const completedTasks = tasks.filter(
    (task) => task.status === "completed"
  ).length;

  return (
    <main className="dashboard-page">
      <Navbar />

      <section className="dashboard-container">

        {/* Welcome */}
        <div className="dashboard-header">
          <div>
            <p className="dashboard-eyebrow">
              TASK MANAGEMENT
            </p>

            <h1>
              Welcome back,{" "}
              <span>
                {user?.user_metadata?.full_name ||
                  user?.email?.split("@")[0]}
              </span>
            </h1>

            <p className="dashboard-description">
              Manage your tasks and stay on top of your work.
            </p>
          </div>
        </div>

        {/* Statistics */}
        <div className="stats-grid">

          <div className="stat-card">
            <div className="stat-icon">✓</div>

            <div>
              <p>Total Tasks</p>
              <h2>{tasks.length}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon pending-icon">○</div>

            <div>
              <p>Pending</p>
              <h2>{pendingTasks}</h2>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon completed-icon">✓</div>

            <div>
              <p>Completed</p>
              <h2>{completedTasks}</h2>
            </div>
          </div>

        </div>

        {/* Create Task */}
        <section className="dashboard-section">
          <CreateTask onTaskCreated={loadDashboard} />
        </section>

        {/* Tasks */}
        <section className="dashboard-section">

          <div className="section-header">
            <div>
              <h2>My Tasks</h2>
              <p>
                Tasks assigned to you or created by you.
              </p>
            </div>

            <span className="task-count">
              {tasks.length} tasks
            </span>
          </div>

          {tasks.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">✓</div>

              <h3>No tasks yet</h3>

              <p>
                Create your first task to get started.
              </p>
            </div>
          ) : (
            <div className="tasks-grid">
              {tasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onTaskUpdated={loadDashboard}
                />
              ))}
            </div>
          )}

        </section>

      </section>
    </main>
  );
}