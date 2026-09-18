#!/usr/bin/env bash
#
# ENPM702 Git Workshop: broken-repository drills.
#
# Each scenario rebuilds a small sandbox from scratch and then puts it into a
# specific broken state. Nothing here touches your real repositories, and no
# GitHub account or network connection is needed: the sandbox ships with its
# own local "origin" so that push, pull and fetch behave the way they do
# against GitHub.
#
#   ./git-workshop.sh list        # show the scenarios
#   ./git-workshop.sh 3           # rebuild the sandbox in scenario 3
#   ./git-workshop.sh clean       # delete the sandbox
#
# Rerun any scenario as often as you like. Each run wipes the sandbox first,
# so you can experiment freely and start over when you paint yourself into a
# corner.
#
# Sandbox location: $HOME/git-workshop  (override with GIT_WORKSHOP_DIR)

set -euo pipefail

WORKSHOP_DIR="${GIT_WORKSHOP_DIR:-$HOME/git-workshop}"
REMOTE_DIR="$WORKSHOP_DIR/origin.git"
REPO_DIR="$WORKSHOP_DIR/robot-config"

AUTHOR_NAME="ENPM702 Student"
AUTHOR_EMAIL="student@example.com"

bold()  { printf '\033[1m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
red()   { printf '\033[31m%s\033[0m\n' "$*"; }
rule()  { printf '%s\n' "----------------------------------------------------------------"; }

git_repo() { git -C "$REPO_DIR" "$@"; }

# ---------------------------------------------------------------- base repo

wipe_sandbox() {
    rm -rf "$WORKSHOP_DIR"
    mkdir -p "$WORKSHOP_DIR"
}

write_config() {
    local rate="$1"
    cat > "$REPO_DIR/robot_config.yaml" <<YAML
robot:
  name: "delivery-bot"
  wheel_radius: 0.08      # meters
  max_speed: 1.5          # m/s

navigation:
  # General navigation settings for the robot
  update_rate: ${rate}          # Hz
  coordinate_system: "WGS84"
  obstacle_margin: 0.35   # meters

sensors:
  lidar: true
  imu: true
  gps: false
YAML
}

commit_all() {
    git_repo add -A
    git_repo commit -q -m "$1"
}

build_base_repo() {
    wipe_sandbox

    git init -q --bare -b main "$REMOTE_DIR"

    git init -q -b main "$REPO_DIR"
    git_repo config user.name  "$AUTHOR_NAME"
    git_repo config user.email "$AUTHOR_EMAIL"
    git_repo config advice.detachedHead false

    cat > "$REPO_DIR/README.md" <<'MD'
# robot-config

Configuration and navigation code for the ENPM702 delivery robot.

## Build

```bash
mkdir build && cd build
cmake .. && make
```
MD

    cat > "$REPO_DIR/.gitignore" <<'IGN'
# Build artifacts
build/
*.o
IGN

    write_config 5

    mkdir -p "$REPO_DIR/src"
    cat > "$REPO_DIR/src/navigation.cpp" <<'CPP'
#include <iostream>

namespace navigation {

double clamp_speed(double requested, double max_speed) {
    if (requested > max_speed) {
        return max_speed;
    }
    return requested;
}

}  // namespace navigation

int main() {
    std::cout << "navigation online\n";
    std::cout << navigation::clamp_speed(2.5, 1.5) << '\n';
}
CPP

    commit_all "Initial commit: add robot configuration and README"

    cat >> "$REPO_DIR/README.md" <<'MD'

## Navigation

The navigation stack runs at the rate set by `navigation.update_rate`.
MD
    commit_all "Document the navigation update rate in the README"

    sed -i 's/  imu: true/  imu: true\n  wheel_encoders: true/' "$REPO_DIR/robot_config.yaml"
    commit_all "Add wheel encoders to the sensor list"

    git_repo remote add origin "$REMOTE_DIR"
    git_repo push -q -u origin main
}

# ------------------------------------------------------------ teammate work

teammate_push() {
    # Simulates a teammate pushing to origin while you were working.
    local work_dir
    work_dir="$(mktemp -d)"
    git clone -q "$REMOTE_DIR" "$work_dir/clone"
    git -C "$work_dir/clone" config user.name "Priya (teammate)"
    git -C "$work_dir/clone" config user.email "priya@example.com"
    cat >> "$work_dir/clone/README.md" <<'MD'

## Safety

The robot stops if no heartbeat arrives for 500 ms.
MD
    git -C "$work_dir/clone" add -A
    git -C "$work_dir/clone" commit -q -m "Document the heartbeat safety timeout"
    git -C "$work_dir/clone" push -q origin main
    rm -rf "$work_dir"
}

# ------------------------------------------------------------- the scenarios

scenario_1() {
    build_base_repo
    local target
    target="$(git_repo rev-parse --short HEAD~1)"
    git_repo switch -q --detach "$target"

    sed -i 's/obstacle_margin: 0.35/obstacle_margin: 0.50/' "$REPO_DIR/robot_config.yaml"
    git_repo add -A
    git_repo commit -q -m "Widen the obstacle margin to 0.50 m after the hallway test"

    bold "Scenario 1: you are not on a branch"
    rule
    cat <<'TXT'
You went back to look at an older commit, started tinkering, and committed.
`git status` says "HEAD detached". The commit you just made belongs to no
branch, so the moment you switch away, nothing points at it any more.

Your job
  1. Confirm the situation with `git status` and `git log --oneline --all --graph`.
  2. Get the new commit onto a branch called `fix/obstacle-margin`
     without losing it.
  3. Merge that branch into `main`.

Hint: a branch is just a pointer. You can create one right where you stand.
TXT
    rule
}

scenario_2() {
    build_base_repo

    git_repo switch -q -c wip/rate-tuning
    write_config 3
    commit_all "Lower the update rate to 3 Hz so the GPS fix can settle"

    git_repo switch -q main
    write_config 10
    commit_all "HOTFIX: raise the update rate to 10 Hz for responsiveness"

    git_repo merge wip/rate-tuning >/dev/null 2>&1 || true

    bold "Scenario 2: a merge stopped halfway"
    rule
    cat <<'TXT'
You ran `git merge wip/rate-tuning` on `main` and it stopped: both branches
changed `navigation.update_rate`. The merge is paused. Your working tree has
conflict markers in it and the repository is in a half-finished state.

Your job
  1. Read `git status`. Notice what it tells you to do next.
  2. Open `robot_config.yaml` and find the `<<<<<<<`, `=======`, `>>>>>>>`
     markers. Decide on a final value and delete every marker.
  3. Stage the file and finish the merge with a commit that explains the
     choice you made.

Then start over (`./git-workshop.sh 2`) and take the other exit instead:
back out of the merge entirely and leave `main` exactly as it was.
TXT
    rule
}

scenario_3() {
    build_base_repo

    sed -i 's/  max_speed: 1.5          # m\/s/  max_speed: 15.0         # m\/s/' "$REPO_DIR/robot_config.yaml"
    commit_all "Bump max speed for the demo"
    git_repo push -q origin main

    bold "Scenario 3: a bad commit is already pushed"
    rule
    cat <<'TXT'
The commit "Bump max speed for the demo" set `max_speed` to 15.0 m/s. That is
ten times the safe value, and the robot is now dangerous. The commit is
already on `origin/main`, so your teammates have it too.

Your job
  1. Find the offending commit and read it with `git show`.
  2. Undo it in a way that is safe on a shared branch: the history your
     teammates already pulled must not change underneath them.
  3. Push the fix.

Question to answer out loud: why is `git reset --hard HEAD~1` the wrong tool
here, even though it would make your own copy look correct?
TXT
    rule
}

scenario_4() {
    build_base_repo

    git_repo switch -q -c feature/battery-monitor
    cat > "$REPO_DIR/src/battery.cpp" <<'CPP'
#include <iostream>

namespace power {

bool needs_charge(double voltage) {
    return voltage < 22.2;  // 6S pack, 3.7 V per cell
}

}  // namespace power
CPP
    commit_all "Add battery voltage monitoring"

    sed -i 's/  gps: false/  gps: false\n  battery_monitor: true/' "$REPO_DIR/robot_config.yaml"
    commit_all "Enable the battery monitor in the robot configuration"

    git_repo switch -q main
    git_repo branch -q -D feature/battery-monitor

    bold "Scenario 4: you deleted a branch you needed"
    rule
    cat <<'TXT'
Two afternoons of work lived on `feature/battery-monitor`. You thought it had
been merged. It had not. You deleted the branch. `git branch` no longer lists
it and `git log` shows no sign of the work.

Your job
  1. Find the commits again. They are not gone yet: Git keeps a record of
     everywhere HEAD has been.
  2. Recreate the branch pointing at the last commit of that work.
  3. Check that `src/battery.cpp` is back.

Hint: the command you need rhymes with "ref log".
TXT
    rule
}

scenario_5() {
    build_base_repo

    # One commit ago: the credentials file went in, and .gitignore went out.
    cat > "$REPO_DIR/robot_secrets.yaml" <<'YAML'
wifi:
  ssid: "ENPM702-Lab"
  password: "Terrapins2026!"
api:
  fleet_token: "ghp_ThisIsNotARealTokenButPretendItIs"
YAML
    rm -f "$REPO_DIR/.gitignore"
    commit_all "Add lab credentials for the field test"
    git_repo push -q origin main

    # Right now: build output and object files are staged but not committed.
    mkdir -p "$REPO_DIR/build/CMakeFiles"
    printf 'binary junk\n'    > "$REPO_DIR/build/robot_node"
    printf 'more junk\n'      > "$REPO_DIR/build/CMakeFiles/cache.txt"
    printf 'object file\n'    > "$REPO_DIR/src/navigation.o"
    printf 'another object\n' > "$REPO_DIR/src/battery.o"
    printf 'log line\n'       > "$REPO_DIR/robot.log"
    git_repo add -A

    bold "Scenario 5: the wrong things are in the repository"
    rule
    cat <<'TXT'
Someone ran `git add .` with no `.gitignore` in place. Two problems:

  a) Build output and a `.o` file are staged right now, waiting to be
     committed. Nothing has been committed yet, so this is easy.
  b) `robot_secrets.yaml`, which holds a wifi password and an API token,
     was committed one commit ago and pushed to `origin`. This is not easy.

