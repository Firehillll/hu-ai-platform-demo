"""Tests for tool components."""

from hu_ai_platform.tools.curriculum_tool import list_programs, lookup_program


class TestCurriculumTool:
    def test_lookup_existing_program(self) -> None:
        result = lookup_program("applied-ai-minor")
        assert "Applied Artificial Intelligence" in result
        assert "30" in result

    def test_lookup_nonexistent_program(self) -> None:
        result = lookup_program("nonexistent")
        assert "not found" in result

    def test_list_programs(self) -> None:
        result = list_programs()
        assert "applied-ai-minor" in result
        assert "software-engineering" in result
