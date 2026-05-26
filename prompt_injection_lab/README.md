# Prompt Injection Lab

This directory contains prompt-injection transition test cases.

I2OS treats prompt injection not merely as malicious text, but as an inadmissible state transition.

## Cases

| File | Expected |
|---|---|
| hidden_upload.json | BLOCK |
| tool_hijack_webpage.json | BLOCK |
| email_permission_escalation.json | BLOCK |
| safe_untrusted_summary.json | GO |
| memory_poisoning_attempt.json | BLOCK |

## Run Lab

```bash
python prompt_injection_lab/run_lab.py --policy policy/default_policy.json
```
