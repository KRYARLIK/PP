import axios from 'axios'
import type { DocumentListResponse, DocumentRecord, SearchResponse } from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '/api/v1',
  timeout: 120_000,
})

function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (error.code === 'ECONNABORTED') return 'Сервер не ответил вовремя'
  }
  return 'Произошла непредвиденная ошибка'
}

export async function uploadDocument(
  file: File,
  onProgress: (progress: number) => void,
): Promise<DocumentRecord> {
  const form = new FormData()
  form.append('file', file)
  try {
    const response = await api.post<DocumentRecord>('/documents/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (event) => {
        if (!event.total) return
        const progress = Math.min(100, Math.round((event.loaded * 100) / event.total))
        onProgress(progress)
      },
    })
    return response.data
  } catch (error) {
    throw new Error(getErrorMessage(error))
  }
}

export async function listDocuments(): Promise<DocumentListResponse> {
  const response = await api.get<DocumentListResponse>('/documents', { params: { page: 1, size: 100 } })
  return response.data
}

export async function searchDocuments(query: string, page = 1, size = 10): Promise<SearchResponse> {
  try {
    const response = await api.get<SearchResponse>('/search', { params: { q: query, page, size } })
    return response.data
  } catch (error) {
    throw new Error(getErrorMessage(error))
  }
}
