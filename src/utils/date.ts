/**
 * Dynamic Year & Date Utility
 * Automatically returns the current year to ensure SEO titles, descriptions,
 * copyright badges, and schema data stay fresh without manual intervention.
 */
export const currentYear = new Date().getFullYear();

/**
 * Returns formatted season string (e.g., "2026/2027" or "2027/2028")
 * Automatically rolls forward:
 * Season is formatted as currentYear / (currentYear + 1)
 */
export const currentSeason = `${currentYear}/${currentYear + 1}`;
export const nextSeason = `${currentYear + 1}/${currentYear + 2}`;

/**
 * Returns the current football league season start year.
 * Bundesliga season starts in summer (~August).
 * From July to December: current calendar year.
 * From January to June: previous calendar year.
 */
export const leagueSeasonYear = new Date().getMonth() >= 6 ? currentYear : currentYear - 1;

/**
 * Replaces any 4-digit year from 2024 to 2035 in static strings (titles, descriptions, headings)
 * with the dynamically computed currentYear. Ensures that articles and metadata
 * never get stuck on an outdated year.
 */
export function injectCurrentYear(text: string): string {
  if (!text) return text;
  return text.replace(/\b202[4-9]\b|\b203[0-5]\b/g, String(currentYear));
}
