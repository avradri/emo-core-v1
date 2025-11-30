// dashboard/app/components/ScenarioTable.tsx

export interface DestineScenarioOverlay {
  twin_id: string | null;
  collection_id: string;
  item_id: string;
  title: string | null;
  time_start: string | null;
  time_end: string | null;
  bbox: number[] | null;
  oi_mean: number | null;
  oi_trend_20y: number | null;
  omega_synergy: number | null;
  gwi_ignitions: number | null;
  smf_global: number | null;
  smf_corr: number | null;
  tau_i_accel_ratio: number | null;
}

function adequacyTag(row: DestineScenarioOverlay): { label: string; className: string } {
  const oi = row.oi_mean ?? 0;
  const smf = row.smf_global ?? 0;

  const score = 0.5 * oi + 0.5 * smf;

  if (score >= 0.65) {
    return { label: "Cognitively adequate", className: "good" };
  }
  if (score >= 0.4) {
    return { label: "At risk", className: "risky" };
  }
  return { label: "Failing", className: "bad" };
}

export default function ScenarioTable({
  rows
}: {
  rows: DestineScenarioOverlay[];
}) {
  if (!rows.length) {
    return (
      <div className="emo-card">
        <div className="emo-card-header">
          <div className="emo-card-title">DestinE scenarios</div>
          <div className="emo-card-badge">Dual-twin overlays</div>
        </div>
        <div className="emo-card-body">
          <p>No DestinE scenarios available yet. Configure DestinE access and reload.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="emo-card">
      <div className="emo-card-header">
        <div className="emo-card-title">DestinE climate scenarios × EMO metrics</div>
        <div className="emo-card-badge">Dual twin</div>
      </div>
      <div className="emo-card-body">
        <div className="scenario-table-root">
          <table className="scenario-table">
            <thead>
              <tr>
                <th>Scenario</th>
                <th>Window</th>
                <th>OI</th>
                <th>SMF</th>
                <th>Ω (synergy)</th>
                <th>GWI bursts</th>
                <th>τ_I accel</th>
                <th>Adequacy</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => {
                const tag = adequacyTag(row);
                return (
                  <tr key={row.item_id}>
                    <td>
                      <div>
                        <div>{row.title || row.item_id}</div>
                        <div style={{ fontSize: "0.7rem", color: "#9ca3af" }}>
                          {row.collection_id}
                        </div>
                      </div>
                    </td>
                    <td>
                      <div style={{ fontSize: "0.75rem" }}>
                        {row.time_start?.slice(0, 10)} – {row.time_end?.slice(0, 10)}
                      </div>
                    </td>
                    <td>{row.oi_mean != null ? row.oi_mean.toFixed(2) : "–"}</td>
                    <td>{row.smf_global != null ? row.smf_global.toFixed(2) : "–"}</td>
                    <td>
                      {row.omega_synergy != null ? row.omega_synergy.toFixed(2) : "–"}
                    </td>
                    <td>{row.gwi_ignitions ?? "–"}</td>
                    <td>
                      {row.tau_i_accel_ratio != null
                        ? row.tau_i_accel_ratio.toFixed(2) + "×"
                        : "–"}
                    </td>
                    <td>
                      <span className={`scenario-tag ${tag.className}`}>{tag.label}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
