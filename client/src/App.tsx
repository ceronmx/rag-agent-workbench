import { useState } from "react";
import { ContextualInsights } from "./components/chat/results/ContextualInsights";
import { SynthesisResult } from "./components/chat/results/SynthesisResult";
// Modular Components
import { DocumentList } from "./components/documents/DocumentList";
import { DocumentUpload } from "./components/documents/DocumentUpload";
import { Layout } from "./components/layout/Layout";

function App() {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <Layout searchQuery={searchQuery} onSearchChange={setSearchQuery}>
      <SynthesisResult />

      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <h2 className="text-2xl lg:text-3xl font-bold tracking-tight uppercase lg:normal-case text-foreground">
              Data Sources
            </h2>
          </div>
          <div className="hidden lg:block">
            <DocumentUpload />
          </div>
        </div>

        <DocumentList searchQuery={searchQuery} />
      </section>

      <ContextualInsights />
    </Layout>
  );
}

export default App;
