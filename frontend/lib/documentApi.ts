/**
 * Document API - Functions for interacting with the document services
 */

import { API_CONFIG, STORAGE_KEYS } from './config'
import type { UploadDocumentResponse, DocumentStatus, ListDocumentsResponse } from './types'

/**
 * Get authorization headers with access token
 */
function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
  return {
    'Authorization': `Bearer ${token}`,
  }
}

/**
 * Upload a document file
 */
export async function uploadDocument(file: File): Promise<UploadDocumentResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_CONFIG.DOCUMENT_INGESTION}/documents/upload`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Upload failed' }))
    throw new Error(error.detail || error.message || 'Failed to upload document')
  }

  return response.json()
}

/**
 * List documents with pagination
 */
export async function listDocuments(
  page: number = 1,
  pageSize: number = 10
): Promise<ListDocumentsResponse> {
  const response = await fetch(
    `${API_CONFIG.DOCUMENT_INGESTION}/documents?page=${page}&page_size=${pageSize}`,
    {
      method: 'GET',
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json',
      },
    }
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to fetch documents' }))
    throw new Error(error.detail || error.message || 'Failed to fetch documents')
  }

  const data = await response.json()
  
  // Transform API response to frontend format
  const documents: DocumentStatus[] = (data.documents || []).map((doc: any) => ({
    upload_id: doc.upload_id || doc.id,
    file_info: {
      filename: doc.file_info?.filename || doc.filename || 'Unknown',
      size: doc.file_info?.size || doc.size || 0,
      content_type: doc.file_info?.content_type || doc.content_type || 'application/octet-stream',
    },
    created_at: doc.created_at || new Date().toISOString(),
    updated_at: doc.updated_at,
    status: mapDocumentStatus(doc.status),
    clinic: doc.organization || doc.clinic,
    error: doc.error_message || doc.error,
  }))

  return {
    documents,
    total: data.total || documents.length,
    page: data.page || page,
    page_size: data.limit || data.page_size || pageSize,
  }
}

/**
 * Map backend status to frontend status
 */
function mapDocumentStatus(status: string): DocumentStatus['status'] {
  switch (status?.toLowerCase()) {
    case 'pending':
      return 'pending'
    case 'processing':
      return 'processing'
    case 'completed':
    case 'uploaded':
      return 'uploaded'
    case 'parsed':
      return 'parsed'
    case 'structured':
      return 'structured'
    case 'failed':
    case 'error':
      return 'failed'
    default:
      return 'pending'
  }
}

/**
 * Get a specific document by ID
 */
export async function getDocument(documentId: string): Promise<DocumentStatus> {
  const response = await fetch(
    `${API_CONFIG.DOCUMENT_INGESTION}/documents/${documentId}`,
    {
      method: 'GET',
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json',
      },
    }
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to fetch document' }))
    throw new Error(error.detail || error.message || 'Failed to fetch document')
  }

  const doc = await response.json()
  
  return {
    upload_id: doc.upload_id || doc.id,
    file_info: {
      filename: doc.file_info?.filename || doc.filename || 'Unknown',
      size: doc.file_info?.size || doc.size || 0,
      content_type: doc.file_info?.content_type || doc.content_type || 'application/octet-stream',
    },
    created_at: doc.created_at || new Date().toISOString(),
    updated_at: doc.updated_at,
    status: mapDocumentStatus(doc.status),
    clinic: doc.organization || doc.clinic,
    error: doc.error_message || doc.error,
  }
}

/**
 * Delete a document
 */
export async function deleteDocument(documentId: string): Promise<void> {
  const response = await fetch(
    `${API_CONFIG.DOCUMENT_INGESTION}/documents/${documentId}`,
    {
      method: 'DELETE',
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json',
      },
    }
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to delete document' }))
    throw new Error(error.detail || error.message || 'Failed to delete document')
  }
}

/**
 * Get document processing status
 */
export async function getDocumentStatus(documentId: string): Promise<{
  status: string
  progress: number
  message?: string
}> {
  const response = await fetch(
    `${API_CONFIG.DOCUMENT_INGESTION}/documents/${documentId}/status`,
    {
      method: 'GET',
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json',
      },
    }
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to fetch status' }))
    throw new Error(error.detail || error.message || 'Failed to fetch status')
  }

  return response.json()
}

/**
 * Download a document
 */
export async function downloadDocument(documentId: string): Promise<Blob> {
  const response = await fetch(
    `${API_CONFIG.DOCUMENT_INGESTION}/documents/${documentId}/download`,
    {
      method: 'GET',
      headers: getAuthHeaders(),
    }
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to download document' }))
    throw new Error(error.detail || error.message || 'Failed to download document')
  }

  return response.blob()
}
