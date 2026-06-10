import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Box,
  Divider,
} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import DashboardIcon from '@mui/icons-material/Dashboard'
import AssignmentIcon from '@mui/icons-material/Assignment'
import PersonIcon from '@mui/icons-material/Person'
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'

function Sidebar({ open, onToggle, userRole }) {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { label: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { label: 'Homework', icon: <AssignmentIcon />, path: '/homework' },
    { label: 'Profile', icon: <PersonIcon />, path: '/profile' },
    ...(userRole === 'admin'
      ? [{ label: 'Admin Panel', icon: <AdminPanelSettingsIcon />, path: '/admin' }]
      : []),
  ]

  const handleNavigation = (path) => {
    navigate(path)
  }

  return (
    <>
      <Drawer
        variant="persistent"
        anchor="left"
        open={open}
        sx={{
          width: 240,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 240,
            boxSizing: 'border-box',
            marginTop: '64px',
            backgroundColor: '#f8f9fa',
            borderRight: '1px solid #e0e0e0',
          },
        }}
      >
        <Box sx={{ p: 1 }}>
          <IconButton onClick={onToggle} sx={{ width: '100%' }}>
            <ChevronLeftIcon />
          </IconButton>
        </Box>
        <Divider />
        <List sx={{ pt: 2 }}>
          {menuItems.map((item) => (
            <ListItem
              button
              key={item.path}
              onClick={() => handleNavigation(item.path)}
              selected={location.pathname === item.path}
              sx={{
                mx: 1,
                mb: 1,
                borderRadius: 1,
                backgroundColor:
                  location.pathname === item.path ? '#e3f2fd' : 'transparent',
                color:
                  location.pathname === item.path ? '#1976d2' : '#666',
                '&:hover': {
                  backgroundColor: '#e3f2fd',
                },
              }}
            >
              <ListItemIcon
                sx={{
                  color: 'inherit',
                  minWidth: 40,
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.label}
                sx={{
                  '& .MuiListItemText-primary': {
                    fontWeight: location.pathname === item.path ? 600 : 500,
                  },
                }}
              />
            </ListItem>
          ))}
        </List>
      </Drawer>

      {!open && (
        <Box
          sx={{
            position: 'fixed',
            left: 16,
            top: 80,
            zIndex: 100,
          }}
        >
          <IconButton onClick={onToggle} sx={{ backgroundColor: '#1976d2', color: 'white' }}>
            <MenuIcon />
          </IconButton>
        </Box>
      )}
    </>
  )
}

export default Sidebar
