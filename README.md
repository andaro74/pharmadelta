# pharmadelta
What changed in FDA drug labeling, and which of our labels it touches. Built on agentkeel.

![PharmaDelta: an agent for FDA drug labeling changes. A question passes a door that admits named callers only and a guardrail that holds the rules outside the agent; the agent cites one row of the label table and one clause of 21 CFR; a CI gate asks again; the answer is a row, a clause and what we owe. A demo: the company is fictional, and it is not medical information.](docs/assets/readme-header.png)

pharmadelta shows what changed in FDA drug labeling and which labels it touches, with a citation on every claim, from an agent whose rules, tests and thresholds each have a named owner.

pharmadelta is an independent open-source demo and is not affiliated with any pharmaceutical company.

The authority for what this demo claims is [SPEC/00-overview.md](SPEC/00-overview.md). What was measured is in [milestones/README.md](milestones/README.md).

The pages are at <https://andaro74.github.io/pharmadelta/>. They show saved CI records and take no question.

## The problem

A generics company holds many drug labels. FDA labeling rules change. Each time, someone has to work out:

- which of our labels the change touches,
- what we owe because of it, and
- which rule says so.

An assistant that answers this from keywords gets the easy cases and fails the traps: a rule that is no longer in force, a route that is not open to a generics company, a reportable event buried in a note about something else. A wrong answer here can become a wrong filing.

pharmadelta answers that one question. Every answer names one row of the company's label table and one clause of 21 CFR Parts 201 and 314. An answer without both is not shown.

The company, Ardentia Generics, is fictional. Its portfolio and every "our label" statement are invented. The labels are real public-domain labels of old off-patent generics, read from DailyMed.

## What you can see

