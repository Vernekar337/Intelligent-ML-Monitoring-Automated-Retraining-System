
export function mapHealthResponse(apiData) {
  console.log("MAPPER INPUT:", apiData);

  const mapped = {
    model_version: apiData.model_version,
    system_status: apiData.overall_status ?? "unknown",
    last_pipeline_run: apiData.generated_at,
    retraining_recommended: apiData.actions?.retraining_recommended ?? false,
    cooldown_active: false
  };

  console.log("MAPPER OUTPUT:", mapped);
  return mapped;
}
