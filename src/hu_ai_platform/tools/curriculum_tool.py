"""Curriculum lookup tool — provides program and course information."""

from typing import TypedDict


class ProgramInfo(TypedDict):
    """Type for program information entries."""

    name: str
    ects: int
    duration: str
    courses: list[str]
    prerequisites: str


# Static curriculum data for demo purposes
# (would connect to a student information system in production)
PROGRAMS: dict[str, ProgramInfo] = {
    "applied-ai-minor": {
        "name": "Applied Artificial Intelligence Minor",
        "ects": 30,
        "duration": "1 semester",
        "courses": [
            "Machine Learning Fundamentals (5 ECTS)",
            "Natural Language Processing (5 ECTS)",
            "Ethics and Responsible AI (5 ECTS)",
            "Computer Vision (5 ECTS)",
            "AI Project (10 ECTS)",
        ],
        "prerequisites": "90+ ECTS completed, basic Python, intro math/stats",
    },
    "software-engineering": {
        "name": "Bachelor Software Engineering",
        "ects": 240,
        "duration": "4 years",
        "courses": [
            "Programming Fundamentals",
            "Data Structures and Algorithms",
            "Web Development",
            "Database Systems",
            "Software Architecture",
            "DevOps and CI/CD",
            "Graduation Project",
        ],
        "prerequisites": "HAVO/VWO diploma or MBO-4",
    },
}


def lookup_program(program_id: str) -> str:
    """Look up details for a specific program.

    This function is designed to be wrapped as an Agno tool.
    """
    program = PROGRAMS.get(program_id)
    if not program:
        available = ", ".join(PROGRAMS.keys())
        return f"Program '{program_id}' not found. Available programs: {available}"

    courses = "\n".join(f"  - {c}" for c in program["courses"])
    return (
        f"**{program['name']}**\n"
        f"- ECTS: {program['ects']}\n"
        f"- Duration: {program['duration']}\n"
        f"- Prerequisites: {program['prerequisites']}\n"
        f"- Courses:\n{courses}"
    )


def list_programs() -> str:
    """List all available programs."""
    lines = []
    for pid, prog in PROGRAMS.items():
        lines.append(f"- **{prog['name']}** (`{pid}`) — {prog['ects']} ECTS, {prog['duration']}")
    return "\n".join(lines)
