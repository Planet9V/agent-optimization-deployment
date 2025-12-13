#!/usr/bin/env ts-node

/**
 * Comprehensive API Testing Framework
 * Tests all 232 APIs systematically after middleware fixes
 */

import axios, { AxiosResponse, AxiosError } from 'axios';
import * as fs from 'fs';
import * as path from 'path';

interface APIEndpoint {
  path: string;
  method: string;
  description: string;
}

interface APICategory {
  count: number;
  base_path: string;
  endpoints: APIEndpoint[];
}

interface APIInventory {
  total_apis: number;
  categories: {
    [key: string]: APICategory;
  };
}

interface TestResult {
  category: string;
  endpoint: string;
  method: string;
  url: string;
  status: 'PASS' | 'FAIL' | 'ERROR';
  http_status?: number;
  response_time?: number;
  error?: string;
  response_schema?: any;
  timestamp: string;
}

interface CategorySummary {
  category: string;
  total: number;
  passed: number;
  failed: number;
  errors: number;
  avg_response_time: number;
}

class ComprehensiveAPITester {
  private baseUrl: string;
  private results: TestResult[] = [];
  private inventory: APIInventory;
  private outputDir: string;

  constructor(baseUrl: string = 'http://localhost:3000') {
    this.baseUrl = baseUrl;
    this.outputDir = path.join(__dirname, 'results');

    // Load API inventory
    const inventoryPath = path.join(__dirname, 'api-inventory.json');
    this.inventory = JSON.parse(fs.readFileSync(inventoryPath, 'utf-8'));

    // Create output directory
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  /**
   * Test a single API endpoint
   */
  private async testEndpoint(
    category: string,
    endpoint: APIEndpoint,
    basePath: string
  ): Promise<TestResult> {
    const url = `${this.baseUrl}${basePath}${endpoint.path}`;
    const startTime = Date.now();

    const result: TestResult = {
      category,
      endpoint: endpoint.path,
      method: endpoint.method,
      url,
      status: 'ERROR',
      timestamp: new Date().toISOString()
    };

    try {
      let response: AxiosResponse;

      // Make request based on method
      switch (endpoint.method) {
        case 'GET':
          response = await axios.get(url, { timeout: 5000 });
          break;
        case 'POST':
          response = await axios.post(url, {}, { timeout: 5000 });
          break;
        case 'PUT':
          response = await axios.put(url, {}, { timeout: 5000 });
          break;
        case 'DELETE':
          response = await axios.delete(url, { timeout: 5000 });
          break;
        default:
          throw new Error(`Unsupported method: ${endpoint.method}`);
      }

      result.http_status = response.status;
      result.response_time = Date.now() - startTime;

      // Check if response is valid
      if (response.status >= 200 && response.status < 300) {
        result.status = 'PASS';
        result.response_schema = this.analyzeResponseSchema(response.data);
      } else {
        result.status = 'FAIL';
        result.error = `HTTP ${response.status}`;
      }
    } catch (error) {
      result.response_time = Date.now() - startTime;

      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        result.http_status = axiosError.response?.status;
        result.error = axiosError.message;

        // Distinguish between client errors (4xx) and server errors (5xx)
        if (result.http_status && result.http_status >= 400 && result.http_status < 500) {
          result.status = 'FAIL'; // Client error
        } else {
          result.status = 'ERROR'; // Server error or network issue
        }
      } else {
        result.error = (error as Error).message;
        result.status = 'ERROR';
      }
    }

    return result;
  }

  /**
   * Analyze response schema
   */
  private analyzeResponseSchema(data: any): any {
    if (typeof data !== 'object' || data === null) {
      return { type: typeof data };
    }

    if (Array.isArray(data)) {
      return {
        type: 'array',
        length: data.length,
        sample: data.length > 0 ? this.analyzeResponseSchema(data[0]) : null
      };
    }

    const schema: any = { type: 'object', fields: {} };
    for (const [key, value] of Object.entries(data)) {
      schema.fields[key] = typeof value;
    }
    return schema;
  }

