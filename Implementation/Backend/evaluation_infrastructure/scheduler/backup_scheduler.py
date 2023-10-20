"""Scheduler module."""
import typing

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    """Custom scheduler class."""

    def __init__(self):
        """
        Initializes the scheduler.

        Args:
            scheduler (BackgroundScheduler): the scheduler to be used.
            tasks (List[Job]): the tasks to be executed.
        """
        self.scheduler = BackgroundScheduler()
        self.tasks: typing.List[Job] = []

    def add_task(self, task: typing.Callable[[], None], interval: int):
        """
        Adds a task to the scheduler.

        Args:
            task (Callable[[], None]): the task to be added.
            interval (int): the interval in minutes at which the task is to be executed.
        """
        job: Job = self.scheduler.add_job(task, "interval", minutes=interval)
        self.tasks.append(job)

    def remove_task(self, task: typing.Callable[[], None]):
        """
        Removes the task from the scheduler.
        If the task is not found, nothing happens.

        Args:
            task (Callable[[], None]): Task to be removed.
        """
        if task_to_remove := next(
            (job for job in self.tasks if job.func == task),
            None,
        ):
            task_to_remove.remove()
            self.tasks.remove(task_to_remove)

    def start(self):
        """Starts the scheduler."""
        self.scheduler.start()

    def stop(self):
        """Stops the scheduler."""
        self.scheduler.shutdown()
