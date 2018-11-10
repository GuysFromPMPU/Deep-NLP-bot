#!/bin/bash

python -m deeppavlov riseapi pavlov_configs/squad_ru.json &
python -m deeppavlov riseapi pavlov_configs/ner_rus.json &