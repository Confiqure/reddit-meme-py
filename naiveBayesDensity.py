  
# 
#  Naive Bayes Basic Classifier 
#


# _____________________________________________________________________

import math

class Classifier:
    def __init__(self, filename, dataFormat):

        """ a classifier will be built from file specified. dataFormat is a
        string that describes how to interpret each line of the data files.
        For example, for the iHealth data with salary the format is:
        "attr	attr	attr	attr	num	class"
        """
   
        total = 0
        classes = {}
        counts = {}
        # counts used for attributes that are not numeric
        counts = {}
        # totals used for attributes that are numereric
        # we will use these to compute the mean and sample standard deviation for
        # each attribute - class pair.
        totals = {}
        numericValues = {}        
        
        # reading the data in from the file
        
        self.format = dataFormat.strip().split('\t')
        self.prior = {}
        self.conditional = {}
        f = open(filename)
        lines = f.readlines()
        f.close()
        for line in lines:
            fields = line.strip().split('\t')
            ignore = []
            vector = []
            nums = []            
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    nums.append(float(fields[i]))
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
            totals.setdefault(category, {})
            numericValues.setdefault(category, {})            
            classes[category] += 1
            #print(total, classes)
            # now process each non-numeric attribute of the instance
            col = 0
            for columnValue in vector:
                col += 1
                counts[category].setdefault(col, {})
                counts[category][col].setdefault(columnValue, 0)
                counts[category][col][columnValue] += 1
            # process numeric attributes
            col = 0
            for columnValue in nums:
                col += 1
                totals[category].setdefault(col, 0)
                #totals[category][col].setdefault(columnValue, 0)
                totals[category][col] += columnValue
                numericValues[category].setdefault(col, [])
                numericValues[category][col].append(columnValue)                
    
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
        self.tmp =  counts               

        #
        # now compute mean and sample standard deviation
        #
        self.means = {}
        self.ssd = {}
        #self.totals = totals
        for (category, columns) in totals.items():
            self.means.setdefault(category, {})
            for (col, cTotal) in columns.items():
                self.means[category][col] = cTotal / classes[category]
        # standard deviation
        
        for (category, columns) in numericValues.items():
            
            self.ssd.setdefault(category, {})
            for (col, values) in columns.items():
                SumOfSquareDifferences = 0
                theMean = self.means[category][col]
                for value in values:
                    SumOfSquareDifferences += (value - theMean)**2
                columns[col] = 0
                self.ssd[category][col] = math.sqrt(SumOfSquareDifferences / (classes[category]  - 1))    

    def classify(self, itemVector, numVector):
        """Return class we think item Vector is in"""
        results = []
        sqrt2pi = math.sqrt(2 * math.pi)
        for (category, prior) in self.prior.items():
            prob = prior
            col = 1
            for attrValue in itemVector:
                if not attrValue in self.conditional[category][col]:
                    # we did not find any instances of this attribute value
                    # occurring with this category so prob = 0
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1
            col = 1
            for x in  numVector:
                mean = self.means[category][col]
                ssd = self.ssd[category][col]
                if ssd != 0:
                    ePart = math.pow(math.e, -(x - mean)**2/(2*ssd**2))
                    prob = prob * ((1.0 / (sqrt2pi*ssd)) * ePart)
                col += 1
            results.append((prob, category))
        # return the category with the highest probability
        #print(results)
        return(max(results)[1])
   



