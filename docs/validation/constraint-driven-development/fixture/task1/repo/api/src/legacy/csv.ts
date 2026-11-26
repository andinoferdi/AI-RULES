/* eslint-disable @typescript-eslint/no-explicit-any */
// Old CSV writer kept for the accounting export until LED-112 lands.

export function toCsv(rows: any[]): string {
  // @ts-ignore -- rows come from the old report builder without types
  const header = Object.keys(rows[0]).join(",");
  // TODO(LED-112): quote fields that contain commas
  return [header, ...rows.map((row) => Object.values(row).join(","))].join("\n");
}
