#
#  Naive Bayes Basic Classifier 
#


# _____________________________________________________________________

class Classifier:
    def __init__(self, filename, data_format):

        """ a classifier will be built from file specified. data_format is a string that
        describes how to interpret each line of the data files. For example,
        for the iHealth data the format is:
        "attr	attr	attr	attr	class"
        """

        total = 0
        classes = {}
        counts = {}

        # reading the data in from the file

        self.format = data_format.strip().split('\t')
        self.prior = {}
        self.conditional = {}
        f = open(filename)
        lines = f.readlines()
        f.close()
        for line in lines:
            fields = line.strip().split('\t')
            ignore = []
            vector = []
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    vector.append(float(fields[i]))
                elif self.format[i] == 'attr':
                    vector.append(fields[i])
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    category = fields[i]
            # now process this instance
            total += 1
            classes.setdefault(category, 0)
            counts.setdefault(category, {})
            classes[category] += 1
            # print(total, classes)
            # now process each attribute of the instance
            col = 0
            for columnValue in vector:
                col += 1
                counts[category].setdefault(col, {})
                counts[category][col].setdefault(columnValue, 0)
                counts[category][col][columnValue] += 1

        #
        # ok done counting. now compute probabilities
        #
        # first prior probabilities p(h)
        #
        for (category, count) in classes.items():
            self.prior[category] = count / total
        #
        # now compute conditional probabilities p(D|h)
        #
        for (category, columns) in counts.items():
            self.conditional.setdefault(category, {})
            for (col, valueCounts) in columns.items():
                self.conditional[category].setdefault(col, {})
                for (attrValue, count) in valueCounts.items():
                    self.conditional[category][col][attrValue] = (
                            count / classes[category])
        self.tmp = counts

    def classify(self, item_vector):
        """Return class we think item Vector is in"""
        results = []
        for (category, prior) in self.prior.items():
            prob = prior
            col = 1
            for attrValue in item_vector:
                if attrValue not in self.conditional[category][col]:
                    # we did not find any instances of this attribute value
                    # occurring with this category so prob = 0
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1
            results.append((prob, category))
        # return the category with the highest probability
        return max(results)[1]
