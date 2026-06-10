import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Card,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material'
import { authAPI } from '../services/api'

function LoginPage({ onLogin }) {
  const navigate = useNavigate()
  const [step, setStep] = useState(0) // 0 = phone, 1 = otp
  const [phoneNumber, setPhoneNumber] = useState('')
  const [otp, setOtp] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleRequestOTP = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!phoneNumber.trim()) {
        setError('Please enter your phone number')
        setLoading(false)
        return
      }

      await authAPI.requestOTP(phoneNumber)
      setMessage('OTP sent successfully! Check your phone or use test OTP.')
      setStep(1)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to send OTP. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyOTP = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (!otp.trim()) {
        setError('Please enter the OTP')
        setLoading(false)
        return
      }

      const response = await authAPI.verifyOTP(phoneNumber, otp)

      // Save tokens and user info
      onLogin(response.data.user, {
        access: response.data.access,
        refresh: response.data.refresh,
      })

      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.error || 'Invalid OTP. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleBack = () => {
    setStep(0)
    setOtp('')
    setError('')
    setMessage('')
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 2,
      }}
    >
      <Card
        sx={{
          width: '100%',
          maxWidth: 400,
          padding: 4,
          boxShadow: '0 10px 40px rgba(0,0,0,0.2)',
        }}
      >
        <Typography
          variant="h4"
          sx={{
            mb: 1,
            fontWeight: 700,
            textAlign: 'center',
            color: '#333',
          }}
        >
          📚 Homework Manager
        </Typography>
        <Typography
          variant="body2"
          sx={{
            mb: 3,
            textAlign: 'center',
            color: '#666',
          }}
        >
          Sign in to your account
        </Typography>

        <Stepper activeStep={step} sx={{ mb: 3 }}>
          <Step>
            <StepLabel>Phone</StepLabel>
          </Step>
          <Step>
            <StepLabel>OTP</StepLabel>
          </Step>
        </Stepper>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {message && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {message}
          </Alert>
        )}

        {step === 0 ? (
          <form onSubmit={handleRequestOTP}>
            <TextField
              fullWidth
              label="Phone Number"
              type="tel"
              placeholder="+92 300 1234567"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              disabled={loading}
              margin="normal"
              variant="outlined"
            />
            <Button
              fullWidth
              variant="contained"
              color="primary"
              size="large"
              sx={{ mt: 3, py: 1.5 }}
              onClick={handleRequestOTP}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Request OTP'}
            </Button>

            <Typography variant="caption" sx={{ display: 'block', mt: 2, color: '#999' }}>
              💡 Demo: Use any phone number. Default test OTP: 123456
            </Typography>
          </form>
        ) : (
          <form onSubmit={handleVerifyOTP}>
            <Typography variant="body2" sx={{ mb: 2, color: '#666' }}>
              Enter the OTP sent to:
              <strong> {phoneNumber}</strong>
            </Typography>
            <TextField
              fullWidth
              label="Enter OTP"
              type="text"
              placeholder="123456"
              value={otp}
              onChange={(e) => setOtp(e.target.value.slice(0, 6))}
              disabled={loading}
              margin="normal"
              variant="outlined"
              inputProps={{ maxLength: 6 }}
            />
            <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
              <Button
                fullWidth
                variant="outlined"
                size="large"
                onClick={handleBack}
                disabled={loading}
              >
                Back
              </Button>
              <Button
                fullWidth
                variant="contained"
                color="primary"
                size="large"
                onClick={handleVerifyOTP}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Verify OTP'}
              </Button>
            </Box>

            <Typography variant="caption" sx={{ display: 'block', mt: 2, color: '#999' }}>
              💡 Demo OTP: 123456
            </Typography>
          </form>
        )}
      </Card>
    </Box>
  )
}

export default LoginPage
