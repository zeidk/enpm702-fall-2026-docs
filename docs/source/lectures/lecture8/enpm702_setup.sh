#!/usr/bin/env bash
# enpm702_setup.sh: compile and run the live coding programs of L8 and L9.
#
# Before class, run it once. It checks that each program compiles and runs:
#     bash enpm702_setup.sh        # weeks 8 and 9 (week8_live, week9_live)
#     bash enpm702_setup.sh 9      # week 9 only (week9_live)
#
# In class, load it into your terminal once, then type live8 or live9 after
# each step:
#     source enpm702_setup.sh
#     live8                        # build week8_live; if it compiles, run it
#     live9                        # the same for week9_live
#
# It changes no file in the repository.
# The folder where you cloned the course repository. If you cloned it somewhere
# else, change the path between the quotes on line 18, for example:
#     ENPM702_LIVE_WS="$HOME/courses/enpm702-fall-2026-cpp"
ENPM702_LIVE_WS="$HOME/enpm702_cpp/enpm702-fall-2026-cpp"
ENPM702_LIVE_LINE=18    # the line above: the messages below name it

# Build week<N>_live. The compiler's output goes to the file $2; returns 1 to 3
# for each kind of failure, 0 when the program is built. When CMake does not
# know the target yet (a week just enabled in CMakeLists.txt), it configures
# again once and retries.
_enpm702_live_build() {
    local target="week${1}_live"
    if [ ! -f "$ENPM702_LIVE_WS/CMakeLists.txt" ]; then
        return 1
    fi
    if [ ! -f "$ENPM702_LIVE_WS/build/CMakeCache.txt" ]; then
        cmake -S "$ENPM702_LIVE_WS" -B "$ENPM702_LIVE_WS/build" -DCMAKE_BUILD_TYPE=Debug \
              -DCMAKE_EXPORT_COMPILE_COMMANDS=ON > "$2" 2>&1 || return 2
    fi
    if cmake --build "$ENPM702_LIVE_WS/build" --target "$target" > "$2" 2>&1; then
        return 0
    fi
    if grep -q "No rule to make target" "$2"; then
        cmake -S "$ENPM702_LIVE_WS" -B "$ENPM702_LIVE_WS/build" > "$2" 2>&1 || return 2
        cmake --build "$ENPM702_LIVE_WS/build" --target "$target" > "$2" 2>&1 || return 3
        return 0
    fi
    return 3
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

# --- Run with bash: check that the programs compile and run ------------------
case "${1:-}" in
    '') weeks="8 9" ;;
    *[!0-9]*) echo "usage: bash enpm702_setup.sh [week number]"; exit 2 ;;
    *) weeks="$1" ;;
esac

# Colors and symbols in a terminal; plain text in a file, a pipe, or with NO_COLOR.
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    bold=$'\e[1m'; dim=$'\e[2m'; red=$'\e[31m'; green=$'\e[32m'
    yellow=$'\e[33m'; cyan=$'\e[36m'; reset=$'\e[0m'; clear_line=$'\r\e[K'
    ok_mark="${green}✔${reset}"; fix_mark="${red}✘${reset}"
    tty=1
else
    bold=""; dim=""; red=""; green=""; yellow=""; cyan=""; reset=""; clear_line=""
    ok_mark="ok "; fix_mark="FIX"
    tty=0
fi

ok()   { echo "    $ok_mark $*"; }
fix()  { echo "    $fix_mark ${red}$*${reset}"; }
show_log() {
    echo "      ${dim}last lines of the output:${reset}"
    tail -n 15 "$1" | sed "s/^/      ${dim}│${reset} /"
}

repo_shown="${ENPM702_LIVE_WS/#$HOME/\~}"
echo
echo "  ${cyan}╭──────────────────────────────────────────────╮${reset}"
echo "  ${cyan}│${reset}  ${bold}ENPM702${reset} · Live Coding setup check           ${cyan}│${reset}"
echo "  ${cyan}╰──────────────────────────────────────────────╯${reset}"
echo
echo "  ${bold}Repository${reset}  $repo_shown"

if [ ! -f "$ENPM702_LIVE_WS/CMakeLists.txt" ]; then
    fix "no ENPM702 repository in this folder"
    echo "      Change line $ENPM702_LIVE_LINE of this script to the folder where you cloned it."
    echo
    exit 1
fi
ok "repository found"

failed=0
for week in $weeks; do
    target="week${week}_live"
    log="$(mktemp)"
    echo
    echo "  ${bold}Lecture $week${reset} ${dim}·${reset} $target"
    [ "$tty" = 1 ] && printf "    ${yellow}…${reset} building"
    start=$SECONDS
    _enpm702_live_build "$week" "$log"
    rc=$?
    seconds=$((SECONDS - start))
    printf "%s" "$clear_line"
    if [ "$rc" -eq 2 ]; then
        fix "CMake could not configure the repository"
        show_log "$log"; failed=1; rm -f "$log"; continue
    elif [ "$rc" -eq 3 ]; then
        fix "$target did not build"
        show_log "$log"; failed=1; rm -f "$log"; continue
    fi
    ok "built $target ${dim}(${seconds} s)${reset}"
    exe="$(_enpm702_live_exe "$week")"
    if [ -n "$exe" ] && "$exe" > "$log" 2>&1; then
        ok "ran $target"
    else
        fix "$target did not run"
        show_log "$log"; failed=1
    fi
    rm -f "$log"
done

echo
if [ "$failed" -ne 0 ]; then
    echo "  $fix_mark ${bold}Fix the lines marked above, then run this script again.${reset}"
    echo
    exit 1
fi
echo "  $ok_mark ${bold}Ready for class.${reset}"
echo
echo "  In class, type this once in your terminal:"
echo "      ${cyan}source $0${reset}"
echo "  Then, after each step:"
for week in $weeks; do
    echo "      ${cyan}live$week${reset}    ${dim}Lecture $week${reset}"
done
echo
exit 0
