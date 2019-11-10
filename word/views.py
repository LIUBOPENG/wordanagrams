from django.http import HttpResponse
from django.shortcuts import render
from itertools import permutations

def getword(request):
   word=request.POST.get('word','');
   print(word)
   perms = [''.join(p) for p in permutations(word)]
   perms_no_repeat = [''.join(q) for q in set(permutations(word))]
   return render(request,'word.html',{'word': perms, 'word_no_repeat': perms_no_repeat})






