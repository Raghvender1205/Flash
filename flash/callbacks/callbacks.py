from typing import List


class Callback:
    def on_epoch_start(self, flash_trainer, **kwargs):
        return

    def on_epoch_end(self, flash_trainer, **kwargs):
        return

    def on_train_epoch_start(self, flash_trainer, **kwargs):
        return

    def on_train_epoch_end(self, flash_trainer, **kwargs):
        return

    def on_valid_epoch_start(self, flash_trainer, **kwargs):
        return

    def on_valid_epoch_end(self, flash_trainer, **kwargs):
        return

    def on_train_step_start(self, flash_trainer, **kwargs):
        return

    def on_train_step_end(self, flash_trainer, **kwargs):
        return

    def on_valid_step_start(self, flash_trainer, **kwargs):
        return

    def on_valid_step_end(self, flash_trainer, **kwargs):
        return

    def on_test_step_start(self, flash_trainer, **kwargs):
        return

    def on_test_step_end(self, flash_trainer, **kwargs):
        return

    def on_train_start(self, flash_trainer, **kwargs):
        return

    def on_train_end(self, flash_trainer, **kwargs):
        return


# Call Callbacks Implemented in Flash..
class CallbackRunner:
    def __init__(self, callbacks: List[Callback], flash_trainer):
        self.flash_trainer = flash_trainer
        self.callbacks = callbacks

    def __call__(self, current_state, **kwargs):
        for cb in self.callbacks:
            _ = getattr(cb, current_state.value)(self.flash_trainer, **kwargs)