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

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = driver.session();

  try {
    const { id } = await params;

    // Fetch customer details
    const customerResult = await session.run(
      `
      MATCH (c:Customer)
      WHERE elementId(c) = $id
      RETURN c {
        .*,
        id: elementId(c)
      } as customer
      `,
      { id }
    );

    if (customerResult.records.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: 'Customer not found',
        },
        { status: 404 }
      );
    }

    const customer = customerResult.records[0].get('customer');

    // Fetch associated documents
    const documentsResult = await session.run(
      `
      MATCH (c:Customer)-[:OWNS]->(d:Document)
      WHERE elementId(c) = $id
      RETURN d {
        .*,
        id: elementId(d)
      } as document
      ORDER BY d.uploadDate DESC
      `,
      { id }
    );

    const documents = documentsResult.records.map((record) =>
      record.get('document')
    );

    return NextResponse.json({
      success: true,
      customer,
      documents,
    });
  } catch (error) {
    console.error('Error fetching customer:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch customer',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = driver.session();

  try {
    const { id } = await params;
    const body = await request.json();

    // Validate input
    const validatedData = customerSchema.parse(body);

    // Clean up empty optional fields
    const updateData: Record<string, any> = {
      name: validatedData.name,
      updatedAt: new Date().toISOString(),
    };

    if (validatedData.email) updateData.email = validatedData.email;
    if (validatedData.phone) updateData.phone = validatedData.phone;
    if (validatedData.company) updateData.company = validatedData.company;
    if (validatedData.address) updateData.address = validatedData.address;
    if (validatedData.notes) updateData.notes = validatedData.notes;

    // Update customer in Neo4j
    const result = await session.run(
      `
      MATCH (c:Customer)
      WHERE elementId(c) = $id
      SET c += $properties
      RETURN c {
        .*,
        id: elementId(c)
      } as customer
      `,
      { id, properties: updateData }
    );

    if (result.records.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: 'Customer not found',
        },
        { status: 404 }
      );
    }

    const customer = result.records[0].get('customer');

    return NextResponse.json({
      success: true,
      customer,
      message: 'Customer updated successfully',
    });
  } catch (error) {
    console.error('Error updating customer:', error);

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
        error: 'Failed to update customer',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = driver.session();

  try {
    const { id } = await params;

    // Check if customer has documents
    const checkResult = await session.run(
      `
      MATCH (c:Customer)-[:OWNS]->(d:Document)
      WHERE elementId(c) = $id
      RETURN COUNT(d) as documentCount
      `,
      { id }
    );

    const documentCount = checkResult.records[0].get('documentCount').toNumber();

    if (documentCount > 0) {
      return NextResponse.json(
        {
          success: false,
          error: 'Cannot delete customer with associated documents',
          details: `This customer has ${documentCount} document(s). Please remove or reassign them first.`,
        },
        { status: 400 }
      );
    }

    // Delete customer
    const deleteResult = await session.run(
      `
      MATCH (c:Customer)
      WHERE elementId(c) = $id
      DELETE c
      RETURN COUNT(c) as deletedCount
      `,
      { id }
    );

    const deletedCount = deleteResult.records[0].get('deletedCount').toNumber();

    if (deletedCount === 0) {
      return NextResponse.json(
        {
          success: false,
          error: 'Customer not found',
        },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Customer deleted successfully',
    });
  } catch (error) {
    console.error('Error deleting customer:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to delete customer',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}
