---
name: ste-writing-aid
description: Write and rewrite technical prose in an STE-flavored style without claiming ASD-STE100 compliance. Use for Jira stories, acceptance criteria, repository documentation, API contracts, architecture notes, pull-request descriptions, runbooks, error messages, release notes, knowledge-base entries, and other engineering prose that should be clear, consistent, and easy to scan while preserving technical meaning, identifiers, requirements, exceptions, and terminology. Do not use for source code or voice-driven marketing and creative writing.
---

# STE Writing Aid

## Overview

Apply useful Simplified Technical English writing discipline without enforcing
the ASD-STE100 controlled vocabulary. Improve the form and readability of
technical prose while preserving its technical meaning.

## Set the Boundaries

- Use only the STE-flavored mode. Do not claim that the result complies with or
  is certified against ASD-STE100.
- Do not enforce a controlled dictionary or invent substitute terminology.
- Preserve code identifiers, commands, routes, literal strings, links,
  requirement strength, negation, numeric values, defaults, ordering, fallback
  behavior, exceptions, and established domain terms.
- Treat style improvement and fact verification as separate tasks. Inspect
  available sources when the user asks for verification, but do not imply that
  clearer prose is technically true.
- Do not rewrite source code. Rewrite comments, messages, and documentation
  around the code only when requested.

## Follow the Workflow

1. Determine whether the user wants a draft, rewrite, review, comparison, or
   explanation.
2. Identify the actors, stable terms, conditions, actions, outcomes, sequence,
   defaults, fallback behavior, and exceptions.
3. Mark the technical invariants that the rewrite must preserve.
4. Rewrite the text with the rules in this skill.
5. Perform the self-review before returning the result.

Read [document patterns](references/document-patterns.md) when the document is a
repository guide, Jira story, knowledge-base note, procedure, or another
structurally dense technical document.

Ask a question only when an unresolved ambiguity would change the technical
meaning. Inspect the available context and sources first.

## Apply the Writing Rules

### Use stable and precise terms

- Use one stable term for each concept.
- Keep established domain terminology when it is precise.
- Do not alternate between synonyms only to add variety.
- Preserve identifiers and literal technical values exactly.

### Name actors and actions

- Name the actor when it is known.
- Prefer active voice when it makes responsibility clearer.
- Use a direct verb for an action.
- Replace nominalizations and stacked helper verbs with direct verbs when this
  does not change the meaning.

### Control sentences and paragraphs

- Put one main idea in each sentence.
- Treat 25 words as a readability target, not a strict limit. Keep a longer
  sentence when splitting it would damage precision or the relationship between
  ideas.
- Keep one topic in each paragraph.
- Put a condition before its action or outcome.
- Keep related conditions, actions, and results close together.

### Make structure visible

- Use bullets for parallel requirements, facts, options, or outcomes.
- Use numbered steps only when order matters.
- Put one action in each procedural step.
- Use headings that name the subject or task.
- Keep existing Markdown structure unless a change materially improves
  comprehension.

### Remove avoidable friction

- Remove filler, repetition, unsupported hedging, and unsupported marketing
  claims.
- Avoid semicolons.
- Prefer a period or comma to an unnecessary em dash.
- Avoid chatty phrasal verbs when a precise direct verb is clearer.
- Retain established technical phrasal verbs such as `log in`, `roll back`, and
  `opt out` when a replacement would reduce precision or sound unnatural.

### Preserve requirement semantics

- Preserve modal strength. Do not change `must`, `should`, `may`, or `can`
  without evidence that the requirement changed.
- Preserve all negation.
- Preserve exact values, ranges, defaults, and limits.
- Preserve sequence and dependency.
- Preserve fallback behavior and exceptions.
- Do not add facts, requirements, actors, or guarantees that the source does not
  support.

## Return the Requested Form

Return only the requested prose by default.

Provide before-and-after text, annotations, a change summary, or a compliance
assessment only when the user requests it. Preserve code spans, code blocks,
links, and other literal material unless the user explicitly asks to change
them.

## Self-Review

Before returning the text, check:

- Does the result preserve every technical invariant?
- Does each concept have one stable name?
- Are actors explicit where responsibility matters?
- Do direct verbs describe the actions?
- Does each sentence contain one main idea where practical?
- Do conditions appear before their actions or outcomes?
- Do bullets represent parallel items and numbers represent sequences?
- Did the rewrite remove filler without removing useful qualification?
- Are identifiers, values, links, negation, defaults, and requirement strength
  unchanged?
- Did the rewrite avoid invented facts and unsupported guarantees?
- Does the response contain only the form that the user requested?

The skill improves writing form and readability. It cannot verify technical
truth unless the task also includes source-based verification.
