import { NextRequest, NextResponse } from 'next/server';
import { neo4jEnhanced } from '@/lib/neo4j-enhanced';

// GET /api/tags - List all tags (with optional category filter)
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const category = searchParams.get('category');

    let tags;
    if (category) {
      tags = await neo4jEnhanced.getTagsByCategory(category);
    } else {
      tags = await neo4jEnhanced.getAllTags();
    }

    return NextResponse.json({
      success: true,
      data: tags,
      count: tags.length
    });
  } catch (error) {
    console.error('Error fetching tags:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch tags',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// POST /api/tags - Create new tag
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { name, category, color, description } = body;

    // Validation
    if (!name || !category || !color) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          message: 'name, category, and color are required fields'
        },
        { status: 400 }
      );
    }

    const tag = await neo4jEnhanced.createTag({
      name: name.trim(),
      category: category.trim(),
      color: color.trim(),
      description: description?.trim()
    });

    return NextResponse.json({
      success: true,
      data: tag,
      message: 'Tag created successfully'
    }, { status: 201 });
  } catch (error) {
    console.error('Error creating tag:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to create tag',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

// DELETE /api/tags - Bulk delete tags
export async function DELETE(request: NextRequest) {
  try {
    const body = await request.json();
    const { tagNames } = body;

    if (!Array.isArray(tagNames) || tagNames.length === 0) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          message: 'tagNames array is required and must not be empty'
        },
        { status: 400 }
      );
    }

    const results = await Promise.allSettled(
      tagNames.map(name => neo4jEnhanced.deleteTag(name))
    );

    const deletedCount = results.filter(r => r.status === 'fulfilled' && r.value).length;
    const failedCount = results.filter(r => r.status === 'rejected').length;

    return NextResponse.json({
      success: true,
      data: {
        deleted: deletedCount,
        failed: failedCount,
        total: tagNames.length
      },
      message: `Successfully deleted ${deletedCount} of ${tagNames.length} tags`
    });
  } catch (error) {
    console.error('Error deleting tags:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to delete tags',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
