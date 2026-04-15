# MEMORY.md

> **Keep this index in sync:** Whenever an entry is added, removed, or renamed inside `docs/memory/`, update this file accordingly.

## Index

_No entries yet._

## Creating and maintaining memory

Memories are organized by day. Each day has its own file in `docs/memory/YYYY-MM-DD.md`.

## Rules for memory entries:

1. **One file per day.** Create `docs/memory/YYYY-MM-DD.md` for each day that has entries.
2. **Usage counter is required.** Every entry must have a `Counter` and `Last used` line. Increment the counter each time a memory is useful to you. The more a pathway is used, the stronger it becomes — this mimics how organic memory works.
3. **Entries must be atemporal and generalizable.** Keep insights, lessons learned, and best practices that apply to future work. If a memory only applies to an isolated past event, it's not worth keeping.
4. **Most recent day first.** Both this index and entries within daily files are in reverse chronological order.
5. **Update the index.** When adding or removing entries in daily files, update this file to match.

## Daily memory files format

Each daily file is created the same way. Below is the file template format for when you create a new daily memory file.

**Placeholders:**
- `YYYY-MM-DD` → the date of the memory entries
- `RELATIVE_PATH_TO_MEMORY.md` → relative path from the daily file to [this very file](./MEMORY.md)
- `LIST_OF_ENTRIES` → a list of entries written in very specific format (described below in the [Entry format](#entry-format) section)

```
# Memory - YYYY-MM-DD

> Whenever an entry is added, removed, or renamed here, update [MEMORY.md]([RELATIVE_PATH_TO_MEMORY.md]) accordingly.

## Entries

[LIST_OF_ENTRIES]
```

## Entry format

Each entry in the daily memory files must follow this exact format below.

**Placeholders:**
- [ENTRY_TITLE]: a short descriptive title for the memory, ideally in the form of a best practice or lesson learned (e.g., "Simplicity", "Anticipation", "Pre-commit hook", "ESLint", etc)
- [MEMORY_CONTENT]: The content of the memory - what happened, what was learned, why it matters for future work.
- [SPECIFIC_DETAIL_1], [SPECIFIC_DETAIL_2], ..., [SPECIFIC_DETAIL_N]: Specific details, examples, or sub-lessons that support the main memory content. These should be concise and directly relevant to the memory.

```
### [ENTRY_TITLE]

> Counter: 0 uses
> Last used: [LAST_USED_DATE_YYYY-MM-DD_OR_NEVER]

[MEMORY_CONTENT]

- [SPECIFIC_DETAIL_1]
- [SPECIFIC_DETAIL_2]
- ...
- [SPECIFIC_DETAIL_N]
```
