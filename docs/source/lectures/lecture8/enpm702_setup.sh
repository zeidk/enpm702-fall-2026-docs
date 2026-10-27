#!/usr/bin/env bash
# enpm702_setup.sh: get your ENPM702 C++ workspace ready for a lecture's live coding.
#
# Run it (do not source it), before class:
#
#     bash enpm702_setup.sh        # week 8, the default
#     bash enpm702_setup.sh 9      # week 9
#
# It changes nothing you wrote. It checks the tools, updates the repository with
# a fast-forward pull, checks that your shell loads enpm702-cpp.sh, then builds
# and runs the week's live coding program (week8_live for week 8). Each line
# says ok or FIX; a FIX line says what to do.
#
# The repository is ~/enpm702_cpp/enpm702-fall-2026-cpp unless you set
# ENPM702_WS, the same variable enpm702-cpp.sh uses:
#
#     ENPM702_WS=~/somewhere/enpm702-fall-2026-cpp bash enpm702_setup.sh

week="${1:-8}"
case "$week" in
    ''|*[!0-9]*) echo "usage: bash enpm702_setup.sh [week number]"; exit 2 ;;
esac
ws="${ENPM702_WS:-$HOME/enpm702_cpp/enpm702-fall-2026-cpp}"
target="week${week}_live"
log="$(mktemp)"
problems=0

ok()   { echo "  ok    $*"; }
fix()  { echo "  FIX   $*"; problems=$((problems + 1)); }
show_log() { echo "        last lines of the output:"; tail -n 15 "$log" | sed 's/^/        | /'; }

echo "ENPM702 setup for the week $week live coding"

# 1. Tools ---------------------------------------------------------------------
for pair in "g++ build-essential" "cmake cmake" "git git"; do
    set -- $pair
    if command -v "$1" > /dev/null 2>&1; then
        ok "$1 is installed"
    else
        fix "$1 is missing. Install it with: sudo apt install $2"
    fi
done

# 2. Repository ----------------------------------------------------------------
if [ ! -f "$ws/enpm702-cpp.sh" ] || [ ! -f "$ws/CMakeLists.txt" ]; then
    fix "no ENPM702 repository at $ws"
    echo "        Clone it with:"
    echo "        git clone https://github.com/zeidk/enpm702-fall-2026-cpp.git $ws"
    echo "        or set ENPM702_WS to where you cloned it."
    rm -f "$log"
    echo "$problems thing(s) to fix. Run this script again after fixing them."
    exit 1
fi
ok "repository at $ws"

# 3. Latest code ---------------------------------------------------------------
if git -C "$ws" pull --ff-only > "$log" 2>&1; then
    ok "repository is up to date"
else
    fix "git pull did not finish. Your own changes are kept; see what changed with:"
    echo "        git -C $ws status"
    show_log
fi

# 4. Shell configuration -------------------------------------------------------
case "$(basename "${SHELL:-bash}")" in
    zsh) rc="$HOME/.zshrc" ;;
    *)   rc="$HOME/.bashrc" ;;
esac
if grep -q "enpm702-cpp.sh" "$rc" 2>/dev/null; then
    ok "$rc loads enpm702-cpp.sh"
else
    fix "$rc does not load enpm702-cpp.sh. Add it once with:"
    echo "        echo 'source $ws/enpm702-cpp.sh' >> $rc"
fi

# 5. The week is enabled -------------------------------------------------------
if grep -Eq "^[[:space:]]*add_subdirectory\(project/week${week}\)" "$ws/CMakeLists.txt"; then
    ok "week $week is enabled in CMakeLists.txt"
else
    fix "week $week is not enabled. In $ws/CMakeLists.txt, remove the # before:"
    echo "        add_subdirectory(project/week${week})"
fi
if [ -d "$ws/project/week${week}/live" ]; then
    ok "project/week${week}/live is there"
else
    fix "project/week${week}/live is missing: the pull did not bring it"
fi

# 6. Configure, build and run --------------------------------------------------
if [ "$problems" -eq 0 ]; then
    if cmake -S "$ws" -B "$ws/build" -DCMAKE_BUILD_TYPE=Debug \
             -DCMAKE_EXPORT_COMPILE_COMMANDS=ON > "$log" 2>&1; then
        ok "configured (the same as 702configure)"
        if cmake --build "$ws/build" --target "$target" > "$log" 2>&1; then
            ok "built $target (the same as 702build $target)"
            exe="$(find "$ws/build" -type f -perm -u+x -name "$target" \
                        -not -path '*/CMakeFiles/*' | head -n 1)"
            if [ -n "$exe" ] && "$exe" > "$log" 2>&1; then
                ok "ran $target (the same as 702run $target)"
            else
                fix "$target did not run"
                show_log
            fi
        else
            fix "$target did not build"
            show_log
        fi
    else
        fix "cmake could not configure the repository"
        show_log
    fi
fi
rm -f "$log"

# 7. Summary -------------------------------------------------------------------
echo
echo "   workspace: $ws"
echo "   enabled  : $(grep -E '^[[:space:]]*add_subdirectory' "$ws/CMakeLists.txt" |
                     sed -E 's|.*project/([^)]*)\).*|\1|' | tr '\n' ' ')"
echo "   commands : 702configure, 702build, 702run, 702exe, 702w<n> (702help for all)"
echo
if [ "$problems" -eq 0 ]; then
    echo "Ready. In class, open a new terminal and type:"
    echo "    enpm702"
    echo "    702build $target"
    echo "    702run $target"
    exit 0
fi
echo "$problems thing(s) to fix. Run this script again after fixing them."
exit 1