| Page | What it shows |
|---|---|
| [Detail](https://andaro74.github.io/pharmadelta/pages/detail.html) | Two questions sent to the deployed agent. Each answer with its row, its clause and the record of the call. |
| [Side by side](https://andaro74.github.io/pharmadelta/pages/side-by-side.html) | The same two questions answered by an ordinary assistant (a keyword baseline) and by the agent, with the answer the test expects. On the trap, the baseline differs and the agent does not. |
| [Try to break it](https://andaro74.github.io/pharmadelta/pages/break-it.html) | A request for dosing advice and an instruction hidden in a pasted document. What the platform's guardrail did on each, and the rule it named. |
| [Sign-off](https://andaro74.github.io/pharmadelta/pages/sign-off.html) | A seat holder's signature over a downloadable evidence package. |

The trap on the side-by-side page: an earlier version of a rule, no longer in force. The ordinary assistant says the label is impacted. The agent says it is not, which is what the test expects.

![The side-by-side page on the trap question. The expected answer: row metoprolol-tartrate.8.1, clause 201.57(c)(9)(i), impacted false, owed none, escalate false. The ordinary assistant's impacted and owed read "differs from expected"; all five of the deployed agent's values read "equals expected".](docs/assets/side-by-side-trap.png)

A picture of the page as saved on 2026-11-14. The page itself holds the records and the CI runs behind them.

## How it works

1. **The data is built from the sources.** Code in this repository reads the eCFR and DailyMed and builds the label table and the clauses. CI compares the build with the committed data.
2. **The agent holds that data and one tool.** The agent, `label-impact`, lives in its own repository. Its tool returns one row of the table and the clauses that row can be read under. The model decides from the row.
3. **The platform checks, signs and deploys the agent.** agentkeel refuses the agent while any of its seven seats is empty, signs its bundle, and deploys it on AWS.
4. **A question goes through the agent's door.** Only a caller the agent's manifest names is admitted. This repository's CI signs in as that caller.
5. **The guardrail reads the question first.** A treatment question or an instruction hidden in a pasted document is stopped there, under a named rule, before the model answers.
6. **The agent answers with a row, a clause and three fields:** whether the label is impacted, what is owed, and whether to escalate.
7. **CI saves the record and a gate re-checks it.** The pages are rebuilt from the saved record. On every run a gate asks the agent again and compares.

![How a question is answered, in five steps. The question is asked by this repository's CI as the named caller pharmadelta. Inside the agentkeel platform on AWS: 1, the door (API Gateway, Cognito) admits only a caller the agent names; 2, the guardrail (Bedrock Guardrails) stops treatment questions and hidden instructions; 3, the agent label-impact (AgentCore Runtime, a model on Bedrock) looks up one row of the label table in DynamoDB; 4, the answer is one row, one clause and three fields. Beside them: seven seats with named owners, and a signed deploy. Outside the platform: 5, CI saves the record and a gate asks again on every run; the pages show the saved records, with the frozen baseline as the control.](docs/assets/architecture.svg)

## Why an agent on a platform, and not one app with the rules inside it

A single app with the rules written into its prompt would answer the two questions on the detail page the same way. The difference is in what each can show to someone who has to rely on the answer.

| The question an auditor asks | One app with the rules inside | Here | Where it was measured |
|---|---|---|---|
| Who decided what the agent may say? | Whoever last edited the prompt. | Seven seats, each a named login. The platform refused the agent while one seat was empty. | [Ledger](milestones/README.md), row 1 |
| Can the agent talk its way past a rule? | The rule is text the model reads, next to the question. | The guardrail sits outside the agent. It stopped both attack questions and named the rule. | Row 6 and the note under the rows (a reading after the measurement) |
| Who is allowed to ask? | Anyone who can reach the app. | Only a caller the agent's manifest names. | Row P, measured in agentkeel |
| Is what runs what was reviewed? | Whatever was deployed last. | The platform signs each bundle and its deploy checks the signature. | agentkeel's own ledger, not this one |
| Is the data what the regulation says? | Typed in once. | Rebuilt from the eCFR and DailyMed in CI and compared. The row closed RED: the build found two errors in the hand-typed seed. | Row 2 |
| Better than what? | No control. | A frozen keyword baseline runs beside the agent. It fails the trap. | Rows 0 and 5 |
| Can I check it myself? | Read the code. | A signed evidence package to download, each file with its hash and the CI run that wrote it. | Row 7 |
| What does the next agent cost? | Build it all again. | A second agent starts from the same template and gets the same controls. | Row 8, **not yet measured** (M07) |

What the platform costs: three repositories where one would do, more moving parts, and a deploy pipeline to run. For one agent, one team and no one to answer to, an app with the rules inside is less work. The platform is for the case where a second agent arrives, or where someone outside the team has to rely on the answer. This demo has measured the rows above for the second case. The first case is M07 and is not measured yet.

## Main services and technologies

The AWS side is agentkeel's, read from its code at `3962809`. This repository holds none of it and has no AWS credential.

**Built for each agent by agentkeel**

| Service | What it does here |
|---|---|
| Amazon Bedrock | Runs the model the agent's manifest pins, through one inference profile per agent. |
| Amazon Bedrock AgentCore Runtime | Runs the agent's container, inside a VPC. |
| Amazon Bedrock Guardrails | The guardrail, built from the platform's baseline rules and the agent's own `rules/`. |
| Amazon DynamoDB | The label table the tool reads, and the platform's registry of deployed agents. |
| Amazon API Gateway and AWS Lambda | The door: an HTTP API with an authoriser that admits only the callers the manifest names. |
| Amazon Cognito | Issues the caller's token. |
| AWS KMS | One key per agent. |
| Amazon ECR | Holds the agent's container image. |
| Amazon VPC endpoints | The agent can reach only the AWS endpoints its manifest lists. |
| Amazon CloudWatch Logs | The door's access log: who asked, and whether they were admitted. |

**Platform-wide in agentkeel**

| Service or tool | What it does |
|---|---|
| AWS CloudTrail and Amazon S3 | Audit records, delivered to a bucket in a separate security account. |
| AWS CDK and CloudFormation | Every stack is code. |
| AWS IAM with GitHub OIDC | CI assumes a deploy role. No AWS key is stored in GitHub. |
| AWS Systems Manager Parameter Store | Settings the Security seat owns. |
| AWS Budgets | A daily spend ceiling. |
| Amazon Athena and Grafana | A panel over the registry. |
| Sigstore cosign | Signs each agent bundle. The deploy checks the signature. |
| A GitHub App | The platform check on every pull request in an agent's repository. |

**In this repository**

| Technology | What it does |
|---|---|
| Python 3.14 and `uv` | The ingestion, the baseline, the gates and the page writers. |
| GitHub Actions | Every result the ledger cites was written by a CI run. A local run is not evidence. |
| GitHub Pages | Serves the pages as static files. |
| eCFR API and DailyMed | The sources for the clauses and the labels. |

## What it is not

- **Not a validation.** It produces the evidence a validation would need.
- **Not medical information.** The agent assesses regulatory impact on labeling. It never answers a treatment question.
- **Not a statement about any marketed product.** The company is fictional.
- **Not live.** The pages show saved records. There is no box to type a question into.

Shortcomings a reader should know:

- One person holds all seven seats, so the reviewer reviews their own work. The pages say so.
- The detail and side-by-side pages serve two questions. The agent's own tests hold more.
- Row 2 of the ledger closed RED, with its finding.
- The time to create a second agent (M07) is not measured yet.

## Three repositories

| Repository | Holds |
|---|---|
| `andaro74/pharmadelta` (this one) | The spec, the ledger, the golden questions, the frozen baseline, the ingestion, the gates and the pages. |
| [`agentkeel-studio/label-impact`](https://github.com/agentkeel-studio/label-impact) | The agent: its manifest, code, prompt, tool, data, rules and its own tests. |
| [`andaro74/agentkeel`](https://github.com/andaro74/agentkeel) | The platform: checks, signing, deploy, guardrail, door, registry, audit. |

## How it was built

One milestone at a time, each with one claim, one planted failure and one measured verdict. The failure is committed before the code that catches it, and only a result written by CI counts. The [ledger](milestones/README.md) holds every row; [SPEC/00](SPEC/00-overview.md) holds the rules.
