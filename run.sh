#!/usr/bin/env bash
# Run an rtw example with a clean workspace.
#
# Usage:
#   ./run.sh <example_name> [rtw flags...]
#
# Examples:
#   ./run.sh simple_api
#   ./run.sh simple_api --max-iter 5
#   ./run.sh simple_api --backend claude --model sonnet-4.6
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
    echo "Usage: $0 <example_name> [rtw flags...]"
    echo ""
    echo "Available examples:"
    for d in "$SCRIPT_DIR"/*/; do
        name="$(basename "$d")"
        [[ -f "$d/TASK.md" ]] && echo "  $name"
    done
    exit 1
}

[[ $# -lt 1 ]] && usage

EXAMPLE_NAME="$1"
shift
EXAMPLE_DIR="${SCRIPT_DIR}/${EXAMPLE_NAME}"
TASK_FILE="${EXAMPLE_DIR}/TASK.md"

if [[ ! -f "$TASK_FILE" ]]; then
    echo "Error: No TASK.md found at ${TASK_FILE}"
    usage
fi

RUN_TS=$(date +%Y%m%d_%H%M%S)
RUN_DIR="${EXAMPLE_DIR}/runs/${RUN_TS}"
mkdir -p "$RUN_DIR"

echo "╔══════════════════════════════════════════╗"
echo "║  rtw-examples runner                     ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Example:   ${EXAMPLE_NAME}"
echo "║  Task:      ${TASK_FILE}"
echo "║  Workspace: ${RUN_DIR}"
echo "║  Extra args: $*"
echo "╚══════════════════════════════════════════╝"
echo ""

rtw run "$TASK_FILE" -w "$RUN_DIR" "$@"
EXIT_CODE=$?

echo ""
echo "────────────────────────────────────────────"
if [[ $EXIT_CODE -eq 0 ]]; then
    echo "Run completed successfully."
else
    echo "Run exited with code ${EXIT_CODE}."
fi
echo "Results: ${RUN_DIR}"
echo "────────────────────────────────────────────"

exit $EXIT_CODE
