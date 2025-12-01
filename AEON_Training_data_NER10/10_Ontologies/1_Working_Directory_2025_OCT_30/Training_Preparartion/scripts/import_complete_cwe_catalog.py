#!/usr/bin/env python3
"""
Import Complete CWE Catalog v4.18
Fixes NULL ID issues and imports all missing CWE definitions
"""

import xml.etree.ElementTree as ET
import sqlite3
from pathlib import Path
import re
from datetime import datetime

# Database path
DB_PATH = Path(__file__).parent.parent / "data" / "training_data.db"
XML_PATH = Path(__file__).parent.parent / "cwec_v4.18.xml"

def extract_cwe_id(text):
    """Extract CWE number from text like 'CWE-79' or 'SQL Injection (CWE-89)'"""
    if not text:
        return None
    match = re.search(r'CWE-(\d+)', text, re.IGNORECASE)
    return match.group(1) if match else None

def parse_cwe_xml(xml_path):
    """Parse CWE XML and extract all weakness definitions"""
    print(f"Parsing CWE XML from: {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Namespace handling
    ns = {'cwe': 'http://cwe.mitre.org/cwe-7'}

    cwes = []

    # Parse Weaknesses
    for weakness in root.findall('.//cwe:Weakness', ns):
        cwe_id = weakness.get('ID')
        name = weakness.get('Name')
        abstraction = weakness.get('Abstraction')

        # Get description
        desc_elem = weakness.find('.//cwe:Description', ns)
        description = desc_elem.text if desc_elem is not None else ""

        # Get extended description if available
        ext_desc_elem = weakness.find('.//cwe:Extended_Description', ns)
        if ext_desc_elem is not None and ext_desc_elem.text:
            description += "\n\n" + ext_desc_elem.text

        cwes.append({
            'cwe_id': cwe_id,
            'name': name,
            'description': description.strip() if description else "",
            'abstraction': abstraction or 'Base',
            'type': 'Weakness'
        })

    # Parse Categories
    for category in root.findall('.//cwe:Category', ns):
        cwe_id = category.get('ID')
        name = category.get('Name')

        # Get summary
        summary_elem = category.find('.//cwe:Summary', ns)
        description = summary_elem.text if summary_elem is not None else ""

        cwes.append({
            'cwe_id': cwe_id,
            'name': name,
            'description': description.strip() if description else "",
            'abstraction': 'Category',
            'type': 'Category'
        })

    # Parse Views
    for view in root.findall('.//cwe:View', ns):
        cwe_id = view.get('ID')
        name = view.get('Name')

        # Get objective
        obj_elem = view.find('.//cwe:Objective', ns)
        description = obj_elem.text if obj_elem is not None else ""

        cwes.append({
            'cwe_id': cwe_id,
            'name': name,
            'description': description.strip() if description else "",
            'abstraction': 'View',
            'type': 'View'
        })

    print(f"Parsed {len(cwes)} CWE entries from XML")
    return cwes

def fix_null_ids(conn):
    """Fix CWE nodes with NULL IDs by extracting from name field"""
    cursor = conn.cursor()

    # Find nodes with NULL IDs that have CWE in the name
    cursor.execute("""
        SELECT id, name
        FROM cwe_nodes
        WHERE cwe_id IS NULL
        AND (name LIKE '%CWE-%' OR name LIKE '%cwe-%')
    """)

    null_nodes = cursor.fetchall()
    print(f"Found {len(null_nodes)} nodes with NULL IDs containing 'CWE-' in name")

    fixed_count = 0
    for node_id, name in null_nodes:
        cwe_num = extract_cwe_id(name)
        if cwe_num:
            cursor.execute("""
                UPDATE cwe_nodes
                SET cwe_id = ?
                WHERE id = ?
            """, (cwe_num, node_id))
            fixed_count += 1

    conn.commit()
    print(f"Fixed {fixed_count} nodes by extracting CWE ID from name")

    return fixed_count

def import_cwe_catalog(conn, cwes):
    """Import all CWE definitions from parsed XML"""
    cursor = conn.cursor()

    # Track statistics
    inserted = 0
    updated = 0
    skipped = 0

    for cwe in cwes:
        cwe_id = cwe['cwe_id']
        name = cwe['name']
        description = cwe['description']
        abstraction = cwe['abstraction']
        cwe_type = cwe['type']

        # Check if CWE already exists
        cursor.execute("""
            SELECT id, name, description
            FROM cwe_nodes
            WHERE cwe_id = ?
        """, (cwe_id,))

        existing = cursor.fetchone()

        if existing:
            # Update if description is empty or significantly different
            existing_id, existing_name, existing_desc = existing

            if not existing_desc or len(description) > len(existing_desc or ""):
                cursor.execute("""
                    UPDATE cwe_nodes
                    SET name = ?,
                        description = ?,
                        abstraction_level = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (name, description, abstraction, datetime.now().isoformat(), existing_id))
                updated += 1
            else:
                skipped += 1
        else:
            # Insert new CWE
            cursor.execute("""
                INSERT INTO cwe_nodes (cwe_id, name, description, abstraction_level, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (cwe_id, name, description, abstraction, datetime.now().isoformat()))
            inserted += 1

    conn.commit()

    print(f"\nImport Results:")
    print(f"  Inserted: {inserted} new CWEs")
    print(f"  Updated: {updated} existing CWEs")
    print(f"  Skipped: {skipped} (already complete)")

    return inserted, updated, skipped

def verify_critical_cwes(conn):
    """Verify all 8 critical CWEs exist"""
    critical_cwes = ['327', '125', '120', '20', '119', '434', '290', '522']

    cursor = conn.cursor()
    missing = []

    for cwe_id in critical_cwes:
        cursor.execute("SELECT name FROM cwe_nodes WHERE cwe_id = ?", (cwe_id,))
        result = cursor.fetchone()

        if result:
            print(f"✓ CWE-{cwe_id}: {result[0]}")
        else:
            print(f"✗ CWE-{cwe_id}: MISSING")
            missing.append(cwe_id)

    return missing

def validate_database(conn):
    """Validate database state after import"""
    cursor = conn.cursor()

    # Count total CWEs
    cursor.execute("SELECT COUNT(*) FROM cwe_nodes")
    total = cursor.fetchone()[0]

    # Count NULL IDs
    cursor.execute("SELECT COUNT(*) FROM cwe_nodes WHERE cwe_id IS NULL")
    null_ids = cursor.fetchone()[0]

    # Count by abstraction level
    cursor.execute("""
        SELECT abstraction_level, COUNT(*)
        FROM cwe_nodes
        GROUP BY abstraction_level
    """)
    abstractions = cursor.fetchall()

    print(f"\n{'='*60}")
    print("DATABASE VALIDATION RESULTS")
    print(f"{'='*60}")
    print(f"Total CWE nodes: {total:,}")
    print(f"NULL IDs remaining: {null_ids:,} ({null_ids/total*100:.1f}%)")
    print(f"\nAbstraction Levels:")
    for level, count in abstractions:
        print(f"  {level or 'NULL'}: {count:,}")

    return total, null_ids

def main():
    print("="*60)
    print("CWE CATALOG IMPORT - v4.18")
    print("="*60)
    print(f"Start time: {datetime.now().isoformat()}")
    print()

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    try:
        # Step 1: Fix NULL IDs
        print("\n[STEP 1] Fixing NULL IDs...")
        fixed = fix_null_ids(conn)

        # Step 2: Parse CWE XML
        print("\n[STEP 2] Parsing CWE XML catalog...")
        cwes = parse_cwe_xml(XML_PATH)

        # Step 3: Import CWE catalog
        print("\n[STEP 3] Importing CWE definitions...")
        inserted, updated, skipped = import_cwe_catalog(conn, cwes)

        # Step 4: Verify critical CWEs
        print("\n[STEP 4] Verifying critical CWEs...")
        missing = verify_critical_cwes(conn)

        if missing:
            print(f"\n⚠ WARNING: {len(missing)} critical CWEs still missing!")
        else:
            print("\n✓ All 8 critical CWEs verified!")

        # Step 5: Validate database
        print("\n[STEP 5] Validating database...")
        total, null_ids = validate_database(conn)

        # Final summary
        print(f"\n{'='*60}")
        print("IMPORT COMPLETE")
        print(f"{'='*60}")
        print(f"End time: {datetime.now().isoformat()}")

        if null_ids == 0:
            print("\n✅ SUCCESS: All CWE nodes have proper IDs")
        else:
            print(f"\n⚠ WARNING: {null_ids} nodes still have NULL IDs")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
