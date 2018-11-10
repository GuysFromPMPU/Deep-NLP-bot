


def getNer(text, ner_model):
    res = ner_model([text])
    return res