#!/usr/bin/env python
"""
Script to count tests by marker (unit, integration, e2e) for testing pyramid.
"""
import subprocess
import sys
from pathlib import Path


def count_tests_by_marker(marker: str) -> int:
    """Count tests with a specific marker."""
    try:
        result = subprocess.run(
            ["pytest", "--collect-only", "-m", marker, "-q"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Extract the number from output like "18/103 tests collected"
        # or "18 tests collected"
        output = result.stdout.strip()

        # Look for pattern like "18/103 tests collected" or "18 tests collected"
        for line in output.split("\n"):
            if "test" in line.lower() and (
                "collected" in line.lower() or "selected" in line.lower()
            ):
                # Extract number before "/" or before "test"
                if "/" in line:
                    collected = line.split("/")[0].strip()
                    try:
                        return int(collected)
                    except ValueError:
                        continue
                elif "test" in line.lower():
                    # Pattern: "18 tests collected"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.lower() == "test" or part.lower() == "tests":
                            if i > 0 and parts[i - 1].isdigit():
                                return int(parts[i - 1])
        return 0
    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
        print(f"Error counting {marker} tests: {e}", file=sys.stderr)
        return 0


def main():
    """Main function to count and display test pyramid."""
    # Change to project root
    project_root = Path(__file__).parent.parent
    import os

    os.chdir(project_root)

    # Count tests by marker
    unit_count = count_tests_by_marker("unit")
    integration_count = count_tests_by_marker("integration")
    e2e_count = count_tests_by_marker("e2e")
    total = unit_count + integration_count + e2e_count

    # Display results
    print("\n" + "=" * 50)
    print("TESTING PYRAMID STATISTICS")
    print("=" * 50)

    if total > 0:
        print(f"\n📊 Unit Tests:        {unit_count:3d} ({unit_count/total*100:.1f}%)")
        print(
            f"🔗 Integration Tests: {integration_count:3d} ({integration_count/total*100:.1f}%)"
        )
        print(f"🌐 E2E Tests:         {e2e_count:3d} ({e2e_count/total*100:.1f}%)")
    else:
        print(f"\n📊 Unit Tests:        {unit_count:3d}")
        print(f"🔗 Integration Tests: {integration_count:3d}")
        print(f"🌐 E2E Tests:         {e2e_count:3d}")

    print(f"\n{'─' * 50}")
    print(f"📈 Total Tests:       {total:3d}")
    print("=" * 50 + "\n")

    # Visual pyramid
    if total > 0:
        max_width = 40
        unit_width = int((unit_count / total) * max_width)
        integration_width = int((integration_count / total) * max_width)
        e2e_width = int((e2e_count / total) * max_width)

        print("Visual Pyramid:")
        print(" " * (max_width - e2e_width) + "█" * e2e_width + f" E2E ({e2e_count})")
        print(
            " " * (max_width - integration_width)
            + "█" * integration_width
            + f" Integration ({integration_count})"
        )
        print("█" * unit_width + f" Unit ({unit_count})")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
