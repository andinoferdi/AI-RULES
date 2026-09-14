# AI-RULES maintenance

This repository maintains portable instructions and generated host adapters, not an application.
Use the project contract in [Agents.md](put-in-your-projects/Agents.md) once when needed;
references within that template resolve relative to its own directory.
Keep one canonical Andino skill in `skills/andino-workflow`; generated installs are not editable sources.
Never copy user credentials/config backups into this repository. Preserve the personal prompt library.
Validate scripts with isolated temporary homes and `scripts/validate.py`; no remote mutation or commit unless requested.