Your job
  1. Unstage everything that should not be committed, without losing the
     files from your disk.
  2. Write a `.gitignore` that covers build output, object files, logs and
     the secrets file. Commit it.
  3. Stop tracking `robot_secrets.yaml` while keeping your local copy.
  4. Then answer the real question: after step 3, is the password still
     recoverable from this repository? Prove your answer with a Git command.
     What must actually happen to that wifi password now?
TXT
    rule
}

scenario_6() {
    build_base_repo

    # The feature branch has a committed change to robot_config.yaml ...
    git_repo switch -q -c feature/waypoints
    cat >> "$REPO_DIR/robot_config.yaml" <<'YAML'

waypoints:
  max_count: 50
YAML
    commit_all "Start the waypoint block"

    # ... and main has moved on in the same file, so the two versions differ.
    git_repo switch -q main
    sed -i 's/  lidar: true/  lidar: true\n  lidar_model: "VLP-16"/' "$REPO_DIR/robot_config.yaml"
    commit_all "Record the lidar model"
    git_repo push -q origin main

    # Back on the feature branch, with half-finished uncommitted edits.
    git_repo switch -q feature/waypoints
    sed -i 's/  max_count: 50/  max_count: 50\n  precision_m: 1.0   # TODO: confirm with the survey team/' "$REPO_DIR/robot_config.yaml"

    bold "Scenario 6: you are mid-edit and the fire alarm goes off"
    rule
    cat <<'TXT'
You are on `feature/waypoints` with unfinished, uncommitted edits in
`robot_config.yaml`. It is half-done and you do not want to commit it.

Then the urgent message arrives: a bug on `main` needs fixing right now.

Your job
  1. Try `git switch main`. Read what Git says.
  2. Park your unfinished work somewhere safe without committing it.
  3. Switch to `main`, change `obstacle_margin` to 0.45, commit.
  4. Go back to `feature/waypoints` and bring your unfinished edits back.
  5. Check that the parking spot is now empty.

Follow-up: what would you have done differently if the interruption had
lasted three days rather than ten minutes?
TXT
    rule
}

