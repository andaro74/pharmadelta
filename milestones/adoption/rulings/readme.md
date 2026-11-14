---
ruling: readme
seat:
  - Product
  - Security
  - Engineering
authorises:
  # Product: what the README says the demo is, how it works and why a platform (rulings 1, 2, 5)
  - README.md
  # Engineering, Security: the services named, read from agentkeel's code (rulings 3, 4)
  - README.md
  - milestones/adoption/rulings/readme.md
evidence:
  - SPEC/00-overview.md
  - docs/adr/ADR-0001-spec00-adopted.md
  - milestones/README.md
  - pages/api/answers.json
  - pages/api/baseline.json
  - pages/api/break-it.json
  - pages/api/sign-off.json
  - https://github.com/andaro74/agentkeel/tree/3962809/infra
  - https://github.com/andaro74/agentkeel/blob/3962809/infra/construct/governed_agent.py
  - https://github.com/andaro74/agentkeel/blob/3962809/infra/construct/door.py
  - https://github.com/andaro74/agentkeel/blob/3962809/infra/bootstrap/app.py
  - https://github.com/andaro74/agentkeel/blob/3962809/infra/audit/README.md
  - https://github.com/andaro74/agentkeel/blob/3962809/infra/security/README.md
  - https://github.com/andaro74/agentkeel/blob/3962809/infra/grafana/README.md
  - https://github.com/andaro74/agentkeel/blob/3962809/.github/workflows/deploy.yml
  - https://github.com/agentkeel-studio/label-impact/blob/bd89989/manifest.yaml
pr: https://github.com/andaro74/pharmadelta/pull/43
---

# Ruling: the README

One person holds all seven seats on this project (agentkeel ruling R1,
ADR-0001). This file records which seat rules on which edit.

This PR is outside any milestone's cap (U9). It carries no claim,
plants nothing and measures nothing. It changes `README.md` and adds
this file. No ledger row, served file, page, gate or workflow is
touched, and no call to the agent was made. The owner asked on
2026-11-14 for a README that says what problem the demo solves, how it
works, what a platform gives that one app with the rules inside does
not, and the main AWS services and technologies.

## Rulings in this PR

1. **Product (what stays word for word).** The tagline, SPEC/00 §1's
   one sentence and §2's "not affiliated" sentence are unchanged, as
   are the lines naming SPEC/00, the ledger and the pages' URL.
2. **Product (the comparison).** The section "Why an agent on a
   platform" is a table of questions. Each "Here" cell names a ledger
   row, or says the measurement is agentkeel's, or says "not yet
   measured" (row 8, M07). It states no number. It says what one app
   with the rules inside would do in plain words and makes no measured
   claim about such an app: none was built. It names what the platform
   costs and the case where an app is less work.
3. **Engineering (the services).** Every AWS service the README names
   was read in `andaro74/agentkeel` at `3962809` on 2026-11-14: the CDK
   modules `infra/` imports (`aws_bedrock`, `aws_bedrockagentcore`,
   `aws_dynamodb`, `aws_apigatewayv2`, `aws_lambda`, `aws_cognito`,
   `aws_kms`, `aws_ecr`, `aws_ec2`, `aws_logs`, `aws_cloudtrail`,
   `aws_s3`, `aws_ssm`, `aws_budgets`, `aws_athena`, `aws_iam`), the
   construct's and the door's docstrings, the four stack READMEs, and
   `deploy.yml` for cosign and the two OIDC uses. A service agentkeel
   imports and the README does not name (Kinesis Data Firehose, Glue,
   SAM) was left out as not one of the main ones. What each service
   does is one line taken from that code's own description. This
   repository holds no AWS resource and no AWS credential.
4. **Security (nothing of the door or the accounts).** The README
   names services, never an account id, a host, a pool id, a client id
   or an ARN. Grep for `execute-api`, `us-west-2_`, `amazonaws` and a
   twelve-digit number: no match.
5. **Product (SPEC/00 §2 and §11).** None of the six words appears in
   the README. "Not a validation. It produces the evidence a validation
   would need." is §2's wording without the word §2 bans. The README
   says the company is fictional, that the demo is not medical
   information, that the pages take no question, that one person holds
   all seven seats, and that row 2 closed RED.
6. **Product.** This PR is #43, the next number on this repository.

## What a reader can falsify

- `git diff ac366d2..<head> --stat` touches `README.md` and this file
  only.
- Each ledger row the comparison table names says what the cell says.
- `grep -i -w -E "validated|compliant|governed|secure|proven" README.md`
  prints nothing.
- Each service in the tables is imported or named under `infra/` or in
  `.github/workflows/deploy.yml` of `andaro74/agentkeel` at `3962809`.
- The four page links answer 200.

## What this ruling does not settle

- The README's AWS section goes stale when agentkeel changes. Nothing
  here reads agentkeel in CI. The owner re-reads it when the platform's
  tag moves.
- Row 8's cell in the comparison table changes from "not yet measured"
  when M07 closes, in M07's close PR or one after it.
- Whether the Mermaid diagram renders as intended is read on GitHub
  after the push, and recorded in a comment on #43.
