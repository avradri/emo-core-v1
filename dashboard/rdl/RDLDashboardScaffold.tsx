import React from "react";

type ScoreSummary = {
  overall_score?: number;
  feasibility?: number;
  expected_dac_gain?: number;
  persistence_likelihood?: number;
  contradiction_risk?: number;
  justice_risk?: number;
  legitimacy_penalty?: number;
  semantic_efficiency?: number;
};

type DashboardProps = {
  domain?: string;
  jurisdiction?: string;
  dominantBottlenecks?: string[];
  confidence?: number;
  portfolioId?: string;
  sequence?: string[];
  rationale?: string;
  score?: ScoreSummary;
  tradeoffSummary?: string;
  legitimacySummary?: string;
  comparisonSummary?: string;
  learningSummary?: string;
};

function Panel({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section
      style={{
        border: "1px solid #ccc",
        borderRadius: 12,
        padding: 16,
        background: "#fff",
      }}
    >
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      {children}
    </section>
  );
}

export default function RDLDashboardScaffold({
  domain,
  jurisdiction,
  dominantBottlenecks = [],
  confidence,
  portfolioId,
  sequence = [],
  rationale,
  score,
  tradeoffSummary,
  legitimacySummary,
  comparisonSummary,
  learningSummary,
}: DashboardProps) {
  return (
    <main style={{ padding: 24 }}>
      <h1>RDL Dashboard Scaffold</h1>
      <p>
        A first governance-facing interface for the Remedy Design Layer.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: 16,
        }}
      >
        <Panel title="Dominant Bottlenecks">
          <p><strong>Domain:</strong> {domain ?? "-"}</p>
          <p><strong>Jurisdiction:</strong> {jurisdiction ?? "-"}</p>
          <p>
            <strong>Bottlenecks:</strong>{" "}
            {dominantBottlenecks.length ? dominantBottlenecks.join(", ") : "-"}
          </p>
          <p><strong>Confidence:</strong> {confidence ?? "-"}</p>
        </Panel>

        <Panel title="Recommended Portfolio">
          <p><strong>Portfolio ID:</strong> {portfolioId ?? "-"}</p>
          <p>
            <strong>Sequence:</strong>{" "}
            {sequence.length ? sequence.join(" → ") : "-"}
          </p>
          <p><strong>Rationale:</strong> {rationale ?? "-"}</p>
        </Panel>

        <Panel title="Score Summary">
          <p><strong>Overall:</strong> {score?.overall_score ?? "-"}</p>
          <p><strong>Feasibility:</strong> {score?.feasibility ?? "-"}</p>
          <p><strong>Expected DAC gain:</strong> {score?.expected_dac_gain ?? "-"}</p>
          <p><strong>Persistence:</strong> {score?.persistence_likelihood ?? "-"}</p>
          <p><strong>Contradiction risk:</strong> {score?.contradiction_risk ?? "-"}</p>
          <p><strong>Justice risk:</strong> {score?.justice_risk ?? "-"}</p>
          <p><strong>Legitimacy penalty:</strong> {score?.legitimacy_penalty ?? "-"}</p>
          <p><strong>Semantic efficiency:</strong> {score?.semantic_efficiency ?? "-"}</p>
        </Panel>

        <Panel title="Tradeoff Report">
          <p>{tradeoffSummary ?? "-"}</p>
        </Panel>

        <Panel title="Legitimacy Review">
          <p>{legitimacySummary ?? "-"}</p>
        </Panel>

        <Panel title="Portfolio Comparison">
          <p>{comparisonSummary ?? "-"}</p>
        </Panel>

        <Panel title="Adaptive Learning">
          <p>{learningSummary ?? "-"}</p>
        </Panel>
      </div>
    </main>
  );
}
