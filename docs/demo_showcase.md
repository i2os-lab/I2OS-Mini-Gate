# I2OS Mini Gate v2.1
## Demo / Showcase Package

v2.1 adds a demonstration package for easy review.

## Added

```text
demo/
├── README.md
├── run_demo.py
├── demo_safe_action.json
├── demo_prompt_injection_block.json
├── demo_delete_block.json
└── demo_external_upload_repair.json
```

## Run

```bash
python demo/run_demo.py
```

## Design Position

v2.0 established the integrated Runtime Shield Prototype.

v2.1 makes it easier to show and understand.

The goal is not to add complexity.

The goal is to make the core concept visible:

```text
Can the AI do this?
↓
Should this transition be permitted before execution?
```
