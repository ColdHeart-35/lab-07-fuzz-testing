# Lab 7: Fuzz Testing

This project demonstrates defensive input validation with three functions in `processor.py`:

- `parse_int_list`: parses comma-separated decimal integers; invalid input returns an empty list.
- `normalize_username`: accepts 1–32 ASCII letters, digits, underscores, or hyphens and returns lowercase text; invalid input returns an empty string.
- `calculate_average`: averages finite numbers from a nonempty list or tuple; invalid input returns `None`.

## Run

```sh
python -m pip install -r requirements.txt
python processor.py
python -m pytest -q test_processor.py
```

Hypothesis tests generate malformed types, arbitrary text, and numeric edge cases. The supplied handout PDF did not include the referenced starter `processor.py`; these functions and their contracts were reconstructed for the lab. The report calls this out and distinguishes the handout's demonstrated parser bug from the added examples.
## GitHub

Project repository: https://github.com/ColdHeart-35/lab-07-fuzz-testing
