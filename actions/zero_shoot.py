from transformers import pipeline


classifier = pipeline("zero-shot-classification",
                      model="Recognai/bert-base-spanish-wwm-cased-xnli")


def zeroShot(sentence, labels):
    inference = classifier(sentence, candidate_labels=labels,
                           hypothesis_template="Este ejemplo es {}.")
    if max(inference['scores']) > 0.5:
        return inference['labels'][inference['scores'].index(max(inference['scores']))]
    print(inference)
