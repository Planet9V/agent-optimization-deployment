import { NextRequest, NextResponse } from 'next/server';
import { neo4jEnhanced } from '@/lib/neo4j-enhanced';

// GET /api/tags/[id] - Get tag details with usage count
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const tagName = decodeURIComponent(id);
    const tag = await neo4jEnhanced.getTag(tagName);

    if (!tag) {
      return NextResponse.json(
        {
          success: false,
          error: 'Not found',
          message: `Tag '${tagName}' not found`
        },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: tag
    });
  } catch (error) {
    console.error('Error fetching tag:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch tag',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// PUT /api/tags/[id] - Update tag
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const tagName = decodeURIComponent(id);
    const body = await request.json();
    const { category, color, description } = body;

    // Check if tag exists
    const existingTag = await neo4jEnhanced.getTag(tagName);
    if (!existingTag) {
      return NextResponse.json(
        {
          success: false,
          error: 'Not found',
          message: `Tag '${tagName}' not found`
        },
        { status: 404 }
      );
    }

    // Update tag (create with same name updates properties)
    const updatedTag = await neo4jEnhanced.createTag({
      name: tagName,
      category: category?.trim() || existingTag.category,
      color: color?.trim() || existingTag.color,
      description: description !== undefined ? description?.trim() : existingTag.description
    });

    return NextResponse.json({
      success: true,
      data: updatedTag,
      message: 'Tag updated successfully'
    });
  } catch (error) {
    console.error('Error updating tag:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to update tag',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// DELETE /api/tags/[id] - Delete tag
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const tagName = decodeURIComponent(id);
    const deleted = await neo4jEnhanced.deleteTag(tagName);

    if (!deleted) {
      return NextResponse.json(
        {
          success: false,
          error: 'Not found',
          message: `Tag '${tagName}' not found or could not be deleted`
        },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      message: `Tag '${tagName}' deleted successfully`
    });
  } catch (error) {
    console.error('Error deleting tag:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to delete tag',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
