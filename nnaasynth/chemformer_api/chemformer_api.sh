export CHEMFORMER_MODEL=/path/to/chemformer/model.ckpt
export CHEMFORMER_VOCAB=/path/to/Chemformer/bart_vocab_downstream.json
export CHEMFORMER_TASK=forward_prediction

python /path/to/aizynthmodels/service/chemformer/bart_service.py