scenario_7() {
    build_base_repo

    teammate_push

    sed -i 's/obstacle_margin: 0.35/obstacle_margin: 0.40/' "$REPO_DIR/robot_config.yaml"
    commit_all "Widen the obstacle margin to 0.40 m"

    bold "Scenario 7: your push is rejected"
    rule
    cat <<'TXT'
You committed locally. Your teammate Priya pushed to `origin/main` while you
were working. Your history and the remote history have both moved forward
from the same commit, so they have diverged.

Your job
  1. Run `git push`. Read the rejection message carefully.
  2. Look at what is on the remote WITHOUT changing your working tree yet.
     Which commits do you have that origin does not, and vice versa?
  3. Bring the two histories together and push successfully.
  4. Look at the resulting shape with `git log --oneline --graph --all`.

Then start over (`./git-workshop.sh 7`) and do step 3 the other way, so the
history comes out as a straight line instead. What is the trade-off?
TXT
    rule
}

# -------------------------------------------------------------------- driver

show_list() {
    bold "ENPM702 Git Workshop scenarios"
    rule
    cat <<'TXT'
  1  Detached HEAD           You committed while not on any branch.
  2  Merge conflict          A merge stopped halfway and is waiting on you.
  3  Bad commit, pushed      An unsafe change is already on the remote.
  4  Deleted branch          Two afternoons of work, gone. Or are they?
  5  Junk and secrets        Build output staged, a password committed.
  6  Dirty working tree      Unfinished edits block a branch switch.
  7  Diverged from origin    Your push is rejected.
TXT
    rule
    printf 'Run one with:  %s 4\n' "$(basename "$0")"
}

main() {
    local arg="${1:-list}"

    case "$arg" in
        list|--list|-l|help|--help|-h)
            show_list
            exit 0
            ;;
        clean|--clean)
            rm -rf "$WORKSHOP_DIR"
            green "Removed $WORKSHOP_DIR"
            exit 0
            ;;
        1|2|3|4|5|6|7)
            "scenario_$arg"
            ;;
        *)
            red "Unknown scenario: $arg"
            show_list
            exit 1
            ;;
    esac

    green "Sandbox ready."
    printf 'Start here:  cd %s\n' "$REPO_DIR"
    printf 'Start over:  %s %s\n' "$(basename "$0")" "$arg"
}

main "$@"
