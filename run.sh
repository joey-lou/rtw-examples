#!/usr/bin/env bash
# Run an rtw example with a clean workspace.
#
# Usage:
#   ./run.sh <example_name> [--rtw <rtw_command>] [rtw flags...]
#
# Examples:
#   ./run.sh simple_api
#   ./run.sh simple_api --max-iter 5
#   ./run.sh simple_api --rtw "uv run --project ~/dev/rtw rtw"
#   ./run.sh simple_api --rtw ./my-local-rtw --backend claude
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RTW_CMD="rtw"

usage() {
    echo "Usage: $0 <example_name> [--rtw <command>] [rtw flags...]"
    echo ""
    echo "Options:"
    echo "  --rtw <cmd>   rtw command to use (default: rtw)"
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

# Parse --rtw flag before forwarding the rest to rtw
RTW_ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --rtw)
            RTW_CMD="$2"
            shift 2
            ;;
        *)
            RTW_ARGS+=("$1")
            shift
            ;;
    esac
done

EXAMPLE_DIR="${SCRIPT_DIR}/${EXAMPLE_NAME}"
TASK_FILE="${EXAMPLE_DIR}/TASK.md"

if [[ ! -f "$TASK_FILE" ]]; then
    echo "Error: No TASK.md found at ${TASK_FILE}"
    usage
fi

# Determine version from the rtw binary
RTW_VERSION=$($RTW_CMD --version 2>/dev/null | awk '{print $2}')
if [[ -z "$RTW_VERSION" ]]; then
    echo "Error: Could not determine rtw version from: $RTW_CMD --version"
    exit 1
fi

# Pick run directory: <version>, <version>-1, <version>-2, ...
RUN_DIR="${EXAMPLE_DIR}/runs/${RTW_VERSION}"
if [[ -d "$RUN_DIR" ]]; then
    SUFFIX=1
    while [[ -d "${RUN_DIR}-${SUFFIX}" ]]; do
        SUFFIX=$((SUFFIX + 1))
    done
    RUN_DIR="${RUN_DIR}-${SUFFIX}"
fi
mkdir -p "$RUN_DIR"

echo "╔══════════════════════════════════════════╗"
echo "║  rtw-examples runner                     ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Example:   ${EXAMPLE_NAME}"
echo "║  rtw:       ${RTW_CMD} (${RTW_VERSION})"
echo "║  Task:      ${TASK_FILE}"
echo "║  Workspace: ${RUN_DIR}"
echo "║  Extra args: ${RTW_ARGS[*]:-}"
echo "╚══════════════════════════════════════════╝"
echo ""

$RTW_CMD run "$TASK_FILE" -w "$RUN_DIR" "${RTW_ARGS[@]}"
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
