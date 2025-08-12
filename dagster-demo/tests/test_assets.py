def test_definitions_load():
    """Test that Dagster definitions can be loaded without errors."""
    # This test ensures that our definitions module can be imported
    # and the definitions object is properly constructed
    from dagster_demo.definitions import defs
    
    assert defs is not None
    # Basic test that the definitions object exists and is a LazyDefinitions object
    assert "LazyDefinitions" in str(type(defs))


def test_basic_import():
    """Test that basic imports work correctly."""
    # Test that we can import our main modules without errors
    import dagster_demo.definitions
    import dagster_demo.defs.assets.dbt
    
    # If we get here without ImportError, the test passes
    assert True