  /**
   * Test all endpoints in a category
   */
  private async testCategory(categoryName: string): Promise<void> {
    console.log(`\n📦 Testing ${categoryName.toUpperCase()} APIs...`);

    const category = this.inventory.categories[categoryName];
    if (!category) {
      console.error(`Category ${categoryName} not found`);
      return;
    }

    let completed = 0;
    const total = category.endpoints.length;

    for (const endpoint of category.endpoints) {
      const result = await this.testEndpoint(
        categoryName,
        endpoint,
        category.base_path
      );

      this.results.push(result);
      completed++;

      // Progress indicator
      const statusSymbol = result.status === 'PASS' ? '✅' :
                          result.status === 'FAIL' ? '❌' : '⚠️';
      console.log(
        `  ${statusSymbol} [${completed}/${total}] ${endpoint.method} ${endpoint.path} ` +
        `(${result.response_time}ms) - ${result.status}`
      );
    }
  }

  /**
   * Generate category summary
   */
  private getCategorySummary(categoryName: string): CategorySummary {
    const categoryResults = this.results.filter(r => r.category === categoryName);

    const passed = categoryResults.filter(r => r.status === 'PASS').length;
    const failed = categoryResults.filter(r => r.status === 'FAIL').length;
    const errors = categoryResults.filter(r => r.status === 'ERROR').length;

    const responseTimes = categoryResults
      .filter(r => r.response_time !== undefined)
      .map(r => r.response_time!);

    const avgResponseTime = responseTimes.length > 0
      ? responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length
      : 0;

    return {
      category: categoryName,
      total: categoryResults.length,
      passed,
      failed,
      errors,
      avg_response_time: Math.round(avgResponseTime)
    };
  }

  /**
   * Generate comprehensive markdown report
   */
  private generateMarkdownReport(): string {
    const totalTests = this.results.length;
    const totalPassed = this.results.filter(r => r.status === 'PASS').length;
    const totalFailed = this.results.filter(r => r.status === 'FAIL').length;
    const totalErrors = this.results.filter(r => r.status === 'ERROR').length;

    const passRate = ((totalPassed / totalTests) * 100).toFixed(2);

    let report = `# Complete API Test Results\n\n`;
    report += `**Test Date**: ${new Date().toISOString()}\n`;
    report += `**Base URL**: ${this.baseUrl}\n`;
    report += `**Total APIs Tested**: ${totalTests}\n\n`;

    // Overall Summary
    report += `## Overall Summary\n\n`;
    report += `| Metric | Count | Percentage |\n`;
    report += `|--------|-------|------------|\n`;
    report += `| ✅ Passed | ${totalPassed} | ${passRate}% |\n`;
    report += `| ❌ Failed | ${totalFailed} | ${((totalFailed/totalTests)*100).toFixed(2)}% |\n`;
    report += `| ⚠️ Errors | ${totalErrors} | ${((totalErrors/totalTests)*100).toFixed(2)}% |\n\n`;

    // Category Summaries
    report += `## Category Summaries\n\n`;
    report += `| Category | Total | Passed | Failed | Errors | Avg Response Time |\n`;
    report += `|----------|-------|--------|--------|--------|-------------------|\n`;

    for (const categoryName of Object.keys(this.inventory.categories)) {
      const summary = this.getCategorySummary(categoryName);
      report += `| ${categoryName} | ${summary.total} | ${summary.passed} | `;
      report += `${summary.failed} | ${summary.errors} | ${summary.avg_response_time}ms |\n`;
    }

    // Detailed Results by Category
    report += `\n## Detailed Results\n\n`;

    for (const categoryName of Object.keys(this.inventory.categories)) {
      const categoryResults = this.results.filter(r => r.category === categoryName);

      report += `### ${categoryName.toUpperCase()} APIs\n\n`;
      report += `| Endpoint | Method | Status | HTTP | Response Time | Error |\n`;
      report += `|----------|--------|--------|------|---------------|-------|\n`;

      for (const result of categoryResults) {
        const statusSymbol = result.status === 'PASS' ? '✅' :
                            result.status === 'FAIL' ? '❌' : '⚠️';
        const httpStatus = result.http_status || 'N/A';
        const responseTime = result.response_time ? `${result.response_time}ms` : 'N/A';
        const error = result.error ? result.error.substring(0, 50) : '-';

        report += `| ${result.endpoint} | ${result.method} | ${statusSymbol} ${result.status} | `;
        report += `${httpStatus} | ${responseTime} | ${error} |\n`;
      }
      report += `\n`;
    }

    // Failed Tests Details
    const failedTests = this.results.filter(r => r.status !== 'PASS');
    if (failedTests.length > 0) {
      report += `## Failed/Error Tests Details\n\n`;

      for (const result of failedTests) {
        report += `### ${result.category} - ${result.method} ${result.endpoint}\n\n`;
        report += `- **Status**: ${result.status}\n`;
        report += `- **HTTP Status**: ${result.http_status || 'N/A'}\n`;
        report += `- **Response Time**: ${result.response_time || 'N/A'}ms\n`;
        report += `- **URL**: ${result.url}\n`;
        if (result.error) {
          report += `- **Error**: ${result.error}\n`;
        }
        report += `\n`;
      }
    }

    // Recommendations
    report += `## Recommendations\n\n`;

    if (totalFailed > 0) {
      report += `1. **Fix Failed Tests (${totalFailed})**: Review client errors (4xx) and fix request formats\n`;
    }

    if (totalErrors > 0) {
      report += `2. **Fix Error Tests (${totalErrors})**: Investigate server errors (5xx) and connection issues\n`;
    }

    if (totalPassed === totalTests) {
      report += `✅ **All tests passed!** The API is fully functional.\n`;
    }

    return report;
  }

