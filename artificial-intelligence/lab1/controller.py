from collections import defaultdict


class Controller:
    def __init__(self,base, view):
        self.aim = None
        self.view = view
        self.base = base
        self.T = defaultdict(list)
        self.features = defaultdict(list)

        for index in range(len(base)):
            self.T[base[index].conclusion[0]].append(index)

        for item in base:
            for k,v in item.condition.items():
                if v not in self.features[k]:
                    self.features[k].append(v)

        for k in self.features.keys():
            self.features[k].append('не знаю')

        self.is_end = False
        self.known = {}
        self.taken_rules = []
        self.stack_aim = []
        self.tresh_rules = []

        self.ans = 'есть ответ'

    def get_stack_aim(self):
        return 'Стек целей: '+str(self.stack_aim)

    def get_known(self):
        return 'Контекстный стек: ' + str(self.known)

    def get_list_aims(self):
        return list(self.T.keys())

    def run(self, aim):
        find_rule = self.T[aim][0]
        self.stack_aim.append((aim, find_rule))
        self.aim = aim
        while not self.is_end:
            is_any_rule = False
            #             print(self.stack_aim)
            #             print(self.known)

            self.view.set_text(self.get_stack_aim() + '\n' + self.get_known() +'\n\n')

            if len(self.stack_aim) > 0 and self.stack_aim[-1][1] >= 0:  # надо еще посмотреть правило
                # анализируем последнее правило в стеке правил
                cur_rule = self.stack_aim[-1][1]
                cur_feat = self.stack_aim[-1][0]
                val_rule = '+'
                cur_rule_conditions = self.base[cur_rule].condition

                for feat_name in cur_rule_conditions.keys():
                    if feat_name not in self.known:
                        val_rule = '?'
                    elif self.known[feat_name] != cur_rule_conditions[feat_name]:
                        val_rule = '-'
                        break

                if val_rule == '?':
                    features = []
                    for feat in self.base[cur_rule].condition.keys():
                        if feat not in self.known:
                            if feat in self.T:
                                rule_indexes = [i for i in self.T[feat] if i not in self.tresh_rules]
                                rule_index = rule_indexes[0]

                            else:
                                rule_index = -1  # у признака нет правила для анализа
                            features.append([feat, rule_index])

                    if len(features) > 0:
                        self.stack_aim.append(features[0])  # первый неизвестный признак

                if val_rule == '-':
                    self.tresh_rules.append(cur_rule)
                    self.stack_aim.pop()
                    rule_indexes = [i for i in self.T[cur_feat] if i not in self.tresh_rules]
                    if rule_indexes:
                        self.stack_aim.append([cur_feat, rule_indexes[0]])
                    else:
                        # если нет подходящего правила
                        self.stack_aim.append([cur_feat, -1])

                if val_rule == '+':
                    self.taken_rules.append(cur_rule)
                    self.stack_aim.pop()
                    feat, val = self.base[cur_rule].conclusion
                    self.known[feat] = val

            else:
                if not is_any_rule:
                    if len(self.stack_aim) == 0:
                        self.is_end = True
                    else:
                        if self.stack_aim[-1][0] == self.aim:
                            self.ans = 'нет ответа'
                        else:
                            question = self.stack_aim[-1][0]
                            self.known[self.stack_aim[-1][0]] = self.view.get_text(question)

                        self.stack_aim.pop()
        # print(self.ans)
        self.view.set_text('\n\n' + self.ans)

