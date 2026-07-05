/* ---------- Layout helpers ---------- */
.login-bg {
  background: linear-gradient(135deg, #4338ca 0%, #6d28d9 50%, #4f46e5 100%);
}

.sidebar {
  transition: width 0.25s ease;
  width: 16rem;
}
.sidebar.collapsed {
  width: 4.5rem;
}
.sidebar.collapsed .sidebar-text {
  display: none;
}
.sidebar.collapsed .nav-link {
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.9rem;
  border-radius: 0.65rem;
  color: #cbd5e1;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease;
}
.nav-link:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}
.nav-active {
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  color: #fff !important;
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.4);
}
.nav-icon {
  font-size: 1.1rem;
  width: 1.5rem;
  text-align: center;
  flex-shrink: 0;
}

/* ---------- Form controls ---------- */
.label {
  display: block;
  font-size: 0.8rem;
  font-weight: 500;
  color: #475569;
  margin-bottom: 0.3rem;
}
.input {
  width: 100%;
  padding: 0.6rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.6rem;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.input:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.25);
}

/* ---------- Buttons ---------- */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1.1rem;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  color: #fff;
  font-weight: 600;
  font-size: 0.875rem;
  border-radius: 0.65rem;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.35);
  transition: transform 0.1s ease, box-shadow 0.15s ease;
  border: none;
  cursor: pointer;
}
.btn-primary:hover {
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.45);
  transform: translateY(-1px);
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1.1rem;
  background: #fff;
  color: #334155;
  font-weight: 600;
  font-size: 0.875rem;
  border-radius: 0.65rem;
  border: 1px solid #cbd5e1;
  transition: background 0.15s ease;
  cursor: pointer;
}
.btn-secondary:hover {
  background: #f1f5f9;
}

/* ---------- Search view toggle ---------- */
.view-toggle-btn {
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
  border-radius: 0.45rem;
  color: #64748b;
  font-weight: 500;
}
.view-toggle-btn.active-view {
  background: #eef2ff;
  color: #4f46e5;
}

/* ---------- Profile card ---------- */
.profile-card {
  background: #fff;
  border: 1px solid #f1f5f9;
  border-radius: 1rem;
  padding: 1.1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: box-shadow 0.15s ease, transform 0.15s ease;
}
.profile-card:hover {
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}
