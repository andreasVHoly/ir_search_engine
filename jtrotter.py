normalization = True
stemming = True
case_folding = True
log_tf = True
use_idf = True
log_idf = True
use_thesaurus = False
use_Stopword = True
use_largeStopwords = False
use_blindRelevance = True
#10vals




def naive(objects):
    output = []
    if len(objects) == 1:
        return objects.pop()
    else:
        o = objects.pop()
        p = naive(objects)
        for item in p:
            for c in range(0,len(item)):
                itemCopy = item
                itemCopy = itemCopy[0:c] + o + itemCopy[c:]
                #itemcopy.insert(o,c)
                output.append(itemCopy)
    return output

listing = ['a','b','c','d','e','f','g','h','i','j']
#print(naive(listing))

values = [['t','f'],
          ['t', 'f'],
          ['t', 'f'],
          ['t', 'f'],
          ['t', 'f'],
          ['t', 'f'],
          ['t', 'f'],
          ['t', 'f'],
          ['t', 'f'],
          ['t', 'f']]

def altway(objects):
    if len(objects) == 1:
        return objects.pop()
    else:
        result = []
        o = objects.pop()
        other = altway(objects)
        for i in other:
            for c in range(0,len(o)):
                result.append(o.pop(c) + i)
        return result


print(altway(values))