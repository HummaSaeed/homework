import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Grid,
  Paper,
  TextField,
  MenuItem,
  InputAdornment,
} from '@mui/material'
import SearchIcon from '@mui/icons-material/Search'
import AddIcon from '@mui/icons-material/Add'
import { homeworkAPI, subjectAPI } from '../services/api'

function HomeworkListPage({ user }) {
  const navigate = useNavigate()
  const [homework, setHomework] = useState([])
  const [subjects, setSubjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [filterSubject, setFilterSubject] = useState('all')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    setError('')
    try {
      // Load homework
      const homeworkResponse = await homeworkAPI.listHomework()
      setHomework(homeworkResponse.data.results || homeworkResponse.data)

      // Load subjects
      const subjectsResponse = await subjectAPI.listSubjects()
      setSubjects(subjectsResponse.data.results || subjectsResponse.data)
    } catch (err) {
      setError('Failed to load homework. Please try again.')
      console.error('Error loading homework:', err)
    } finally {
      setLoading(false)
    }
  }

  const filteredHomework = homework.filter((item) => {
    const matchSearch =
      item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.description.toLowerCase().includes(search.toLowerCase())
    const matchStatus = filterStatus === 'all' || item.status === filterStatus
    const matchSubject = filterSubject === 'all' || item.subject?.id === parseInt(filterSubject)
    return matchSearch && matchStatus && matchSubject
  })

  const getStatusColor = (status) => {
    const colors = {
      draft: '#e0e0e0',
      assigned: '#e3f2fd',
      completed: '#e8f5e9',
      graded: '#e8f5e9',
    }
    return colors[status] || '#f5f5f5'
  }

  const getStatusTextColor = (status) => {
    const colors = {
      draft: '#666',
      assigned: '#1976d2',
      completed: '#4caf50',
      graded: '#4caf50',
    }
    return colors[status] || '#333'
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 700 }}>
          Homework Assignments
        </Typography>
        {user?.role === 'teacher' && (
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => navigate('/homework/create')}
          >
            Create Homework
          </Button>
        )}
      </Box>

      {error && (
        <Paper sx={{ p: 2, mb: 3, backgroundColor: '#ffebee', borderLeft: '4px solid #f44336' }}>
          <Typography sx={{ color: '#c62828' }}>{error}</Typography>
        </Paper>
      )}

      {/* Filters */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            placeholder="Search homework..."
            variant="outlined"
            size="small"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon sx={{ color: '#999' }} />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            select
            label="Status"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            size="small"
            variant="outlined"
          >
            <MenuItem value="all">All Status</MenuItem>
            <MenuItem value="draft">Draft</MenuItem>
            <MenuItem value="assigned">Assigned</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="graded">Graded</MenuItem>
          </TextField>
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            select
            label="Subject"
            value={filterSubject}
            onChange={(e) => setFilterSubject(e.target.value)}
            size="small"
            variant="outlined"
          >
            <MenuItem value="all">All Subjects</MenuItem>
            {subjects.map((subject) => (
              <MenuItem key={subject.id} value={subject.id}>
                {subject.name}
              </MenuItem>
            ))}
          </TextField>
        </Grid>
      </Grid>

      {/* Homework List */}
      {filteredHomework.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography color="textSecondary" sx={{ mb: 2 }}>
            No homework assignments found
          </Typography>
          <Typography variant="caption" color="textSecondary">
            {search || filterStatus !== 'all' || filterSubject !== 'all'
              ? 'Try adjusting your filters'
              : 'No assignments yet'}
          </Typography>
        </Paper>
      ) : (
        <Grid container spacing={2}>
          {filteredHomework.map((item) => (
            <Grid item xs={12} key={item.id}>
              <Card
                sx={{
                  cursor: 'pointer',
                  '&:hover': { boxShadow: 4 },
                  transition: 'box-shadow 0.3s',
                  borderLeft: `4px solid ${getStatusTextColor(item.status)}`,
                }}
                onClick={() => navigate(`/homework/${item.id}`)}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                        {item.title}
                      </Typography>
                      <Typography color="textSecondary" sx={{ fontSize: '0.875rem', mb: 1.5 }}>
                        {item.description?.substring(0, 150)}
                        {item.description?.length > 150 ? '...' : ''}
                      </Typography>

                      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                        {item.subject && (
                          <Typography
                            variant="caption"
                            sx={{
                              backgroundColor: '#e3f2fd',
                              color: '#1976d2',
                              padding: '4px 8px',
                              borderRadius: 1,
                            }}
                          >
                            📚 {item.subject.name}
                          </Typography>
                        )}
                        {item.due_date && (
                          <Typography
                            variant="caption"
                            sx={{
                              backgroundColor: '#fff3e0',
                              color: '#ff9800',
                              padding: '4px 8px',
                              borderRadius: 1,
                            }}
                          >
                            📅 Due: {new Date(item.due_date).toLocaleDateString()}
                          </Typography>
                        )}
                        <Typography
                          variant="caption"
                          sx={{
                            backgroundColor: getStatusColor(item.status),
                            color: getStatusTextColor(item.status),
                            padding: '4px 8px',
                            borderRadius: 1,
                            textTransform: 'capitalize',
                            fontWeight: 500,
                          }}
                        >
                          {item.status}
                        </Typography>
                        {item.points && (
                          <Typography
                            variant="caption"
                            sx={{
                              backgroundColor: '#e8f5e9',
                              color: '#4caf50',
                              padding: '4px 8px',
                              borderRadius: 1,
                            }}
                          >
                            ⭐ {item.points} pts
                          </Typography>
                        )}
                      </Box>
                    </Box>
                    <Button
                      variant="contained"
                      color="primary"
                      size="small"
                      onClick={(e) => {
                        e.stopPropagation()
                        navigate(`/homework/${item.id}`)
                      }}
                      sx={{ ml: 2 }}
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
  )
}

export default HomeworkListPage
