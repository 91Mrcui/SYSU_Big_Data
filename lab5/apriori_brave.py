#!/usr/bin/env python
import time

class APRIORI():
    # initializing 
    def __init__(self, minsupp, minconf):
        self.transactions=[]
        self.minsupp = float(minsupp)
        self.minconf = float(minconf)
        self.itemsets = []
        self.rules ={}

    def load_transactions(self, csv_file):
        first_itemsets = dict()
        for readline in open(csv_file, 'r',encoding='utf-8'):
            for line in readline.split('\r'):
                t = line.strip().split(',')
                self.transactions.append(set(t))
                for item in t:
                    item_set = frozenset([item])
                    if item_set not in first_itemsets:
                        first_itemsets[item_set]=1
                    else:
                        first_itemsets[item_set]+=1
        self.itemsets.append(first_itemsets)
        #print(self.itemsets)
        self.correct_first_itemset()

    #removes the itemsets below the given support value
    def correct_first_itemset(self):
        num_of_transactions  = len(self.transactions)
        first_itemset = self.itemsets[0]
        for item in list(first_itemset.keys()):
            #print("1")
            support_value = float(first_itemset[item])/num_of_transactions
            #print(support_value)
            if support_value < self.minsupp:
                del first_itemset[item]
            else:
                first_itemset[item] = support_value
        self.itemsets[0] = first_itemset
        self.itemsets=self.itemsets[:90000]
        #print(self.itemsets)

    #iteratively adds itemsets using the previous itemsets
    def get_itemsets(self):
        prev_itemset = self.itemsets[0].keys()
        num_of_transactions = len(self.transactions)
        #print(prev_itemset)
        while len(prev_itemset) != 0:
            #print(len(list(prev_itemset)[0]))
            new_set_len = len(list(prev_itemset)[0])+1
            candidate_itemsets = dict()
            for i in range(0, len(prev_itemset)):
                for j in range(i+1, len(prev_itemset)):
                    present_set = list(prev_itemset)[i] | list(prev_itemset)[j]
                    if len(present_set) is new_set_len:
                        count = 0
                        for itemset in prev_itemset:
                            if itemset <= present_set:
                                count += 1
                        if count == len(present_set):
                            candidate_itemsets[present_set] = 0

            if len(candidate_itemsets) != 0:
                for t in self.transactions:
                    for itemset in candidate_itemsets:
                        if itemset <= t:
                            candidate_itemsets[itemset] += 1
                for itemset in list(candidate_itemsets.keys()):
                    support_value = float(candidate_itemsets[itemset])/num_of_transactions
                    if support_value < self.minsupp:
                        del candidate_itemsets[itemset]
                    else:
                        candidate_itemsets[itemset] = support_value
            if len(candidate_itemsets) != 0:
                self.itemsets.append(candidate_itemsets)
            prev_itemset = candidate_itemsets.keys()

    #function generates rules and checks for minimum confidence values
    def get_rules(self):
        self.get_itemsets()
        for itemsets in self.itemsets[1:]:
            for itemset in itemsets.keys():
                for item in itemset:
                    left_items = itemset - frozenset([item])
                    num = self.itemsets[len(itemset) - 1][itemset]
                    num_total = self.itemsets[len(left_items) - 1][left_items]
                    conf = float(num) / num_total
                    if conf >= self.minconf:
                        line = "[" + ", ".join(list(left_items)) + "] => [" + item + "] (Conf: "+str(conf * 100) + "%, Supp: " + str ((itemsets[itemset] * 100)) + "%)"
                        self.rules[line] = conf


    def __key_itemset(self, t):
        return self.itemsets[len(t) - 1][t]

    def __key_rule(self, t):
        return self.rules[t]


    # getting itemset confidence values
    def get_itemset_val(self, t):
        return self.itemsets[len(t) - 1][t]

    # getting the rule values
    def get_rule_val(self, t):
        return self.rules[t]

    # printing the required file
    def print_result(self):
        print('\n==High-confidence association rules (min_conf='+str(self.minconf*100)+'%)')
        rules_ordered = sorted(self.rules.keys(), key = self.__key_rule, reverse = True)
        rules_ordered = sorted(self.rules.keys(), key = self.get_rule_val, reverse = True)
        for rules in rules_ordered:
            print(rules)


if __name__ == '__main__':
    
    data="data.csv"
    min_sup=0.4
    min_conf=0.5

    miner = APRIORI(min_sup, min_conf)
    miner.load_transactions(data)
    time_start = time.time() #开始计时
    miner.get_rules()
    time_end = time.time() 
    miner.print_result()
    print(f"\nusing time: {1000*(time_end-time_start):.4f} ms")