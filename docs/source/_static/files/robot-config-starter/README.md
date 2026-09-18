# robot-config

Baseline configuration for the ENPM702Tech sidewalk delivery robot.

Eleven robots on the test fleet boot from `robot_config.yaml`. Changes
here reach every one of them, so they go through a branch and a pull
request rather than straight onto `main`.

## Files

| File | Purpose |
|---|---|
| `robot_config.yaml` | Drive limits, navigation settings, sensor list |
| `.gitignore` | What Git should leave alone |

## Settings that matter

- `robot.max_speed` is capped at 1.5 m/s by the campus operating
  agreement. Do not raise it without sign-off.
- `navigation.update_rate` is how often the navigation stack recomputes
  position. Higher is more responsive and costs CPU; lower gives a GPS
  fix more time to settle.
- `navigation.obstacle_margin` is the clearance kept around detected
  obstacles, in meters.

## Changing a value

```bash
git switch -c feature/short-description
# edit robot_config.yaml
git add robot_config.yaml
git commit
```

Say in the commit message why the value changed, not just what changed.

Once this repository has a remote, push the branch and open a pull
request rather than merging it yourself.
