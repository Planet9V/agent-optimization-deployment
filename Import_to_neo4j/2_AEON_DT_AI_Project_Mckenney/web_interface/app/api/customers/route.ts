import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';
import { z } from 'zod';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USERNAME || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

const customerSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email().optional().or(z.literal('')),
  phone: z.string().optional(),
  company: z.string().optional(),
  address: z.string().optional(),
  notes: z.string().optional(),
});

export async function GET(request: NextRequest) {
  const session = driver.session();

  try {
    const result = await session.run(
      `
      MATCH (c:Customer)
      OPTIONAL MATCH (c)-[:OWNS]->(d:Document)
      WITH c, COUNT(d) as documentCount
      RETURN c {
        .*,
        id: elementId(c),
        documentCount: documentCount
      } as customer
      ORDER BY c.name ASC
      `
    );

    const customers = result.records.map((record) => record.get('customer'));

    return NextResponse.json({
      success: true,
      customers,
      count: customers.length,
    });
  } catch (error) {
    console.error('Error fetching customers:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch customers',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}

export async function POST(request: NextRequest) {
  const session = driver.session();

  try {
    const body = await request.json();

    // Validate input
    const validatedData = customerSchema.parse(body);

    // Clean up empty optional fields
    const customerData: Record<string, any> = {
      name: validatedData.name,
      createdAt: new Date().toISOString(),
    };

    if (validatedData.email) customerData.email = validatedData.email;
    if (validatedData.phone) customerData.phone = validatedData.phone;
    if (validatedData.company) customerData.company = validatedData.company;
    if (validatedData.address) customerData.address = validatedData.address;
    if (validatedData.notes) customerData.notes = validatedData.notes;

    // Create customer in Neo4j
    const result = await session.run(
      `
      CREATE (c:Customer $properties)
      RETURN c {
        .*,
        id: elementId(c)
      } as customer
      `,
      { properties: customerData }
    );

    const customer = result.records[0].get('customer');

    return NextResponse.json(
      {
        success: true,
        customer,
        message: 'Customer created successfully',
      },
      { status: 201 }
    );
  } catch (error) {
    console.error('Error creating customer:', error);

    if (error instanceof z.ZodError) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          details: (error as any).errors || error.issues,
        },
        { status: 400 }
      );
    }

    return NextResponse.json(
      {
        success: false,
        error: 'Failed to create customer',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}
