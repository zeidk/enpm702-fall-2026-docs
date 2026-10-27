#!/usr/bin/env bash
# enpm702_setup.sh: check that a lecture's live coding program compiles and runs.
#
# Run it (do not source it), before class, after your workspace is ready:
#
#     bash enpm702_setup.sh        # week 8, the default
#     bash enpm702_setup.sh 9      # week 9
#
# It changes no file in the repository. It configures the build (the same as
# 702configure), builds the week's live coding program (week8_live for week 8,
# the same as 702build week8_live) and runs it (the same as 702run week8_live).
# Each line says ok or FIX.
#
# The repository is ~/enpm702_cpp/enpm702-fall-2026-cpp unless you set
# ENPM702_WS, the same variable enpm702-cpp.sh uses:
#
#     export ENPM702_WS=~/somewhere/enpm702-fall-2026-cpp
#     bash enpm702_setup.sh

week="${1:-8}"
case "$week" in
    ''|*[!0-9]*) echo "usage: bash enpm702_setup.sh [week number]"; exit 2 ;;
esac
ws="${ENPM702_WS:-$HOME/enpm702_cpp/enpm702-fall-2026-cpp}"
target="week${week}_live"
log="$(mktemp)"

ok()  { echo "  ok    $*"; }
fix() { echo "  FIX   $*"; }
show_log() { echo "        last lines of the output:"; tail -n 15 "$log" | sed 's/^/        | /'; }
finish() { rm -f "$log"; echo; echo "$1"; exit "$2"; }

echo "ENPM702: compile and run $target"

if [ ! -f "$ws/CMakeLists.txt" ]; then
    fix "no ENPM702 repository at $ws"
    echo "        Set ENPM702_WS to the folder where you cloned it."
    finish "Fix the line above, then run this script again." 1
fi
ok "repository at $ws"

if ! cmake -S "$ws" -B "$ws/build" -DCMAKE_BUILD_TYPE=Debug \
           -DCMAKE_EXPORT_COMPILE_COMMANDS=ON > "$log" 2>&1; then
    fix "cmake could not configure the repository"
    show_log
    finish "Fix the line above, then run this script again." 1
fi
ok "configured (the same as 702configure)"

if ! cmake --build "$ws/build" --target "$target" > "$log" 2>&1; then
    fix "$target did not build"
    show_log
    finish "Fix the line above, then run this script again." 1
fi
ok "built $target (the same as 702build $target)"

exe="$(find "$ws/build" -type f -perm -u+x -name "$target" -not -path '*/CMakeFiles/*' | head -n 1)"
if [ -z "$exe" ] || ! "$exe" > "$log" 2>&1; then
    fix "$target did not run"
    show_log
    finish "Fix the line above, then run this script again." 1
fi
ok "ran $target (the same as 702run $target)"

finish "Ready for class." 0
