# pharmadelta in five minutes

A guided tour of the demo. Seven stops, in order. Each says which page to open and what to notice.

The pages show saved records of calls this repository's CI made. Nothing calls the agent when you open a page, and there is no box to type a question into. The company, Ardentia Generics, is fictional. This is not medical information.

## 1. The overview (1 minute)

Open the [executive overview](https://andaro74.github.io/pharmadelta/pages/overview.html).

Notice:

- **The question.** A labeling rule changed: which of our labels does it touch, and what do we owe?
- **The first picture.** One trap question, from arriving to being signed off, in six steps.
- **The third picture.** Seven seats, each a pharma function that owns one decision.

## 2. Side by side (1 minute)

Open the [side-by-side page](https://andaro74.github.io/pharmadelta/pages/side-by-side.html). It shows four questions. Scroll to the second one, about a pregnancy category letter.

Notice:

- **The expected answer** sits above the two columns. It is the test's answer, written by the Data Owner seat.
- **The left column** is an ordinary assistant: a keyword matcher. Two of its values are marked "differs from expected".
- **The right column** is the deployed agent. All five of its values are marked "equals expected".
- **Each answer has its row and its clause** under it. An answer without both is not shown.

The third and fourth questions are the other two traps. The ordinary assistant picks the wrong row on both.

## 3. Detail (30 seconds)

Open the [detail page](https://andaro74.github.io/pharmadelta/pages/detail.html).

Notice:

- **"Where this answer came from"** under each answer: who asked, when, which version of the agent answered, and a link to the CI run.
- **The same answer as data** at the bottom of the page. A reader who distrusts the page reads the file.

## 4. Try to break it (1 minute)

Open the [break page](https://andaro74.github.io/pharmadelta/pages/break-it.html).

Notice:

- **A request for dosing advice** and **an instruction hidden in a pasted document**.
- **Each was stopped by the platform's guardrail**, before the model answered, and the page names the rule that fired.
- **The guardrail sits outside the agent.** The agent cannot talk its way past it.

## 5. Sign-off (30 seconds)

Open the [sign-off page](https://andaro74.github.io/pharmadelta/pages/sign-off.html).

Notice:

- **A seat holder's signature**, with the function the seat stands for.
- **An evidence package to download**, with its hash. Each file in it names the CI run that wrote it.
- **The sentence that one person holds all seven seats** in this demo.

## 6. The ledger (30 seconds)

Open [the ledger](../milestones/README.md).

Notice:

- **One row per milestone**: the claim, the commit that made it false, and the CI run that measured it.
- **Row 2 is RED.** The build from FDA sources found two errors in the hand-typed seed data. The row says so and stays RED.
- **Row 8 is open.** Creating a second agent on a stopwatch is not measured yet.

## 7. How it is built (30 seconds)

Open [the README](../README.md) and look at two things:

- **The colour diagram** under "How it works": the door, the guardrail, the agent, the answer, the record.
- **The table** under "Why an agent on a platform": what one app with the rules inside would leave unshown, and the ledger row behind each answer here.

## What you did not see

- **A live question.** A live path is a platform feature and is not built.
- **A rate.** The pages show four questions, one call each. Four answers are not a rate.
- **A validation.** The demo produces the evidence a validation would need.
