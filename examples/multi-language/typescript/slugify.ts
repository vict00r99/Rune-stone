// Generated from: ../slugify.rune

/**
 * Map of accented characters to ASCII equivalents.
 * Covers common Latin diacritics.
 */
const ACCENT_MAP: Record<string, string> = {
  à: "a", á: "a", â: "a", ã: "a", ä: "a", å: "a",
  è: "e", é: "e", ê: "e", ë: "e",
  ì: "i", í: "i", î: "i", ï: "i",
  ò: "o", ó: "o", ô: "o", õ: "o", ö: "o",
  ù: "u", ú: "u", û: "u", ü: "u",
  ñ: "n", ç: "c", ß: "ss",
  À: "A", Á: "A", Â: "A", Ã: "A", Ä: "A", Å: "A",
  È: "E", É: "E", Ê: "E", Ë: "E",
  Ì: "I", Í: "I", Î: "I", Ï: "I",
  Ò: "O", Ó: "O", Ô: "O", Õ: "O", Ö: "O",
  Ù: "U", Ú: "U", Û: "U", Ü: "U",
  Ñ: "N", Ç: "C",
};

/**
 * Converts a text string into a URL-friendly slug.
 *
 * @param text - Any string to slugify.
 * @param separator - Character to join words (default: hyphen).
 * @returns Lowercase slug with only [a-z0-9] and the separator.
 */
export function slugify(text: string, separator: string = "-"): string {
  if (!text) {
    return "";
  }

  // Replace accented characters using the map
  let slug = text
    .split("")
    .map((char) => ACCENT_MAP[char] ?? char)
    .join("");

  // Lowercase
  slug = slug.toLowerCase();

  // Remove everything that's not alphanumeric, space, or hyphen
  slug = slug.replace(/[^a-z0-9\s-]/g, "");

  // Replace whitespace and hyphens with separator
  const separatorPattern = new RegExp(`[\\s-]+`, "g");
  slug = slug.replace(separatorPattern, separator);

  // Trim leading/trailing separators
  const trimPattern = new RegExp(
    `^\\${separator}+|\\${separator}+$`,
    "g"
  );
  slug = slug.replace(trimPattern, "");

  return slug;
}
