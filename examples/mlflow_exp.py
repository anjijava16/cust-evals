import mlflow
import mlflow.sklearn
#from sklearn.ensemble import RandomForestClassifier

import os
import subprocess

# Load environment variables from zsh profile
command = "source ~/.zprofile && env"
proc = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    shell=True,
    executable="/bin/zsh"
)
for line in proc.stdout:
    key, _, value = line.decode().partition("=")
    os.environ[key] = value.strip()

# Set tracking URI
mlflow.set_tracking_uri("http://localhost:5007")


# LLM Evaluation
import mlflow
from mlflow.metrics.genai import answer_relevance, faithfulness

# Set experiment
mlflow.set_experiment("llm-evaluation")

# Define your LLM function
def my_llm(inputs):
    import openai
    client = openai.OpenAI()

    responses = []
    for input_text in inputs["questions"]:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input_text}]
        )
        responses.append(response.choices[0].message.content)

    return responses

# Create evaluation dataset
eval_data = {
    "questions": [
        "What is MLflow?",
        "How does MLflow track experiments?",
        "What is a model registry?"
    ],
    "ground_truth": [
        "MLflow is an open-source platform for managing ML lifecycle...",
        "MLflow tracks experiments by logging parameters, metrics, and artifacts...",
        "A model registry is a centralized repository for storing ML models..."
    ]
}

# Evaluate
with mlflow.start_run():
    results = mlflow.evaluate(
        model=my_llm,
        data=eval_data,
        targets="ground_truth",
        model_type="question-answering",
        evaluators="default",
        extra_metrics=[
            answer_relevance,
            faithfulness
        ]
    )

    print(results.metrics)
    print(results.tables)