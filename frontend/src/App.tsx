import { useCallback, useEffect, useState } from 'react'
import { DocumentsList } from './components/DocumentsList'
import { SearchPanel } from './components/SearchPanel'
import { UploadZone } from './components/UploadZone'
import { listDocuments } from './services/api'
import type { DocumentRecord } from './types'

export default function App() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([])
  const [loadingDocuments, setLoadingDocuments] = useState(true)

  const refreshDocuments = useCallback(async () => {
    try {
      const data = await listDocuments()
      setDocuments(data.items)
    } finally {
      setLoadingDocuments(false)
    }
  }, [])

  useEffect(() => {
    void refreshDocuments()
  }, [refreshDocuments])

  return (
    <div className="app-shell">
      <header className="hero">
        <div className="hero__content">
          <p className="hero__kicker">Учебный проект · Программная инженерия</p>
          <h1>Интеллектуальный поиск по базе знаний университета</h1>
          <p>
            Загружайте учебные материалы в PDF и DOCX, а затем находите нужные
            фрагменты с русскоязычным полнотекстовым поиском.
          </p>
          <div className="hero__links">
            <a href="/docs" target="_blank" rel="noreferrer">Swagger API</a>
            <a href="/api/v1/health" target="_blank" rel="noreferrer">Состояние сервисов</a>
          </div>
        </div>
      </header>

      <main>
        <div className="grid-two">
          <UploadZone onUploaded={refreshDocuments} />
          <DocumentsList documents={documents} loading={loadingDocuments} />
        </div>
        <SearchPanel />
      </main>

      <footer>
        FastAPI · React · PostgreSQL · Elasticsearch · Redis · Docker
      </footer>
    </div>
  )
}
