import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material'
import Container from '@mui/material/Container'

// Pages
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import HomeworkListPage from './pages/HomeworkListPage'
import HomeworkDetailPage from './pages/HomeworkDetailPage'
import SubmitHomeworkPage from './pages/SubmitHomeworkPage'
import ProfilePage from './pages/ProfilePage'
import AdminDashboard from './pages/AdminDashboard'

// Components
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'

// Styles
import './App.css'

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    success: {
      main: '#4caf50',
    },
    error: {
      main: '#f44336',
    },
    warning: {
      main: '#ff9800',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
    h1: { fontSize: '2.5rem', fontWeight: 700 },
    h2: { fontSize: '2rem', fontWeight: 700 },
    h3: { fontSize: '1.75rem', fontWeight: 600 },
    h4: { fontSize: '1.5rem', fontWeight: 600 },
    h5: { fontSize: '1.25rem', fontWeight: 600 },
    h6: { fontSize: '1rem', fontWeight: 600 },
  },
})

// Protected Route Component
function ProtectedRoute({ children, isAuthenticated }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return children
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    // Check if user is logged in
    const storedUser = localStorage.getItem('user')
    const accessToken = localStorage.getItem('access_token')

    if (storedUser && accessToken) {
      setUser(JSON.parse(storedUser))
      setIsAuthenticated(true)
    }
  }, [])

  const handleLogin = (userData, tokens) => {
    setUser(userData)
    setIsAuthenticated(true)
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
  }

  const handleLogout = () => {
    setUser(null)
    setIsAuthenticated(false)
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="app">
          {isAuthenticated && <Navbar user={user} onLogout={handleLogout} />}
          <div className="app-content">
            {isAuthenticated && (
              <Sidebar
                open={sidebarOpen}
                onToggle={() => setSidebarOpen(!sidebarOpen)}
                userRole={user?.role}
              />
            )}
            <Container
              maxWidth="lg"
              sx={{
                flex: 1,
                py: 3,
                ml: isAuthenticated ? (sidebarOpen ? '240px' : '0px') : '0px',
                transition: 'margin-left 0.3s ease',
              }}
            >
              <Routes>
                {/* Public Routes */}
                <Route
                  path="/login"
                  element={
                    isAuthenticated ? (
                      <Navigate to="/dashboard" replace />
                    ) : (
                      <LoginPage onLogin={handleLogin} />
                    )
                  }
                />

                {/* Protected Routes */}
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <DashboardPage user={user} />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/homework"
                  element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <HomeworkListPage user={user} />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/homework/:id"
                  element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <HomeworkDetailPage user={user} />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/homework/:id/submit"
                  element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <SubmitHomeworkPage user={user} />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      <ProfilePage user={user} setUser={setUser} />
                    </ProtectedRoute>
                  }
                />

                <Route
                  path="/admin"
                  element={
                    <ProtectedRoute isAuthenticated={isAuthenticated}>
                      {user?.role === 'admin' ? (
                        <AdminDashboard user={user} />
                      ) : (
                        <Navigate to="/dashboard" replace />
                      )}
                    </ProtectedRoute>
                  }
                />

                {/* Default Route */}
                <Route
                  path="/"
                  element={<Navigate to={isAuthenticated ? '/dashboard' : '/login'} replace />}
                />
              </Routes>
            </Container>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App
