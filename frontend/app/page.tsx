"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { AuraLogo } from "@/components/aura-logo"
import { ThemeToggle } from "@/components/theme-toggle"
import { useAuth } from "@/contexts/AuthContext"

export default function LoginPage() {
  const [isSignup, setIsSignup] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [fullName, setFullName] = useState("")
  const [organization, setOrganization] = useState("")
  const [role, setRole] = useState<"clinic_admin" | "gcf_coordinator">("clinic_admin")
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const { login, register, isLoading } = useAuth()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    try {
      await login({ email, password })
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invalid email or password")
    }
  }

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setSuccess("")

    try {
      await register({ 
        email, 
        password, 
        full_name: fullName, 
        organization, 
        role 
      })
      setSuccess("Account created successfully! Please login.")
      // Switch to login mode
      setTimeout(() => {
        setIsSignup(false)
        setSuccess("")
      }, 2000)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed")
    }
  }

  const toggleMode = () => {
    setIsSignup(!isSignup)
    setError("")
    setSuccess("")
    setEmail("")
    setPassword("")
    setFullName("")
    setOrganization("")
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 relative">
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>

      <div className="absolute inset-0 dark:bg-gradient-to-br dark:from-slate-900 dark:via-purple-900/20 dark:to-slate-900 pointer-events-none" />

      <Card className="w-full max-w-md card-glow relative z-10 dark:bg-card/80 dark:backdrop-blur-sm dark:border-primary/20">
        <CardHeader className="text-center space-y-6">
          <AuraLogo className="justify-center" />
          <div>
            <h1 className="text-2xl font-semibold text-foreground">
              {isSignup ? "Create Account" : "Welcome Back"}
            </h1>
            <p className="text-muted-foreground mt-2">
              {isSignup ? "Sign up to get started" : "Sign in to access your dashboard"}
            </p>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={isSignup ? handleSignup : handleLogin} className="space-y-4">
            {isSignup && (
              <>
                <div className="space-y-2">
                  <label htmlFor="fullName" className="text-sm font-medium text-foreground">
                    Full Name
                  </label>
                  <Input
                    id="fullName"
                    type="text"
                    placeholder="Enter your full name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                    className="dark:bg-muted/50 dark:border-primary/30 dark:focus:border-primary dark:focus:ring-primary/20"
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="organization" className="text-sm font-medium text-foreground">
                    Organization
                  </label>
                  <Input
                    id="organization"
                    type="text"
                    placeholder="Enter your organization"
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                    required
                    className="dark:bg-muted/50 dark:border-primary/30 dark:focus:border-primary dark:focus:ring-primary/20"
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="role" className="text-sm font-medium text-foreground">
                    Role
                  </label>
                  <select
                    id="role"
                    value={role}
                    onChange={(e) => setRole(e.target.value as "clinic_admin" | "gcf_coordinator")}
                    required
                    className="w-full px-3 py-2 rounded-md border border-input bg-background dark:bg-muted/50 dark:border-primary/30 dark:focus:border-primary dark:focus:ring-primary/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                  >
                    <option value="clinic_admin">Clinic Admin</option>
                    <option value="gcf_coordinator">GCF Coordinator</option>
                  </select>
                </div>
              </>
            )}
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium text-foreground">
                Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="dark:bg-muted/50 dark:border-primary/30 dark:focus:border-primary dark:focus:ring-primary/20"
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium text-foreground">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="dark:bg-muted/50 dark:border-primary/30 dark:focus:border-primary dark:focus:ring-primary/20"
              />
            </div>
            {error && <div className="text-destructive text-sm text-center">{error}</div>}
            {success && <div className="text-green-500 text-sm text-center">{success}</div>}
            <Button
              type="submit"
              className="w-full bg-primary hover:bg-primary/90 glow-primary dark:text-primary-foreground"
              disabled={isLoading}
            >
              {isLoading ? (isSignup ? "Creating Account..." : "Signing in...") : (isSignup ? "Sign Up" : "Login")}
            </Button>
            {!isSignup && (
              <div className="text-center">
                <a href="#" className="text-sm text-primary hover:underline glow-primary">
                  Forgot Password?
                </a>
              </div>
            )}
          </form>
          <div className="mt-6 text-center">
            <button
              onClick={toggleMode}
              className="text-sm text-primary hover:underline glow-primary"
              type="button"
            >
              {isSignup ? "Already have an account? Sign in" : "Don't have an account? Sign up"}
            </button>
          </div>
          <div className="mt-8 pt-6 border-t border-border text-center">
            <p className="text-xs text-muted-foreground">Powered by GCF and CDITH</p>
            <p className="text-xs text-muted-foreground mt-2">
              Default accounts: admin@gmail.com / coord@gmail.com (password: pw)
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
