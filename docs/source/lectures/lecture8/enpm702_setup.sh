#!/usr/bin/env bash
# enpm702_setup.sh: compile and run a lecture's live coding program.
#
# Before class, run it once. It checks that the program compiles and runs:
#     bash enpm702_setup.sh        # week 8 (week8_live), the default
#     bash enpm702_setup.sh 9      # week 9 (week9_live)
#
# In class, load it into your terminal once, then type live8 after each step:
#     source enpm702_setup.sh
#     live8                        # build week8_live; if it compiles, run it
#     live9                        # the same for week9_live
#
# It changes no file in the repository.

# The folder where you cloned the course repository. If you cloned it somewhere
# else, change the path between the quotes, for example:
#     ENPM702_LIVE_WS="$HOME/courses/enpm702-fall-2026-cpp"
ENPM702_LIVE_WS="$HOME/enpm702_cpp/enpm702-fall-2026-cpp"
ENPM702_LIVE_LINE=18    # the line above: the messages below name it

# Build week<N>_live. The compiler's output goes to the file $2; returns 1 to 3
# for each kind of failure, 0 when the program is built.
_enpm702_live_build() {
    local target="week${1}_live"
    if [ ! -f "$ENPM702_LIVE_WS/CMakeLists.txt" ]; then
        return 1
    fi
    if [ ! -f "$ENPM702_LIVE_WS/build/CMakeCache.txt" ]; then
        cmake -S "$ENPM702_LIVE_WS" -B "$ENPM702_LIVE_WS/build" -DCMAKE_BUILD_TYPE=Debug \
              -DCMAKE_EXPORT_COMPILE_COMMANDS=ON > "$2" 2>&1 || return 2
    fi
    cmake --build "$ENPM702_LIVE_WS/build" --target "$target" > "$2" 2>&1 || return 3
}

# Print the path of the program week<N>_live under build/.
_enpm702_live_exe() {
    find "$ENPM702_LIVE_WS/build" -type f -perm -u+x -name "week${1}_live" \
         -not -path '*/CMakeFiles/*' 2>/dev/null | head -n 1
}

# live8, live9: build the week's program and, if it compiles, run it.
_enpm702_live() {
    local log exe rc
    log="$(mktemp)"
    _enpm702_live_build "$1" "$log"
    rc=$?
    if [ "$rc" -eq 1 ]; then
        echo "No ENPM702 repository at $ENPM702_LIVE_WS."
        echo "Change line $ENPM702_LIVE_LINE of enpm702_setup.sh, then source it again."
    elif [ "$rc" -ne 0 ]; then
        cat "$log"
        echo "week${1}_live did not compile: read the first error above."
    fi
    rm -f "$log"
    [ "$rc" -eq 0 ] || return 1
    exe="$(_enpm702_live_exe "$1")"
    "$exe"
}
live8() { _enpm702_live 8; }
live9() { _enpm702_live 9; }

# --- Sourced: live8 and live9 are now defined in this terminal ---------------
_enpm702_live_sourced=1
if [ -n "${BASH_VERSION:-}" ] && [ "${BASH_SOURCE[0]}" = "$0" ]; then
    _enpm702_live_sourced=0
fi
if [ -n "${ZSH_VERSION:-}" ]; then
    case "$ZSH_EVAL_CONTEXT" in
        *:file*) ;;
        *) _enpm702_live_sourced=0 ;;
    esac
fi
if [ "$_enpm702_live_sourced" = 1 ]; then
    unset _enpm702_live_sourced
    echo "live8 and live9 are ready in this terminal."
    return 0
fi

# --- Run with bash: check that the program compiles and runs -----------------
week="${1:-8}"
case "$week" in
    ''|*[!0-9]*) echo "usage: bash enpm702_setup.sh [week number]"; exit 2 ;;
esac
target="week${week}_live"
log="$(mktemp)"

echo "ENPM702: compile and run $target"
_enpm702_live_build "$week" "$log"
rc=$?
if [ "$rc" -eq 1 ]; then
    echo "  FIX   no ENPM702 repository at $ENPM702_LIVE_WS"
    echo "        Change line $ENPM702_LIVE_LINE of this script to the folder where you cloned it."
elif [ "$rc" -eq 2 ]; then
    echo "  ok    repository at $ENPM702_LIVE_WS"
    echo "  FIX   cmake could not configure the repository"
elif [ "$rc" -eq 3 ]; then
    echo "  ok    repository at $ENPM702_LIVE_WS"
    echo "  ok    configured"
    echo "  FIX   $target did not build"
else
    echo "  ok    repository at $ENPM702_LIVE_WS"
    echo "  ok    configured"
    echo "  ok    built $target"
    exe="$(_enpm702_live_exe "$week")"
    if [ -n "$exe" ] && "$exe" > "$log" 2>&1; then
        echo "  ok    ran $target"
        rm -f "$log"
        echo
        echo "Ready for class. In class, type these two lines once in your terminal:"
        echo "    source $0"
        echo "    live$week"
        echo "and type live$week again after each step."
        exit 0
    fi
    echo "  FIX   $target did not run"
fi
if [ "$rc" -ge 2 ] || [ -s "$log" ]; then
    echo "        last lines of the output:"
    tail -n 15 "$log" | sed 's/^/        | /'
fi
rm -f "$log"
echo
echo "Fix the line above, then run this script again."
exit 1
