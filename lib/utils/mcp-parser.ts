/**
 * MCP Output Parser Utilities
 *
 * File: mcp-parser.ts
 * Created: 2025-11-19
 * Purpose: Robust JSON extraction from MCP tool output
 *
 * Problem: MCP tools often prefix output with emojis and status text
 * Example: "🔧 Claude-Flow initialized\n[{...}]"
 * This causes JSON.parse() to fail with "Unexpected token '�'"
 *
 * Solution: Extract JSON portion from mixed output
 */

/**
 * Extract JSON from MCP output that may contain emoji/text prefix
 *
 * @param output - Raw output from MCP command (stdout)
 * @returns Parsed JSON object
 * @throws Error if no valid JSON found in output
 *
 * @example
 * const output = "🔧 Starting...\n[{\"id\":1}]";
 * const data = extractJSON(output); // [{id: 1}]
 */
export function extractJSON(output: string): any {
  if (!output || typeof output !== 'string') {
    throw new Error('Invalid MCP output: expected string');
  }

  // Remove any leading non-JSON content (emojis, text, etc.)
  // JSON always starts with { or [
  const jsonStart = output.search(/[\{\[]/);

  if (jsonStart === -1) {
    throw new Error(
      `No JSON found in MCP output. First 100 chars: ${output.substring(0, 100)}`
    );
  }

  // Extract JSON portion and trim whitespace
  const jsonString = output.substring(jsonStart).trim();

  // Parse and return
  try {
    return JSON.parse(jsonString);
  } catch (error: any) {
    throw new Error(
      `Failed to parse JSON from MCP output. ` +
      `JSON portion (first 200 chars): ${jsonString.substring(0, 200)}. ` +
      `Original error: ${error.message}`
    );
  }
}

/**
 * Safe JSON extraction that returns null on failure
 *
 * @param output - Raw output from MCP command
 * @returns Parsed JSON object or null
 *
 * @example
 * const data = extractJSONSafe("invalid"); // null
 */
export function extractJSONSafe(output: string): any | null {
  try {
    return extractJSON(output);
  } catch {
    return null;
  }
}

/**
 * Extract JSON with fallback value
 *
 * @param output - Raw output from MCP command
 * @param fallback - Fallback value if parsing fails
 * @returns Parsed JSON object or fallback
 *
 * @example
 * const data = extractJSONWithFallback("invalid", []); // []
 */
export function extractJSONWithFallback<T>(output: string, fallback: T): any | T {
  try {
    return extractJSON(output);
  } catch {
    return fallback;
  }
}

/**
 * Check if output contains valid JSON
 *
 * @param output - Raw output to check
 * @returns True if valid JSON can be extracted
 */
export function hasJSON(output: string): boolean {
  return extractJSONSafe(output) !== null;
}

/**
 * Extract multiple JSON objects from output (newline-delimited JSON)
 *
 * @param output - Raw output that may contain multiple JSON objects
 * @returns Array of parsed JSON objects
 *
 * @example
 * const output = "🔧 Line 1\n{\"a\":1}\n{\"b\":2}";
 * const data = extractMultipleJSON(output); // [{a:1}, {b:2}]
 */
export function extractMultipleJSON(output: string): any[] {
  const results: any[] = [];
  const lines = output.split('\n');

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
      try {
        results.push(JSON.parse(trimmed));
      } catch {
        // Skip invalid JSON lines
        continue;
      }
    }
  }

  return results;
}

/**
 * Extract text prefix from MCP output (everything before JSON)
 *
 * @param output - Raw output from MCP command
 * @returns Text prefix or empty string
 *
 * @example
 * const output = "🔧 Starting...\n[{\"id\":1}]";
 * const prefix = extractPrefix(output); // "🔧 Starting..."
 */
export function extractPrefix(output: string): string {
  const jsonStart = output.search(/[\{\[]/);
  if (jsonStart === -1) {
    return output;
  }
  return output.substring(0, jsonStart).trim();
}

/**
 * Parse MCP output into structured result
 *
 * @param output - Raw output from MCP command
 * @returns Structured result with prefix, data, and raw output
 */
export interface MCPParseResult<T = any> {
  prefix: string;
  data: T;
  raw: string;
  hasJSON: boolean;
}

export function parseMCPOutput<T = any>(output: string): MCPParseResult<T> {
  const prefix = extractPrefix(output);
  const data = extractJSONSafe(output);

  return {
    prefix,
    data,
    raw: output,
    hasJSON: data !== null
  };
}
