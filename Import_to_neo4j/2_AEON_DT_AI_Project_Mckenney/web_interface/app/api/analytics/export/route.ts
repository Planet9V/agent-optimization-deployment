import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USERNAME || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

function calculateStartDate(timeRange: string): Date {
  const endDate = new Date();
  const startDate = new Date();

  switch (timeRange) {
    case '7d':
      startDate.setDate(endDate.getDate() - 7);
      break;
    case '30d':
      startDate.setDate(endDate.getDate() - 30);
      break;
    case '90d':
      startDate.setDate(endDate.getDate() - 90);
      break;
    default:
      startDate.setDate(endDate.getDate() - 30);
  }

  return startDate;
}

async function fetchAnalyticsData(timeRange: string, customerId: string | null) {
  const session = driver.session();

  try {
    const startDate = calculateStartDate(timeRange);
    const startDateStr = startDate.toISOString();

    const query = `
      MATCH (d:Document)
      WHERE datetime(d.createdAt) >= datetime($startDate)
      ${customerId ? 'AND d.customerId = $customerId' : ''}
      OPTIONAL MATCH (d)<-[:OWNS]-(c:Customer)
      OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
      OPTIONAL MATCH (d)-[:CONTAINS|MENTIONS]->(e)
      WHERE e:Entity OR e:Person OR e:Organization OR e:Location OR e:Technology
      WITH d, c,
           collect(DISTINCT t.name) as tags,
           count(DISTINCT e) as entityCount,
           collect(DISTINCT labels(e)[0]) as entityTypes
      RETURN d.id as documentId,
             d.title as title,
             d.type as type,
             d.createdAt as createdAt,
             d.processingStatus as processingStatus,
             d.qualityScore as qualityScore,
             c.name as customerName,
             c.id as customerId,
             tags,
             entityCount,
             entityTypes
      ORDER BY d.createdAt DESC
    `;

    const result = await session.run(query, {
      startDate: startDateStr,
      customerId,
    });

    return result.records.map(record => ({
      documentId: record.get('documentId'),
      title: record.get('title'),
      type: record.get('type'),
      createdAt: record.get('createdAt'),
      processingStatus: record.get('processingStatus') || 'pending',
      qualityScore: record.get('qualityScore') || 0,
      customerName: record.get('customerName'),
      customerId: record.get('customerId'),
      tags: record.get('tags') || [],
      entityCount: record.get('entityCount').toNumber(),
      entityTypes: record.get('entityTypes') || [],
    }));
  } finally {
    await session.close();
  }
}

function convertToCSV(data: Record<string, unknown>[]): string {
  if (data.length === 0) return '';

  const headers = Object.keys(data[0]);
  const csvRows = [headers.join(',')];

  for (const row of data) {
    const values = headers.map(header => {
      const value = row[header];
      if (Array.isArray(value)) {
        return `"${value.join('; ')}"`;
      }
      if (typeof value === 'string' && value.includes(',')) {
        return `"${value}"`;
      }
      return value || '';
    });
    csvRows.push(values.join(','));
  }

  return csvRows.join('\n');
}

function generatePDFContent(data: Record<string, unknown>[], timeRange: string, customerId: string | null): string {
  const now = new Date().toISOString();
  const customerFilter = customerId ? `Customer: ${customerId}` : 'All Customers';

  const content = `
AEON Digital Twin Analytics Report
Generated: ${now}
Time Range: ${timeRange}
${customerFilter}

Total Documents: ${data.length}

Document Details:
${data.map((doc, index) => `
${index + 1}. ${doc.title}
   - Type: ${doc.type}
   - Created: ${doc.createdAt}
   - Status: ${doc.processingStatus}
   - Quality Score: ${doc.qualityScore}
   - Customer: ${doc.customerName}
   - Entities: ${doc.entityCount}
   - Tags: ${Array.isArray(doc.tags) ? (doc.tags as string[]).join(', ') : 'None'}
`).join('\n')}
`;

  return content;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { format, timeRange = '30d', customerId = null } = body;

    if (!['csv', 'json', 'pdf'].includes(format)) {
      return NextResponse.json(
        { error: 'Invalid format. Must be csv, json, or pdf' },
        { status: 400 }
      );
    }

    const data = await fetchAnalyticsData(timeRange, customerId);

    switch (format) {
      case 'csv': {
        const csv = convertToCSV(data);
        return new NextResponse(csv, {
          headers: {
            'Content-Type': 'text/csv',
            'Content-Disposition': `attachment; filename="analytics-${timeRange}-${Date.now()}.csv"`,
          },
        });
      }

      case 'json': {
        const json = JSON.stringify(data, null, 2);
        return new NextResponse(json, {
          headers: {
            'Content-Type': 'application/json',
            'Content-Disposition': `attachment; filename="analytics-${timeRange}-${Date.now()}.json"`,
          },
        });
      }

      case 'pdf': {
        // For now, return plain text. In production, use a PDF library like pdfkit or puppeteer
        const pdfContent = generatePDFContent(data, timeRange, customerId);
        return new NextResponse(pdfContent, {
          headers: {
            'Content-Type': 'text/plain',
            'Content-Disposition': `attachment; filename="analytics-${timeRange}-${Date.now()}.txt"`,
          },
        });
      }

      default:
        return NextResponse.json(
          { error: 'Unsupported format' },
          { status: 400 }
        );
    }
  } catch (error) {
    console.error('Error exporting analytics:', error);
    return NextResponse.json(
      { error: 'Failed to export analytics data' },
      { status: 500 }
    );
  }
}
