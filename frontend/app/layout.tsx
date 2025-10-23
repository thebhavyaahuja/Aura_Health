import type React from "react"
import { Inter } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/hooks/use-theme"
import { AuthProvider } from "@/contexts/AuthContext"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
})

export const metadata = {
  title: "Aura Health - Mammogram Report Management",
  description: "Professional medical tool for managing mammogram reports and risk assessment",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} antialiased`}>
      <body className="min-h-screen bg-background font-sans text-foreground">
        <AuthProvider>
          <ThemeProvider defaultTheme="light" storageKey="aura-health-theme">
            {children}
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
