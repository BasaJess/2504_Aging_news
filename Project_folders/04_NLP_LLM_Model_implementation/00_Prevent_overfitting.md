### ***We detected overfitting. Here is an attempt to fix it:***
---
#### 1. Early Stopping (Stop Traiuning when overfitting starts)
Instead of training for a fixed 3 Epochs, we can stop training when the validation loss stops decreasing, or starts increasing
- Adding an Early stop to out trainer, modifying the training script to monitor validation loss and stop early if it stops improving:
``` 
from transformers import TrainerCallback

class EarlyStoppingCallback(TrainerCallback):
    def __init__(self, early_stopping_patience=2):
        self.early_stopping_patience = early_stopping_patience
        self.best_loss = float("inf")
        self.patience_counter = 0

    def on_evaluate(self, args, state, control, metrics, **kwargs):
        val_loss = metrics.get("eval_loss")
        if val_loss < self.best_loss:
            self.best_loss = val_loss
            self.patience_counter = 0
        else:
            self.patience_counter += 1

        if self.patience_counter >= self.early_stopping_patience:
            control.should_training_stop = True

early_stopping = EarlyStoppingCallback(early_stopping_patience=2)
```
The model will train until the validation loss stops improving for 2 consecutive evaluations
If the validation loss starts getting worse, training stop early to prevent overfitting

We need also to add a callback to the Trainer in the [notebook](../../notebooks/preprocess_fine-tune.ipynb)

```
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    callbacks=[early_stopping]
)
```

#### 2. Regularization (Prevent Model from memorizing too fast)
 - *Increase Droupout in BERT.* BERT has dropout layers that randomly disable some neuron during training. By increading dropout, we force the model to rely on different features, making it harder to memorize.
 ```
 from transformers import BertConfig, BertForSequenceClassification

 config = BertConfig.from_pretrained("bert-base-uncased",  hidden_dropout_prob=0.3, attention_probs_dropout_prob=0.3)
 model = BertForSequenceClassification.from_pretrained("bert-base-uncased", config=config)
```
Default dropout is 0.1 -> We increase it to 0.3 for stronger regularization.
 - *Reduce learning Rate (Prevent Overconfidence).* A hight learning rate may cause the model to quickly memorize training data, we will lower it from 5e-5 to 2e-5 or 3e-5:
 ```
  training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=3e-5,  # Reduced learning rate
    weight_decay=0.01,  # Helps generalization
)
```
 - *Add wiight decay(L2 regularization).* Weight decay prevents large weight values, forcing the model to stay simpler.
 ```
 training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    learning_rate=3e-5,
    weight_decay=0.01,  # L2 Regularization
)
```
#### 3. Reduce Epochs(Only train until necessary)
Trining for 3 full epochs is too much.
 - Reducing to 1 or 2 epochs
 - Using early stopping to let the model decide when to stop
 ```
 training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,  #  Reduce to 2
    per_device_train_batch_size=8,
    evaluation_strategy="epoch",
)
```