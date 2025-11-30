// dashboard/app/page.tsx
import UIAGauge, { DestineUIASummary } from "./components/UIAGauge";
import ScenarioTable, {
  DestineScenarioOverlay
} from "./components/ScenarioTable";

const API_BASE =
  process.env.NEXT_PUBLIC_EMO_API_BASE || "http://localhost:8000";

async function fetchJSON<T>(path: string): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { cache: "no-store" });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(
      `Request to ${url} failed: ${res.status} ${res.statusText} ${text}`
    );
  }

  return (await res.json()) as T;
}

export default async function Page() {
  let uiaSummary: DestineUIASummary | null = null;
  let overlays: DestineScenarioOverlay[] = [];
  let error: string | null = null;

  try {
    const [uiaRes, overlayRes] = await Promise.all([
      fetchJSON<DestineUIASummary>("/v1/uia/destine/summary"),
      fetchJSON<DestineScenarioOverlay[]>("/v1/metrics/destine/scenarios/overlays")
    ]);
    uiaSummary = uiaRes;
    overlays = overlayRes;
  } catch (e: unknown) {
    error =
      e instanceof Error ? e.message : "Failed to load data from EMO API.";
  }

  return (
    <main>
      <header className="emo-header">
        <h1 className="emo-title">Emergent Mind Observatory – DestinE Dual-Twin</h1>
        <p className="emo-subtitle">
          A live cognitive overlay on DestinE climate scenarios. UIA-inspired
          vital signs for the human–Earth interface – in one glance.
        </p>
      </header>

      {error && (
        <div className="emo-error">
          <strong>API error:</strong> {error}
        </div>
      )}

      <section className="emo-grid" aria-label="UIA gauge and scenario table">
        <div>
          {uiaSummary ? (
            <UIAGauge summary={uiaSummary} />
          ) : (
            <div className="emo-card">
              <div className="emo-card-header">
                <div className="emo-card-title">Climate cognition gauge</div>
              </div>
              <div className="emo-card-body">
                <p>Waiting for UIA summary from the EMO API…</p>
              </div>
            </div>
          )}
        </div>
        <div>
          <ScenarioTable rows={overlays} />
        </div>
      </section>
    </main>
  );
}
