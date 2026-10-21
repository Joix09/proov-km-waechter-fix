# What I checked, and what the agent got wrong

The agent performed perfectly. 

## What the agent got wrong

Nothing went catastrophically wrong, but there were two moments where I needed to
verify the agent's reasoning rather than just accept it.

**The miles conversion constant.** The agent correctly identified that `MILES_PER_KM = 1.609`
was inverted — 1.609 is kilometres-per-mile, not miles-per-kilometre. It replaced it with
`km / KM_PER_MILE` using `KM_PER_MILE = 1.60934`. I checked this manually: 100 km ÷ 1.60934
= 62.1 miles, which matches the expected value in `verify.py`. The agent's fix was right, but
I would not have caught a silent error in the constant if I had not re-read its reasoning.

**The missing-reading default.** The agent changed `car.get("last_service_km", 0)` to
`car.get("last_service_km")` with an early `return False`. The logic is: if we have no reading,
we cannot make a judgement, so we do not flag the car. I checked whether that is the right
policy (rather than, say, flagging the car to be safe) by re-reading the task description. The
task says "a car with no last-service reading must not be treated as fully worn", which
confirms the agent's choice. I also confirmed that `needs_service` and `car_wear` in
`fleet_report.py` are consistent — both treat a missing reading as "skip, contribute 0% wear".

## What I checked before I accepted the work

1. **Ran `pytest -v` after every change**, not just at the end. All 4 tests pass.
2. **Ran `python verify.py`** before and after each fix. After the code changes, 9/11 checks
   pass. The remaining two (`analyze.py` and `NOTES.md`) were the human-authored parts.
3. **Checked the rule constants by hand**: `SERVICE_INTERVAL_KM = 15000` and
   `WARN_AT_PERCENT = 80` in `km_wachter.py` are unchanged. `settings.cfg` still reads
   `service_interval_km = 15000` and `warn_at_percent = 80`. `verify.py` also confirms both.
4. **Checked the wear formula manually**: a car at 14,900 km since service should be
   14900 / 15000 × 100 = 99.33%. With the old `//` it gave 0%. With `/` it gives 99.3%.
   `verify.py`'s `wear_is_not_floored` check confirms this.
5. **Spot-checked the dead-code deletions** in `fleet_utils.py`: searched the whole codebase
   for calls to `is_due`, `parse_service_date`, and `chunk_list` before accepting their
   removal. None of them appear anywhere outside `fleet_utils.py` itself.

## What the data actually said

The obvious assumption going in was that high total mileage and old age predict breakdowns.
The data does not say that.

**`odometer_km` (total mileage): r = +0.002.** Cars that broke down had an average odometer
of 53,448 km. Cars that did not broke down averaged 53,302 km. That is a difference of
146 km across 120 cars — effectively zero. A car's total mileage tells you almost nothing
about whether it will break down.

**`age_years`: r = −0.001.** Even smaller — and slightly negative. Older cars were
marginally *less* likely to break down than younger ones, though the difference is noise.

**What actually predicts breakdowns:**

- `km_since_service` (r = +0.404): cars that broke down averaged 11,678 km since their last
  service; cars that survived averaged only 7,261 km. This is by far the strongest signal.
  A car running deep into its service window is already under stress.
- `avg_daily_km` (r = +0.252): harder-driven cars (more km per day) break down more often,
  regardless of their total mileage.
- `load_factor` (r = +0.215): heavily loaded cars fail more often.

The risk score built from these three catches 18 out of 26 real breakdowns (69%) in the
top-25% risk bucket — cars the 80%-wear rule would not have flagged yet, because they were
not near the interval threshold. The score lets the fleet team get ahead of the curve.
