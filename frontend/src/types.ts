export type DocumentStatus = 'processing' | 'ready' | 'error'

export interface DocumentRecord {
  id: string
  file_name: string
  file_type: string
  file_size: number
  status: DocumentStatus
  chunks_count: number
  error_message: string | null
  uploaded_at: string
}

export interface DocumentListResponse {
  total: number
  items: DocumentRecord[]
}

export interface SearchResultItem {
  chunk_id: string
  document_id: string
  file_name: string
  page: number
  text: string
  highlight: string | null
  score: number
}

export interface SearchResponse {
  query: string
  page: number
  size: number
  total: number
  cached: boolean
  items: SearchResultItem[]
}

export type UploadState = 'uploading' | 'indexing' | 'ready' | 'error'

export interface UploadItem {
  id: string
  fileName: string
  progress: number
  state: UploadState
  error?: string
}
