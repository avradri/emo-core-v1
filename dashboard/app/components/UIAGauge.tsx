// dashboard/app/components/UIAGauge.tsx
export interface DestineUIASummary {
  twin_id: string;
  n_scenarios: number;
  oi_mean_avg: number | null;
  smf_global_avg: number | null;
  omega_synergy_avg: number | null;
  gwi_ignitions_total: number | null;
  tau_i_accel_ratio_avg: number | null;
  uia_proxy: number | null;
}

function clamp01(x: number): number {
  if (Number.isNaN(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

function healthLabel(uia: number | null): string {
  if (uia == null) return "UIA engine warming up";
  const v = clamp01(uia);
  if (v >= 0.66) return "UIA-balanced / responsive";
  if (v >= 0.33) return "Unstable band";
  return "Pathological band candidate";
}

export default function UIAGauge({ summary }: { summary: DestineUIASummary }) {
  const { uia_proxy, n_scenarios, oi_mean_avg, smf_global_avg, tau_i_accel_ratio_avg } =
    summary;

  const pos = uia_proxy != null ? clamp01(uia_proxy) : 0.5;
  const leftPercent = `${pos * 100}%`;

  return (
    <div className="emo-card">
      <div className="emo-card-header">
        <div className="emo-card-title">Climate cognition gauge (prototype UIA)</div>
        <div className="emo-card-badge">Human–Earth interface</div>
      </div>
      <div className="emo-card-body">
        <div className="uia-gauge-root">
          <div className="uia-gauge-main">
            <div className="uia-gauge-track">
              <div className="uia-gauge-bands">
                <div className="uia-band pathological" />
                <div className="uia-band unstable" />
                <div className="uia-band healthy" />
              </div>
              <div className="uia-gauge-pointer" style={{ left: leftPercent }} />
            </div>
            <div className="uia-gauge-ticks">
              <span>Pathological</span>
              <span>Unstable</span>
              <span>Healthy</span>
            </div>
          </div>
          <div className="uia-gauge-meta">
            <span className="uia-chip">
              Scenarios: <strong>{n_scenarios}</strong>
            </span>
            {oi_mean_avg != null && (
              <span className="uia-chip">
                OI (avg): <strong>{oi_mean_avg.toFixed(2)}</strong>
              </span>
            )}
            {smf_global_avg != null && (
              <span className="uia-chip">
                SMF (avg): <strong>{smf_global_avg.toFixed(2)}</strong>
              </span>
            )}
            {tau_i_accel_ratio_avg != null && (
              <span className="uia-chip">
                τ_I accel: <strong>{tau_i_accel_ratio_avg.toFixed(2)}×</strong>
              </span>
            )}
          </div>
          <div className="uia-gauge-meta">
            <span>{healthLabel(uia_proxy)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
