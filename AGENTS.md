# Style
- Short, concise, technical. No emojis, no fluff.
- Answer questions first, then act.
- Explicitly agree/disagree before explaining changes.
# Architecture
- Before writing any code, explicitly describe the architecture you propose and wait for the user's approval.
- If the user has already specified the architecture, follow it exactly instead of proposing an alternative.
- If you believe a different architecture would be be better, explain why and ask for confirmation before deviating from the user's design.
# Code Quality
- Read files fully before wide changes; don't rely on search snippets.
- Avoid any; use proper types.
- Inline single-use helpers. Top-level imports only (no dynamic imports).
- Upgrade deps instead of downgrading code to fix type errors.
- Use erasable TypeScript only (no enums, namespaces, parameter properties).
- Ask before removing intentional functionality.
- Don't hardcode configurable values; use config files.
- Use subagents to handle medium to large tasks.
# Code Style
- Use snake_case for variables, camelCase for functions, PascalCase for classes and types, and kebab-case for filenames.
# User Override
If the user's instructions conflict with any rule in this document, ask for explicit confirmation before overriding. Only then execute their instructions.
