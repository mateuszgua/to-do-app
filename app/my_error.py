class MyError(Exception):
    """Base class for other exceptions"""
    pass


class UserNotExist(MyError):
    """Raised when user is not exist in db """

    def __str__(self):
        return "User not exist in database."


class TasksNotExist(MyError):
    """Raised when tasks is not exist in db """

    def __str__(self):
        return "Task not exist in database."


class DatabaseReaderProblem(MyError):
    """Raised when is problem to load data from database """

    def __str__(self):
        return "Problem to load data from database."


class DatabaseWriterError(MyError):
    """Raised when is problem to save data in database """

    def __str__(self):
        return "There is a problem to save data in database."
