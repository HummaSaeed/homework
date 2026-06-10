import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Paper,
  Grid,
  Divider,
} from '@mui/material'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import DownloadIcon from '@mui/icons-material/Download'
import { homeworkAPI } from '../services/api'

function HomeworkDetailPage({ user }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [homework, setHomework] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadHomework()
  }, [id])

  const loadHomework = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await homeworkAPI.getHomework(id)
      setHomework(response.data)
    } catch (err) {
      setError('Failed to load homework details. Please try again.')
      console.error('Error loading homework:', err)
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

  if (!homework) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <Typography color="error">Homework not found</Typography>
        <Button onClick={() => navigate('/homework')} sx={{ mt: 2 }}>
          Back to Homework
        </Button>
      </Paper>
    )
  }

  const isOverdue = homework.due_date && new Date(homework.due_date) < new Date()
  const daysUntilDue =
    homework.due_date && Math.ceil((new Date(homework.due_date) - new Date()) / (1000 * 60 * 60 * 24))

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate('/homework')}
        sx={{ mb: 2 }}
      >
        Back to Homework
      </Button>

      {error && (
        <Paper sx={{ p: 2, mb: 3, backgroundColor: '#ffebee', borderLeft: '4px solid #f44336' }}>
          <Typography sx={{ color: '#c62828' }}>{error}</Typography>
        </Paper>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
              <Box>
                <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                  {homework.title}
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  {homework.subject && (
                    <Typography
                      variant="caption"
                      sx={{
                        backgroundColor: '#e3f2fd',
                        color: '#1976d2',
                        padding: '6px 12px',
                        borderRadius: 1,
                        fontWeight: 500,
                      }}
                    >
                      📚 {homework.subject.name}
                    </Typography>
                  )}
                  <Typography
                    variant="caption"
                    sx={{
                      backgroundColor: '#e8f5e9',
                      color: '#4caf50',
                      padding: '6px 12px',
                      borderRadius: 1,
                      fontWeight: 500,
                      textTransform: 'capitalize',
                    }}
                  >
                    {homework.status}
                  </Typography>
                  {homework.points && (
                    <Typography
                      variant="caption"
                      sx={{
                        backgroundColor: '#fff3e0',
                        color: '#ff9800',
                        padding: '6px 12px',
                        borderRadius: 1,
                        fontWeight: 500,
                      }}
                    >
                      ⭐ {homework.points} Points
                    </Typography>
                  )}
                </Box>
              </Box>
              {user?.role === 'student' && homework.status === 'assigned' && (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => navigate(`/homework/${homework.id}/submit`)}
                >
                  Submit Homework
                </Button>
              )}
            </Box>
          </Box>

          <Divider sx={{ my: 2 }} />

          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  Description
                </Typography>
                <Typography
                  variant="body2"
                  sx={{
                    color: '#333',
                    lineHeight: 1.8,
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}
                >
                  {homework.description}
                </Typography>
              </Box>

              {homework.attachments && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                    Attachments
                  </Typography>
                  <Paper sx={{ p: 2, backgroundColor: '#f5f5f5' }}>
                    <Button
                      startIcon={<DownloadIcon />}
                      href={homework.attachments}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Download File
                    </Button>
                  </Paper>
                </Box>
              )}
            </Grid>

            <Grid item xs={12} md={4}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                    Details
                  </Typography>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="caption" sx={{ color: '#999' }}>
                      Assigned By
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {homework.assigned_by?.full_name || homework.assigned_by?.username}
                    </Typography>
                  </Box>

                  {homework.due_date && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="caption" sx={{ color: '#999' }}>
                        Due Date
                      </Typography>
                      <Typography
                        variant="body2"
                        sx={{
                          fontWeight: 500,
                          color: isOverdue ? '#f44336' : '#333',
                        }}
                      >
                        {new Date(homework.due_date).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                        })}
                      </Typography>
                      {!isOverdue && daysUntilDue !== null && (
                        <Typography variant="caption" sx={{ color: '#666' }}>
                          {daysUntilDue} days remaining
                        </Typography>
                      )}
                      {isOverdue && (
                        <Typography variant="caption" sx={{ color: '#f44336', fontWeight: 600 }}>
                          ⚠️ Overdue
                        </Typography>
                      )}
                    </Box>
                  )}

                  {homework.status === 'graded' && homework.score !== null && (
                    <Box sx={{ mb: 2, p: 2, backgroundColor: '#e8f5e9', borderRadius: 1 }}>
                      <Typography variant="caption" sx={{ color: '#999' }}>
                        Your Score
                      </Typography>
                      <Typography variant="h5" sx={{ fontWeight: 700, color: '#4caf50' }}>
                        {homework.score}/{homework.points || 100}
                      </Typography>
                      {homework.feedback && (
                        <Box sx={{ mt: 1 }}>
                          <Typography variant="caption" sx={{ fontWeight: 600 }}>
                            Feedback:
                          </Typography>
                          <Typography variant="caption" sx={{ display: 'block', mt: 0.5 }}>
                            {homework.feedback}
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  )}

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="caption" sx={{ color: '#999' }}>
                      Created
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {new Date(homework.created_at).toLocaleDateString()}
                    </Typography>
                  </Box>

                  {homework.status === 'assigned' && user?.role === 'student' && (
                    <Button
                      fullWidth
                      variant="contained"
                      color="primary"
                      onClick={() => navigate(`/homework/${homework.id}/submit`)}
                      sx={{ mt: 2 }}
                    >
                      Submit Now
                    </Button>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  )
}

export default HomeworkDetailPage
