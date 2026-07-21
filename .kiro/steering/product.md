# Product Overview

Quizz is a command-line quiz game for comparing how well one participant can impersonate another.

## Purpose

The product supports two workflows:

1. A player session that collects a participant's own answers and the same participant's answers when impersonating another person.
2. A judge workflow that compares those answer sheets against the target person's actual answers and reports how closely the impersonation matched.

## Users

- Impersonator: the participant who answers questions in two perspectives.
- Judge: the person who evaluates the impersonation accuracy.

## Core Requirements

- The system must present multiple-choice questions from a YAML question set.
- The system must collect answers for two perspectives in a single run.
- The system must validate that answers correspond to defined question options.
- The system must persist answer sheets as YAML files.
- The system must score impersonation accuracy using exact matches per question.
- The system must render a scoreboard and a per-question breakdown with visual markers.
