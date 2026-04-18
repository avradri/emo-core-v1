import RDLDashboard from "../components/RDLDashboard";

export default function RDLPage() {
  return (
    <RDLDashboard
      domain="disaster"
      jurisdiction="RO"
      dominantBottlenecks={["translation", "contradiction"]}
      confidence={0.75}
      portfolioId="disaster_RO_translation_contradiction"
      sequence={[
        "Automatic mutual-aid triggers",
        "Public warning protocol harmonization",
      ]}
      rationale="Initial scaffold view using static sample values before live API wiring."
      score={{
        overall_score: 0.61,
        feasibility: 0.65,
        expected_dac_gain: 0.75,
        persistence_likelihood: 0.65,
        contradiction_risk: 0.5,
        justice_risk: 0.2,
        legitimacy_penalty: 0.024,
        semantic_efficiency: 0.625,
      }}
      tradeoffSummary="Moderate feasibility and expected gain are offset by coordination and contradiction risks."
      legitimacySummary="Low rights-risk profile, but transparency and contestability remain required."
      comparisonSummary="Best comparison variant: compact."
      learningSummary="No observed outcomes loaded yet."
    />
  );
}
