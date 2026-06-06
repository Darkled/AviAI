import pytest
from app.core.security import validate_sql_query

def test_validate_sql_valid_select():
    """Test that a standard SELECT query is allowed."""
    query = "SELECT * FROM fleet"
    # Should not raise any exception
    validate_sql_query(query)

def test_validate_sql_valid_with():
    """Test that a query starting with WITH (CTE) is allowed."""
    query = "WITH cte AS (SELECT * FROM aircraft_models) SELECT * FROM cte"
    validate_sql_query(query)

def test_validate_sql_case_insensitive():
    """Test that validation is case-insensitive."""
    query = "select id from fleet"
    validate_sql_query(query)

def test_validate_sql_empty():
    """Test that empty queries are rejected."""
    with pytest.raises(ValueError, match="SQL query cannot be empty"):
        validate_sql_query("")
    with pytest.raises(ValueError, match="SQL query cannot be empty"):
        validate_sql_query("   ")

def test_validate_sql_not_select():
    """Test that non-SELECT/WITH queries are rejected."""
    with pytest.raises(ValueError, match="Only SELECT or WITH"):
        validate_sql_query("INSERT INTO fleet (name) VALUES ('test')")
    with pytest.raises(ValueError, match="Only SELECT or WITH"):
        validate_sql_query("UPDATE fleet SET name = 'test'")

def test_validate_sql_forbidden_keywords():
    """Test that forbidden keywords anywhere in the query are rejected."""
    # DROP in the middle
    with pytest.raises(ValueError, match="Forbidden keyword 'DROP'"):
        validate_sql_query("SELECT * FROM fleet; DROP TABLE fleet")
    
    # DELETE in the middle
    with pytest.raises(ValueError, match="Forbidden keyword 'DELETE'"):
        validate_sql_query("SELECT * FROM (DELETE FROM fleet)")

    # TRUNCATE
    with pytest.raises(ValueError, match="Forbidden keyword 'TRUNCATE'"):
        validate_sql_query("SELECT * FROM fleet -- TRUNCATE table")

def test_validate_sql_word_boundaries():
    """Test that we only match whole words for forbidden keywords."""
    # 'DROPLET' contains 'DROP' but should be allowed as a column name
    query = "SELECT droplet_id FROM fleet"
    validate_sql_query(query)

    # 'CREATED_AT' contains 'CREATE' but should be allowed
    query = "SELECT created_at FROM aircraft_models"
    validate_sql_query(query)
