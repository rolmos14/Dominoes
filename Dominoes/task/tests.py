from typing import List, Any
from hstest import *
import ast


class TestStage2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(),
            TestCase(),
            TestCase()
        ]

    def get_the_stock(self, reply):
        """Get the player's stock"""
        try:
            ind = reply.find("1:")
            ind2 = reply.lower().find("status")
            list_stack = reply[ind:ind2].strip().split('\n')
            stock = [i.split(':')[1].strip() for i in list_stack]
            try:
                stock = [ast.literal_eval(i) for i in stock]
            except (ValueError, SyntaxError):
                raise WrongAnswer("An error occurred while processing your output.\n"
                                           "Please make sure that your program's output is formatted exactly as described.")
            return stock
        except Exception:
            raise WrongAnswer("Please, output all pieces in the format: \"N:[N1, N2]\"\n"	
                              "Don't forget the colon character as a separator.")

    def check_the_stock(self, reply):
        """Check that the pieces in the player stock are unique"""

        uniq = self.get_the_stock(reply)
        len1 = len(uniq)
        try:
            uniq = set([tuple(i) for i in uniq])
        except TypeError:
            raise WrongAnswer("An error occurred while tests were processing your output.\n"
                              "Make sure you output pieces in the required format.")
        len2 = len(uniq)
        if len1 != len2:
            return False
        return True

    def check_the_snake(self, reply, ds):
        """Check that the domino snake is really the maximum"""

        stock = self.get_the_stock(reply)
        stock = [i for i in stock if i[0] == i[1]]
        if len(stock) > 0:
            if ds and type(ds[0]) != int:
                raise WrongAnswer("The domino snake is supposed to be a list containing two integers.\n"
                                  "Please, make sure you output the domino snake in the required format.")
            if ds < sorted(stock, reverse=True)[0]:
                return False
        return True

    def check_the_length(self, reply, cs):
        stock = self.get_the_stock(reply)
        opt = len(stock) == 7 and cs == 6
        opt2 = len(stock) == 6 and cs == 7
        if not (opt or opt2):
            return False
        return True

    def check_the_status(self, reply, cs):
        """Check if the status is right"""

        opt = cs == 7 and "computer is" in reply.lower()
        opt2 = cs == 6 and "your turn" in reply
        if not (opt or opt2):
            return False
        return True

    def check(self, reply: list, attach: Any) -> CheckResult:
        if not self.check_the_stock(reply):
            return CheckResult.wrong("Your pieces are not unique")
        replyk = [i for i in reply.split('\n') if i]
        if replyk[0] != "=" * 70:
            return CheckResult.wrong("The design is not right")
        try:
            stock_size = int(replyk[1].split()[-1])
        except ValueError:
            raise WrongAnswer("The stock size doesn't seem to be printed in the correct format. \n"
                              "Please, output it in the format: \"Stock size: N\",\n"
                              "where N is a number.")
        if stock_size != 14:
            return CheckResult.wrong("The stock is not right")
        try:
            domino_snake = ast.literal_eval(replyk[3])
        except (IndentationError, SyntaxError, ValueError):
            raise WrongAnswer("Domino pieces don't seem to be printed in the correct format.")

        if not self.check_the_snake(reply, domino_snake):
            return CheckResult.wrong("The domino snake should be the maximum")
        try:
            cs = int(replyk[2].split()[-1])
        except ValueError:
            raise WrongAnswer("Computer pieces don't seem to be printed in the correct format. \n"
                              "Please, output them in the format: \"Computer pieces: N\",\n"
                              "where N is a number.")
        if not 6 <= cs <= 7:
            return CheckResult.wrong("The computer pieces are not right")
        if not self.check_the_length(reply, cs):
            return CheckResult.wrong("Something is not right about the pieces played")
        if not self.check_the_status(reply, cs):
            return CheckResult.wrong("The status of the game is wrong")
        return CheckResult.correct()


if __name__ == '__main__':
    TestStage2('dominoes.dominoes').run_tests()
