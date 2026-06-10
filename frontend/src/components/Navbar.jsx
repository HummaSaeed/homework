import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Menu,
  MenuItem,
  Avatar,
  Box,
} from '@mui/material'
import LogoutIcon from '@mui/icons-material/Logout'
import PersonIcon from '@mui/icons-material/Person'

function Navbar({ user, onLogout }) {
  const navigate = useNavigate()
  const [anchorEl, setAnchorEl] = React.useState(null)

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleProfile = () => {
    navigate('/profile')
    handleMenuClose()
  }

  const handleLogout = () => {
    onLogout()
    navigate('/login')
    handleMenuClose()
  }

  return (
    <AppBar
      position="fixed"
      sx={{
        backgroundColor: '#fff',
        color: '#333',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        zIndex: 1200,
      }}
    >
      <Toolbar>
        <Typography
          variant="h6"
          sx={{
            flexGrow: 1,
            fontWeight: 700,
            cursor: 'pointer',
            color: '#1976d2',
          }}
          onClick={() => navigate('/dashboard')}
        >
          📚 Homework Manager
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="body2" sx={{ color: '#666' }}>
            {user?.full_name || user?.username}
          </Typography>
          <Typography
            variant="caption"
            sx={{
              backgroundColor: '#e3f2fd',
              color: '#1976d2',
              padding: '4px 8px',
              borderRadius: '4px',
              textTransform: 'capitalize',
            }}
          >
            {user?.role}
          </Typography>

          <Avatar
            onClick={handleMenuOpen}
            sx={{
              cursor: 'pointer',
              backgroundColor: '#1976d2',
              width: 40,
              height: 40,
            }}
          >
            {user?.full_name?.charAt(0) || 'U'}
          </Avatar>
        </Box>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        >
          <MenuItem onClick={handleProfile}>
            <PersonIcon sx={{ mr: 1 }} />
            Profile
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <LogoutIcon sx={{ mr: 1 }} />
            Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  )
}

export default Navbar
