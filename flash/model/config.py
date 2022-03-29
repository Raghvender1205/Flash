from dataclasses import dataclass
from typing import Optional

@dataclass
class FlashConfig:
    experiment_name = "default"
    device: Optional[str] = 'cuda' # CUDA / CPU

    # Batch Sizes
    training_batch_size: Optional[int] = 32
    validation_batch_size: Optional[int] = 32
    test_batch_size: Optional[int] = 32

    # Training Parameters
    epochs: Optional[int] = 20
    gradient_accumulation_steps: Optional[int] = 1
    clip_grad_norm: Optional[float] = -1
    num_jobs: Optional[int] = -1
    fp16: Optional[bool] = False

    # DataLoader Parameters
    train_shuffle: Optional[bool] = True
    valid_shuffle: Optional[bool] = True
    train_drop_last: Optional[bool] = False
    valid_drop_last: Optional[bool] = False
    test_drop_last: Optional[bool] = False
    test_shuffle: Optional[bool] = False
    pin_memory: Optional[bool] = True

    # Scheduler Parameters
    step_scheduler_after: Optional[str] = "epoch"  # "epoch" or "batch"
    step_scheduler_metric: Optional[str] = None

    # TODO: Validation Parameters
    val_strategy: Optional[str] = 'epoch' # "epoch" or batch
    val_steps: Optional[int] = 100 # Not used if val_strategy is "epoch"