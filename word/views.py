from django.http import HttpResponse
from django.shortcuts import render
from itertools import permutations
from django.core.cache import cache
import redis_lock
import redis
from redis import StrictRedis

#def permutations(string, step = 0):
#    # if we've gotten to the end, print the permutation
#    if step == len(string):
#        print " ".join(string)
#
#    # everything to the right of step has not been swapped yet
#    for i in range(step, len(string)):
#
#        # copy the string (store as array)
#        string_copy = [character for character in string]
#
#        # swap the current index with the step
#        string_copy[step], string_copy[i] = string_copy[i], string_copy[step]
#
#        # recurse on the portion of the string that has not been swapped yet (now it's index will begin with step + 1)
#        permutations(string_copy, step + 1)

def getword(request):
   word=request.POST.get('word','');
   perms = [''.join(p) for p in permutations(word)]
   perms_no_repeat = [''.join(q) for q in set(permutations(word))]

   # Add redis lock
   conn = StrictRedis(host='127.0.0.1',port=6331)
   lock = redis_lock.Lock(conn, "hcountlock")
   if lock.acquire(blocking=False):
       print("Got the lock.")
       http_count = cache.get('hcount')
       if http_count is None:
           cache.set('hcount', str(0))

       new_count = int(http_count) + 1
       cache.set('hcount', str(new_count))

       # release redis lock
       lock.release()
       return render(request,'word.html',{'word': perms, 'word_no_repeat': perms_no_repeat})
   else:
       print("Other instance has the lock.")
       return render(request,'word.html',{})








