import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Paper,
} from '@mui/material'
import AssignmentIcon from '@mui/icons-material/Assignment'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import PendingActionsIcon from '@mui/icons-material/PendingActions'
import { homeworkAPI } from '../services/api'

function DashboardPage({ user }) {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [recentHomework, setRecentHomework] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    setLoading(true)
    setError('')
    try {
      // Fetch recent homework
      const response = await homeworkAPI.listHomework({ limit: 5 })
      setRecentHomework(response.data.results || response.data)

      // Calculate stats
      const totalHomework = response.data.count || response.data.length
      const completedHomework = (response.data.results || response.data).filter(
        (h) => h.status === 'completed' || h.status === 'graded'
      ).length
      const pendingHomework = totalHomework - completedHomework

      setStats({
        totalHomework,
        completedHomework,
        pendingHomework,
      })
    } catch (err) {
      console.error('Error loading dashboard:', err)
      // Set default stats if API fails
      setStats({
        totalHomework: 0,
        completedHomework: 0,
        pendingHomework: 0,
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    )
  }

  const roleWelcome = {
    admin: 'Admin Dashboard',
    teacher: 'Teacher Dashboard',
    student: 'Student Dashboard',
  }

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Welcome, {user?.full_name || 'User'}! 👋
        </Typography>
        <Typography variant="body1" sx={{ color: '#666' }}>
          {roleWelcome[user?.role] || 'Dashboard'}
        </Typography>
      </Box>

      {error && (
        <Paper sx={{ p: 2, mb: 3, backgroundColor: '#ffebee', borderLeft: '4px solid #f44336' }}>
          <Typography sx={{ color: '#c62828' }}>{error}</Typography>
        </Paper>
      )}

      {/* Stats Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#e3f2fd', border: '1px solid #bbdefb' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                    Total Homework
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700, color: '#1976d2' }}>
                    {stats?.totalHomework || 0}
                  </Typography>
                </Box>
                <AssignmentIcon sx={{ fontSize: 40, color: '#1976d2', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#e8f5e9', border: '1px solid #c8e6c9' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                    Completed
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700, color: '#4caf50' }}>
                    {stats?.completedHomework || 0}
                  </Typography>
                </Box>
                <CheckCircleIcon sx={{ fontSize: 40, color: '#4caf50', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#fff3e0', border: '1px solid #ffe0b2' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                    Pending
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700, color: '#ff9800' }}>
                    {stats?.pendingHomework || 0}
                  </Typography>
                </Box>
                <PendingActionsIcon sx={{ fontSize: 40, color: '#ff9800', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#f3e5f5', border: '1px solid #e1bee7' }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                    Success Rate
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700, color: '#9c27b0' }}>
                    {stats?.totalHomework ? Math.round((stats.completedHomework / stats.totalHomework) * 100) : 0}
                    %
                  </Typography>
                </Box>
                <AssignmentIcon sx={{ fontSize: 40, color: '#9c27b0', opacity: 0.7 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Homework */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Recent Homework
          </Typography>
          <Button variant="contained" color="primary" onClick={() => navigate('/homework')}>
            View All
          </Button>
        </Box>

        {recentHomework.length === 0 ? (
          <Paper sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="textSecondary">No homework assigned yet</Typography>
          </Paper>
        ) : (
          <Grid container spacing={2}>
            {recentHomework.map((homework) => (
              <Grid item xs={12} key={homework.id}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    '&:hover': { boxShadow: 4 },
                    transition: 'box-shadow 0.3s',
                  }}
                  onClick={() => navigate(`/homework/${homework.id}`)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                      <Box sx={{ flex: 1 }}>
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          {homework.title}
                        </Typography>
                        <Typography color="textSecondary" sx={{ fontSize: '0.875rem', mb: 1 }}>
                          {homework.description?.substring(0, 100)}...
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                          <Typography
                            variant="caption"
                            sx={{
                              backgroundColor: '#e3f2fd',
                              color: '#1976d2',
                              padding: '4px 8px',
                              borderRadius: 1,
                            }}
                          >
                            {homework.subject?.name || 'Subject'}
                          </Typography>
                          <Typography
                            variant="caption"
                            sx={{
                              backgroundColor:
                                homework.status === 'completed' || homework.status === 'graded'
                                  ? '#e8f5e9'
                                  : '#fff3e0',
                              color:
                                homework.status === 'completed' || homework.status === 'graded'
                                  ? '#4caf50'
                                  : '#ff9800',
                              padding: '4px 8px',
                              borderRadius: 1,
                              textTransform: 'capitalize',
                            }}
                          >
                            {homework.status}
                          </Typography>
                        </Box>
                      </Box>
                      <Button
                        variant="outlined"
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation()
                          navigate(`/homework/${homework.id}`)
                        }}
                      >
                        View
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Box>
  )
}

export default DashboardPage
