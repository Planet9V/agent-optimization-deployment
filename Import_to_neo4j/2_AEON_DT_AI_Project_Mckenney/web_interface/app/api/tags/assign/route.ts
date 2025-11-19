import { NextRequest, NextResponse } from 'next/server';
import { neo4jEnhanced } from '@/lib/neo4j-enhanced';

// POST /api/tags/assign - Assign multiple tags to document/entity
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { documentId, tagNames, taggedBy } = body;

    // Validation
    if (!documentId || !tagNames) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          message: 'documentId and tagNames are required fields'
        },
        { status: 400 }
      );
    }

    if (!Array.isArray(tagNames) || tagNames.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          message: 'tagNames must be a non-empty array'
        },
        { status: 400 }
      );
    }

    // Assign tags to document - creates HAS_TAG relationships in Neo4j
    await neo4jEnhanced.assignTagsToDocument(
      documentId,
      tagNames,
      taggedBy || 'system'
    );

    // Fetch updated tags for the document
    const updatedTags = await neo4jEnhanced.getDocumentTags(documentId);

    return NextResponse.json({
      success: true,
      data: {
        documentId,
        assignedTags: tagNames,
        allTags: updatedTags
      },
      message: `Successfully assigned ${tagNames.length} tag(s) to document`
    }, { status: 200 });
  } catch (error) {
    console.error('Error assigning tags:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to assign tags',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// DELETE /api/tags/assign - Remove tags from document
export async function DELETE(request: NextRequest) {
  try {
    const body = await request.json();
    const { documentId, tagNames } = body;

    // Validation
    if (!documentId || !tagNames) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          message: 'documentId and tagNames are required fields'
        },
        { status: 400 }
      );
    }

    if (!Array.isArray(tagNames) || tagNames.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          message: 'tagNames must be a non-empty array'
        },
        { status: 400 }
      );
    }

    // Remove tags from document
    await neo4jEnhanced.removeTagsFromDocument(documentId, tagNames);

    // Fetch remaining tags for the document
    const remainingTags = await neo4jEnhanced.getDocumentTags(documentId);

    return NextResponse.json({
      success: true,
      data: {
        documentId,
        removedTags: tagNames,
        remainingTags
      },
      message: `Successfully removed ${tagNames.length} tag(s) from document`
    });
  } catch (error) {
    console.error('Error removing tags:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to remove tags',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