  /**
   * Save results to files
   */
  private saveResults(): void {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

    // Save JSON results
    const jsonPath = path.join(this.outputDir, `results-${timestamp}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(this.results, null, 2));
    console.log(`\n💾 JSON results saved to: ${jsonPath}`);

    // Save Markdown report
    const mdPath = path.join(this.outputDir, `COMPLETE_API_TEST_RESULTS.md`);
    const report = this.generateMarkdownReport();
    fs.writeFileSync(mdPath, report);
    console.log(`📄 Markdown report saved to: ${mdPath}`);

    // Save CSV for analysis
    const csvPath = path.join(this.outputDir, `results-${timestamp}.csv`);
    const csvHeader = 'Category,Endpoint,Method,URL,Status,HTTP Status,Response Time,Error\n';
    const csvRows = this.results.map(r =>
      `${r.category},${r.endpoint},${r.method},${r.url},${r.status},` +
      `${r.http_status || ''},${r.response_time || ''},"${r.error || ''}"`
    ).join('\n');
    fs.writeFileSync(csvPath, csvHeader + csvRows);
    console.log(`📊 CSV results saved to: ${csvPath}`);
  }

  /**
   * Run all tests
   */
  public async runAllTests(): Promise<void> {
    console.log('🚀 Starting Comprehensive API Testing...');
    console.log(`📍 Base URL: ${this.baseUrl}`);
    console.log(`📋 Total APIs to test: ${this.inventory.total_apis}\n`);

    const startTime = Date.now();

    // Test each category
    for (const categoryName of Object.keys(this.inventory.categories)) {
      await this.testCategory(categoryName);
    }

    const totalTime = Date.now() - startTime;

    // Print summary
    console.log('\n' + '='.repeat(60));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(60));

    const totalTests = this.results.length;
    const totalPassed = this.results.filter(r => r.status === 'PASS').length;
    const totalFailed = this.results.filter(r => r.status === 'FAIL').length;
    const totalErrors = this.results.filter(r => r.status === 'ERROR').length;

    console.log(`Total Tests: ${totalTests}`);
    console.log(`✅ Passed: ${totalPassed} (${((totalPassed/totalTests)*100).toFixed(2)}%)`);
    console.log(`❌ Failed: ${totalFailed} (${((totalFailed/totalTests)*100).toFixed(2)}%)`);
    console.log(`⚠️ Errors: ${totalErrors} (${((totalErrors/totalTests)*100).toFixed(2)}%)`);
    console.log(`⏱️ Total Time: ${(totalTime/1000).toFixed(2)}s`);
    console.log('='.repeat(60));

    // Save results
    this.saveResults();

    console.log('\n✅ Testing complete!');
  }

  /**
   * Test specific category
   */
  public async testCategoryOnly(categoryName: string): Promise<void> {
    if (!this.inventory.categories[categoryName]) {
      console.error(`Category ${categoryName} not found`);
      return;
    }

    console.log(`🚀 Testing ${categoryName.toUpperCase()} APIs only...\n`);
    await this.testCategory(categoryName);
    this.saveResults();
    console.log('\n✅ Testing complete!');
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const baseUrl = process.env.API_BASE_URL || 'http://localhost:3000';

  const tester = new ComprehensiveAPITester(baseUrl);

  if (args.length === 0) {
    // Test all APIs
    await tester.runAllTests();
  } else {
    // Test specific category
    const category = args[0];
    await tester.testCategoryOnly(category);
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { ComprehensiveAPITester };
