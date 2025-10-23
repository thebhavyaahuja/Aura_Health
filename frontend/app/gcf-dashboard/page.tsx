"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AuraLogo } from "@/components/aura-logo"
import { Search, AlertTriangle, Users, FileText, TrendingUp } from "lucide-react"
import { useRouter } from "next/navigation"
import { ThemeToggle } from "@/components/theme-toggle"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { useAuth } from "@/contexts/AuthContext"

interface ReportRecord {
  id: string
  patientId: string
  clinicName: string
  submissionDate: string
  riskScore: "High" | "Medium" | "Low"
  reviewStatus: "New" | "Under Review" | "Follow-up Initiated" | "Review Complete"
}

export default function GCFDashboardPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [riskFilter, setRiskFilter] = useState("All")
  const [clinicFilter, setClinicFilter] = useState("All")
  const [reports, setReports] = useState<ReportRecord[]>([
    {
      id: "1",
      patientId: "P789-A",
      clinicName: "Mercy General Hospital",
      submissionDate: "2024-01-15",
      riskScore: "High",
      reviewStatus: "Follow-up Initiated", // Updated status to reflect changes from detail screen
    },
    {
      id: "2",
      patientId: "P456-B",
      clinicName: "City Imaging Center",
      submissionDate: "2024-01-15",
      riskScore: "High",
      reviewStatus: "Under Review",
    },
    {
      id: "3",
      patientId: "P123-C",
      clinicName: "Regional Medical Center",
      submissionDate: "2024-01-14",
      riskScore: "High",
      reviewStatus: "Follow-up Initiated",
    },
    {
      id: "4",
      patientId: "P890-D",
      clinicName: "Downtown Clinic",
      submissionDate: "2024-01-14",
      riskScore: "High",
      reviewStatus: "New",
    },
    {
      id: "5",
      patientId: "P234-E",
      clinicName: "Mercy General Hospital",
      submissionDate: "2024-01-13",
      riskScore: "Medium",
      reviewStatus: "Under Review",
    },
    {
      id: "6",
      patientId: "P567-F",
      clinicName: "City Imaging Center",
      submissionDate: "2024-01-13",
      riskScore: "Medium",
      reviewStatus: "New",
    },
    {
      id: "7",
      patientId: "P345-G",
      clinicName: "Regional Medical Center",
      submissionDate: "2024-01-12",
      riskScore: "Medium",
      reviewStatus: "Review Complete",
    },
    {
      id: "8",
      patientId: "P678-H",
      clinicName: "Downtown Clinic",
      submissionDate: "2024-01-12",
      riskScore: "Medium",
      reviewStatus: "Follow-up Initiated",
    },
    {
      id: "9",
      patientId: "P901-I",
      clinicName: "Mercy General Hospital",
      submissionDate: "2024-01-11",
      riskScore: "Medium",
      reviewStatus: "Review Complete",
    },
    {
      id: "10",
      patientId: "P012-J",
      clinicName: "City Imaging Center",
      submissionDate: "2024-01-11",
      riskScore: "Low",
      reviewStatus: "Review Complete",
    },
  ])

  const router = useRouter()
  const { user, logout } = useAuth()

  useEffect(() => {
    const handleStorageChange = () => {
      const updatedReport = localStorage.getItem("updatedReport")
      if (updatedReport) {
        const reportData = JSON.parse(updatedReport)
        setReports((prev) =>
          prev.map((report) =>
            report.id === reportData.id ? { ...report, reviewStatus: reportData.reviewStatus } : report,
          ),
        )
        localStorage.removeItem("updatedReport")
      }
    }

    window.addEventListener("storage", handleStorageChange)
    handleStorageChange() // Check on mount

    return () => window.removeEventListener("storage", handleStorageChange)
  }, [])

  const filteredReports = reports.filter((report) => {
    const matchesSearch =
      report.patientId.toLowerCase().includes(searchTerm.toLowerCase()) ||
      report.clinicName.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRisk = riskFilter === "All" || report.riskScore === riskFilter
    const matchesClinic = clinicFilter === "All" || report.clinicName === clinicFilter

    return matchesSearch && matchesRisk && matchesClinic
  })

  const getRiskBadgeClass = (risk: string) => {
    switch (risk) {
      case "High":
        return "risk-high px-2 py-1 rounded-full text-xs font-medium"
      case "Medium":
        return "risk-medium px-2 py-1 rounded-full text-xs font-medium"
      case "Low":
        return "risk-low px-2 py-1 rounded-full text-xs font-medium"
      default:
        return "bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs font-medium"
    }
  }

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case "New":
        return "status-new px-2 py-1 rounded-full text-xs font-medium"
      case "Under Review":
        return "status-review px-2 py-1 rounded-full text-xs font-medium"
      case "Follow-up Initiated":
        return "status-followup px-2 py-1 rounded-full text-xs font-medium"
      case "Review Complete":
        return "status-complete px-2 py-1 rounded-full text-xs font-medium"
      default:
        return "bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs font-medium"
    }
  }

  const handleViewDetails = (report: ReportRecord) => {
    router.push(`/report-detail/${report.id}`)
  }

  // Calculate KPIs
  const newReportsToday = reports.filter((r) => r.submissionDate === "2024-01-15").length
  const highRiskPending = reports.filter((r) => r.riskScore === "High" && r.reviewStatus !== "Review Complete").length
  const mediumRiskCases = reports.filter((r) => r.riskScore === "Medium").length
  const totalReports = 342 // Static number as per spec

  return (
    <ProtectedRoute allowedRoles={['gcf_coordinator']}>
    <div className="min-h-screen bg-background">
      {/* Gradient background for dark theme */}
      <div className="absolute inset-0 dark:bg-gradient-to-br dark:from-slate-900 dark:via-purple-900/20 dark:to-slate-900 pointer-events-none" />

      {/* Header */}
      <header className="bg-card border-b border-border relative z-10 dark:bg-card/80 dark:backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <AuraLogo />
            <div className="flex items-center gap-4">
              {/* Theme toggle */}
              <ThemeToggle />
              <div className="text-right">
                <p className="text-sm font-medium text-foreground">{user?.full_name || "GCF Coordinator"}</p>
                <p className="text-xs text-muted-foreground">{user?.organization || "GCF Program"}</p>
              </div>
              <Button
                variant="outline"
                onClick={logout}
                className="text-primary border-primary hover:bg-primary hover:text-primary-foreground glow-primary"
              >
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
        <div className="space-y-8">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="card-glow dark:bg-card/80 dark:backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">New Reports Today</p>
                    <p className="text-3xl font-bold text-foreground">{newReportsToday}</p>
                  </div>
                  <FileText className="w-8 h-8 text-primary" />
                </div>
              </CardContent>
            </Card>

            <Card className="border-destructive/20 card-glow dark:bg-card/80 dark:backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">High-Risk Cases Pending</p>
                    <p className="text-3xl font-bold text-destructive">{highRiskPending}</p>
                  </div>
                  <AlertTriangle className="w-8 h-8 text-destructive" />
                </div>
              </CardContent>
            </Card>

            <Card className="card-glow dark:bg-card/80 dark:backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Medium-Risk Cases</p>
                    <p className="text-3xl font-bold text-warning">{mediumRiskCases}</p>
                  </div>
                  <Users className="w-8 h-8 text-warning" />
                </div>
              </CardContent>
            </Card>

            <Card className="card-glow dark:bg-card/80 dark:backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Total Reports Processed</p>
                    <p className="text-3xl font-bold text-foreground">{totalReports}</p>
                  </div>
                  <TrendingUp className="w-8 h-8 text-success" />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Filters and Search */}
          <Card className="card-glow dark:bg-card/80 dark:backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-xl text-foreground">Report Management</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col sm:flex-row gap-4 mb-6">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                  <Input
                    placeholder="Search by Patient ID or Name..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 dark:bg-muted/50 dark:border-primary/30 dark:focus:border-primary dark:focus:ring-primary/20"
                  />
                </div>
                <Select value={riskFilter} onValueChange={setRiskFilter}>
                  <SelectTrigger className="w-full sm:w-48 dark:bg-muted/50 dark:border-primary/30">
                    <SelectValue placeholder="Filter by Risk" />
                  </SelectTrigger>
                  <SelectContent className="dark:bg-card dark:border-primary/30">
                    <SelectItem value="All">All Risk Levels</SelectItem>
                    <SelectItem value="High">High Risk</SelectItem>
                    <SelectItem value="Medium">Medium Risk</SelectItem>
                    <SelectItem value="Low">Low Risk</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={clinicFilter} onValueChange={setClinicFilter}>
                  <SelectTrigger className="w-full sm:w-48 dark:bg-muted/50 dark:border-primary/30">
                    <SelectValue placeholder="Filter by Clinic" />
                  </SelectTrigger>
                  <SelectContent className="dark:bg-card dark:border-primary/30">
                    <SelectItem value="All">All Clinics</SelectItem>
                    <SelectItem value="Mercy General Hospital">Mercy General Hospital</SelectItem>
                    <SelectItem value="City Imaging Center">City Imaging Center</SelectItem>
                    <SelectItem value="Regional Medical Center">Regional Medical Center</SelectItem>
                    <SelectItem value="Downtown Clinic">Downtown Clinic</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Reports Table */}
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="text-left py-3 px-4 font-medium text-foreground">Risk Score</th>
                      <th className="text-left py-3 px-4 font-medium text-foreground">Patient Identifier</th>
                      <th className="text-left py-3 px-4 font-medium text-foreground">Clinic Name</th>
                      <th className="text-left py-3 px-4 font-medium text-foreground">Submission Date</th>
                      <th className="text-left py-3 px-4 font-medium text-foreground">Review Status</th>
                      <th className="text-left py-3 px-4 font-medium text-foreground">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredReports.map((report) => (
                      <tr
                        key={report.id}
                        className="border-b border-border hover:bg-muted/50 dark:hover:bg-primary/5 transition-colors"
                      >
                        <td className="py-3 px-4">
                          <span className={getRiskBadgeClass(report.riskScore)}>{report.riskScore}</span>
                        </td>
                        <td className="py-3 px-4 font-mono text-foreground">{report.patientId}</td>
                        <td className="py-3 px-4 text-foreground">{report.clinicName}</td>
                        <td className="py-3 px-4 text-muted-foreground">{report.submissionDate}</td>
                        <td className="py-3 px-4">
                          <span className={getStatusBadgeClass(report.reviewStatus)}>{report.reviewStatus}</span>
                        </td>
                        <td className="py-3 px-4">
                          <Button
                            size="sm"
                            onClick={() => handleViewDetails(report)}
                            className="bg-primary hover:bg-primary/90 text-primary-foreground glow-primary"
                          >
                            View Details
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              <div className="flex items-center justify-between mt-6">
                <p className="text-sm text-muted-foreground">
                  Showing {filteredReports.length} of {reports.length} reports
                </p>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" disabled>
                    Previous
                  </Button>
                  <Button variant="outline" size="sm" className="bg-primary text-primary-foreground glow-primary">
                    1
                  </Button>
                  <Button variant="outline" size="sm">
                    2
                  </Button>
                  <Button variant="outline" size="sm">
                    Next
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
    </ProtectedRoute>
  )
}
