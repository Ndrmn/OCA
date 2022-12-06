
from app import app
class Commands:

    @classmethod
    def print_test(cls):
        print("just test message")


@app.cli.command("test")
def print_test():
    """test"""
    Commands.print_test()
