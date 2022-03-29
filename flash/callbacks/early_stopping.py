import numpy as np

from flash import enums
from flash.callbacks import Callback
from flash.logger import logger


# https://en.wikipedia.org/wiki/Early_stopping
# https://pytorch-lightning.readthedocs.io/en/stable/common/early_stopping.html
class EarlyStopping(Callback):
    def __init__(self, monitor, model_path, patience=5, mode='min', delta=0.001, save_weights_only=False):
        self.monitor = monitor
        self.patience = patience
        self.counter = 0
        self.mode = mode
        self.best_score = None
        self.early_stop = False
        self.delta = delta
        self.save_weights_only = save_weights_only
        self.model_path = model_path

        if self.mode == 'min':
            self.val_score = np.Inf
        else:
            self.val_score = -np.Inf

        if self.monitor.startswith('train_'):
            self.model_state = 'train'
            self.monitor_value = self.monitor[len('train_'):]
        elif self.monitor.startswith('valid_'):
            self.model_state = 'valid'
            self.monitor_value = self.monitor[len('valid_') :]
        else:
            raise Exception('Monitor must start with train_ or valid_')

    def check(self, flash_trainer):
        epoch_score = flash_trainer.metrics[self.model_state][self.monitor_value]
        if self.mode == 'min':
            score = -1.0 * epoch_score
        else:
            score = np.copy(epoch_score)


        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(epoch_score, flash_trainer)
        elif score < self.best_score + self.delta:
            self.counter += 1
            logger.info('EarlyStopping counter: {} out of {}'.format(self.counter, self.patience))
            if self.counter >= self.patience:
                flash_trainer.model_state =  enums.ModelState.END
        else:
            self.best_score = score
            self.save_checkpoint(epoch_score, flash_trainer)
            self.counter = 0

    def on_valid_epoch_end(self, flash_trainer):
        if flash_trainer.config.val_strategy == 'epoch':
            return
        self.check(flash_trainer)

    def on_epoch_end(self, flash_trainer):
        if flash_trainer.config.val_strategy == 'batch':
            return
        self.check(flash_trainer)

    def save_checkpoint(self, epoch_score, flash_trainer):
        if epoch_score not in [-np.inf, np.inf, -np.nan, np.nan]:
            logger.info('\nScore improved ({} --> {}). Saving model'.format(self.val_score, epoch_score))
            flash_trainer.save(self.model_path, weights_only=self.save_weights_only)
        self.val_score = epoch_score