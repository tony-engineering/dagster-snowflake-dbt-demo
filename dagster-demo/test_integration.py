#!/usr/bin/env python3

"""
Test script for Dagster dbt integration
"""

import os
from pathlib import Path

def test_integration():
    print("🚀 Testing Dagster dbt Integration")
    print("=" * 50)
    
    # Test 1: Import definitions
    try:
        from dagster_demo.definitions import defs
        print("✅ Successfully imported Dagster definitions")
    except Exception as e:
        print(f"❌ Failed to import definitions: {e}")
        return False
    
    # Test 2: Check dbt project setup
    dbt_project_path = Path("../dbt_demo/dbt_project.yml")
    if dbt_project_path.exists():
        print("✅ dbt_project.yml found")
    else:
        print("❌ dbt_project.yml not found")
        return False
    
    # Test 3: Check manifest exists
    manifest_path = Path("../dbt_demo/target/manifest.json")
    if manifest_path.exists():
        print("✅ dbt manifest.json found")
    else:
        print("❌ dbt manifest.json not found - run 'dbt parse' first")
        return False
    
    # Test 4: Check if assets are loaded
    try:
        definitions = defs()
        # Get all asset keys from the definitions
        asset_keys = []
        for asset in definitions.assets:
            if hasattr(asset, 'keys'):
                # For assets with multiple keys
                asset_keys.extend(asset.keys)
            else:
                # For single assets
                asset_keys.append(asset.key)
        
        if asset_keys:
            print(f"✅ Found {len(asset_keys)} assets:")
            for key in asset_keys:
                print(f"   - {key}")
        else:
            print("⚠️ No assets found")
    except Exception as e:
        print(f"❌ Failed to load assets: {e}")
        return False
    
    print("=" * 50)
    print("🎉 Integration test completed successfully!")
    print("\n📌 Next steps:")
    print("1. Run 'dagster dev' in the dagster-demo directory")
    print("2. Open http://localhost:3000 in your browser")
    print("3. Navigate to the Assets tab to see your dbt models")
    print("4. Click 'Materialize all' to run your dbt models")
    
    return True

if __name__ == "__main__":
    success = test_integration()
    exit(0 if success else 1)
