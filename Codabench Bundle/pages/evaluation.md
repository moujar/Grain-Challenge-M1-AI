# Evaluation

This page describes how submissions are evaluated and how scores are computed on the challenge platform.

---

## Evaluation Task

Participants must predict the **grain variety** for each test image.

* Each test sample corresponds to **one individual grain**.
* There are **8 possible grain varieties**.
* One label must be predicted per test image.

---

## Primary Evaluation Metric

The main evaluation metric is **classification accuracy**.

### Accuracy

Accuracy measures the proportion of correctly classified samples:

* A prediction is considered correct if the predicted label exactly matches the ground-truth label.
* The final score is the percentage of correct predictions over all test samples.

This metric is simple, intuitive, and easy to interpret.

---

## Evaluation Procedure

1. Participants submit a prediction file through the Codabench platform.
2. The platform runs the evaluation on a **hidden test set**.
3. The predicted labels are compared to the ground-truth labels.
4. The accuracy score is computed automatically.
5. The score is displayed on the leaderboard.

Ground-truth labels for the test set are **never shared** with participants.

---

## Leaderboard

* Submissions are ranked based on **accuracy**.
* Higher accuracy results in a better rank.

Limits on the number of daily submissions may apply.

---

## Validation and Generalization

The test data may include:

* Grains from different crop years
* Variations in acquisition conditions

This is done to evaluate the **generalization ability** of the submitted models.

---

## Important Notes

* Submissions with an invalid format will be rejected automatically.
* Do not include any additional files or outputs in your submission.
* Do not attempt to infer or access ground-truth labels.

Failure to follow these rules may result in disqualification.

---

## Final Remarks

The evaluation setup is designed to be fair, transparent, and reproducible. Participants are encouraged to focus on building models that generalize well rather than overfitting to a specific data split.
