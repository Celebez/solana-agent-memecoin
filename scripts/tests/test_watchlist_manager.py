"""Test watchlist_manager.py — CRUD operations."""
import sys, os, json
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use temp file for tests
import watchlist_manager

TEST_MINT = "TestMint1111111111111111111111111111111111"


def setup_module(module):
    """Redirect watchlist file ke temp."""
    watchlist_manager.WATCHLIST_FILE = Path(tempfile.mktemp(suffix=".json"))


def teardown_module(module):
    """Cleanup."""
    if watchlist_manager.WATCHLIST_FILE.exists():
        watchlist_manager.WATCHLIST_FILE.unlink()


def test_add_new_item():
    """Add token to empty watchlist."""
    item = watchlist_manager.add_item(TEST_MINT, label="TestToken", note="Sample note")
    assert item is not None
    assert item["mint"] == TEST_MINT
    assert item["label"] == "TestToken"
    assert item["note"] == "Sample note"
    assert "added_at" in item


def test_add_duplicate_prevented():
    """Duplicate add returns None."""
    watchlist_manager.add_item(TEST_MINT)
    result = watchlist_manager.add_item(TEST_MINT)
    assert result is None


def test_list_items(capsys):
    """List displays all items."""
    watchlist_manager.list_items()
    captured = capsys.readouterr()
    assert "TestToken" in captured.out
    assert TEST_MINT[:12] in captured.out


def test_update_item():
    """Update modifies existing item."""
    result = watchlist_manager.update_item(TEST_MINT, label="UpdatedLabel", above=0.001)
    assert result is True
    items = watchlist_manager.load_watchlist()
    assert items[0]["label"] == "UpdatedLabel"
    assert items[0]["alerts"]["above"] == 0.001


def test_remove_item():
    """Remove deletes item."""
    result = watchlist_manager.remove_item(TEST_MINT)
    assert result is True
    items = watchlist_manager.load_watchlist()
    assert len(items) == 0


def test_remove_nonexistent():
    """Remove returns False if not found."""
    result = watchlist_manager.remove_item("NonExistentMint111111111111111111111")
    assert result is False
