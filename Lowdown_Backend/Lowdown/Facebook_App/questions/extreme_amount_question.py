from collections import defaultdict
import random

from questions import MultipleChoiceQuestion

class ExtremeAmountQuestion(MultipleChoiceQuestion):
    def __init__(self, responses_amounts, highest_amount_desired_flag):
        amount_responses = defaultdict(set)
        for response, amount in responses_amounts.iteritems():
            amount_responses[amount].add(response)
        amount_list = amount_responses.keys()
        amount_list.sort(reverse=highest_amount_desired_flag)
        correct_index = random.randint(0, min(5, len(amount_list) / 2))
        wrong_responses = []
        for i in range(correct_index + 1, len(amount_list)):
            wrong_responses.extend(amount_responses[amount_list[i]])
        super(ExtremeAmountQuestion, self).__init__(
            amount_responses[amount_list[correct_index]],
            wrong_responses
        )

class HighestAmountQuestion(ExtremeAmountQuestion):
    def __init__(self, responses_amounts):
        super(HighestAmountQuestion, self).__init__(responses_amounts, True)

class LowestAmountQuestion(ExtremeAmountQuestion):
    def __init__(self, responses_amounts):
        super(LowestAmountQuestion, self).__init__(responses_amounts, False)
