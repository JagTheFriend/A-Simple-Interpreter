import typing as t


counter = 0
def get_user_input() -> t.Tuple[int, str]:
    """Gets the user input
    Returns:
        tuple[int, str]: Contains a number and the user input
    """
    while True:
        try:
            yield counter, input(f"In [{counter}]: ")
            globals()["counter"] += 1  # increase the counter by 1
        except KeyboardInterrupt:
            pass

        except EOFError:
            break


def exec_function(user_input: t.AnyStr) -> t.Union[exec, eval]:
    """Checks whether eval or exec should be used"""
    try:
        compile(user_input, "<stdin>", "eval")
    except SyntaxError:
        return exec
    return eval


def exec_user_input(
    i: int,
    user_input: t.AnyStr,
    user_globals: t.Dict[str, t.Any]
) -> t.Dict[str, t.Any]:
    """Displays the output after executing the user input
    Args:
        i (int): Index number
        user_input (str): Contain the user input in string format
        user_globals (dict): Contains all the variables etc created by the user

    Returns:
        user_globals (dict): Contains all the (updated) variables etc created by the user
    """
    user_globals = user_globals.copy()

    try:
        retval = exec_function(user_input)(user_input, user_globals)

    except Exception as error:
        print(f"{error.__class__.__name__}: {error}")

    else:
        if retval is not None:
            print(f"Out[{i}]: {retval}")

    return user_globals


def selected_user_globals(user_globals: t.Dict[str, t.Any]) -> t.Tuple[str, t.Any]:
    """Returns what user defined variables were selected"""
    return (
        (key, user_globals[key])
        for key in sorted(user_globals)
        if not key.startswith("__") or not key.endswith("__")
    )


def save_user_globals(user_globals: t.Dict[str, t.Any], path="user_globals.txt"):
    """Saves all the global variables in a file
    Args:
        user_globals: Contains all the global variables defined by the user
        path (str, Default: "user_globals.txt"): Path to the file,
                                                where the global variables would be stored
    """
    with open(path, "w") as file:
        for key, val in selected_user_globals(user_globals):
            file.write(f"{key}: {val.__class__.__name__} = {val}\n")


def main():
    user_globals = {}
    print("Would like you to save all the variables in a separate file?")
    store_files = input("Enter yes/no: ")[0].lower() == "y"

    if store_files:
        save_user_globals(user_globals)

    for i, user_input in get_user_input():
        user_globals = exec_user_input(i, user_input, user_globals)

        if store_files:
            save_user_globals(user_globals)


if __name__ == "__main__":
    main()
