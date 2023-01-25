class MyError(Exception):
    """Base class for other exceptions"""
    pass


class LoadTasksProblem(MyError):
    """Raised when is problem to load data from database """

    def __str__(self):
        return "Problem to load tasks from database."


class LoadUserProblem(MyError):
    """Raised when user is not exist in db """

    def __str__(self):
        return "Problem for load user for login. User not exist in database."


class DatabaseWriteUserError(MyError):
    """Raised when is problem to save data in database """

    def __str__(self):
        return "There is a problem to save user in database."


class DatabaseWriteTaskError(MyError):
    """Raised when is problem to save data in database """

    def __str__(self):
        return "There is a problem to save task in database."


class DatabaseEditTaskError(MyError):
    """Raised when is problem to edit data in database """

    def __str__(self):
        return "There is a problem to edit task in database."


class DatabaseDeleteTaskError(MyError):
    """Raised when is problem to delete data in database """

    def __str__(self):
        return "There is a problem to delete task in database."
