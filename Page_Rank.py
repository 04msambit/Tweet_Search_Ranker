import sys
import simplejson
import difflib
import re
import collections
import math
import numpy
import operator

def page_rank():
    
    
    user_list=collections.defaultdict(list)
    d=collections.defaultdict(list)
    old_page_rank = collections.defaultdict(float)
    new_page_rank = collections.defaultdict(float)

    user_name_dictionary = collections.defaultdict(float)


    filename = sys.argv[1]
    flag=1

    
    # Loop over all lines
    f = file(filename, "r")
    lines = f.readlines()
    for line in lines:
       
             tweet = simplejson.loads(line)
             user_name = tweet['user']['screen_name']
             user  = tweet['user']['id']
             user_id = tweet['user']['id']
             
          
             if user not in user_name_dictionary:
                user_name_dictionary[user]=user_name
                 
             if user_id not in old_page_rank:
                old_page_rank[user_id]=1


             refer= tweet['entities']['user_mentions']
                    
             d[user]=[]
             for val in range(0,len(refer)):
                 d[user].append(refer[val]['id'])
                 if refer[val]['id'] not in old_page_rank:
                    old_page_rank[refer[val]['id']]=1
             
             if user in user_list:
                for value in d[user]:
                    if value not in user_list[user]:
                       user_list[user].append(value)
             else:
                user_list[user]=[]
                for vall in d[user]:
                    if vall not in user_list[user]:
                       user_list[user].append(vall)
                          


             d={}
    
    new_page_rank = old_page_rank.copy()

    for key in new_page_rank:
        new_page_rank[key]=0

    

    # We will start to build the new page rank table here
    
    number_of_iterations = 0
    
    while(flag):
    
      for key in user_list:
          for iter_value in user_list[key]:
              new_rank_value = float(old_page_rank[key]) / float(len(user_list[key]))
              new_page_rank[iter_value]+=new_rank_value
      # We will check for precision here with old_page_rank

      for kl in new_page_rank:
          new_page_rank[kl] = float(new_page_rank[kl]) * float(0.85)
          new_page_rank[kl]+=float(0.15)
          new_page_rank[kl] = float(new_page_rank[kl] * 0.9) + float((0.1)/float(len(new_page_rank)))
      
      flg=1
      
      for key in new_page_rank:
          compare_value = float(abs((new_page_rank[key] - old_page_rank[key])))
          if compare_value > 0.0000001:
             flg=0
             break
             
      old_page_rank = new_page_rank
      number_of_iterations+=1
      
      if(flg):
        flag=0
    
    sorted_new_page_rank = sorted(new_page_rank.items(), key=operator.itemgetter(1),reverse=True)


    counter=0

    print 'Users Ranked according to Page Rank Score are:\n'
       
    for iter in range(0,len(sorted_new_page_rank)):
        print ("id:%s\tscreen_name:%s" % (sorted_new_page_rank[iter][0], user_name_dictionary[sorted_new_page_rank[iter][0]]))
        counter+=1
    
        if(counter==50):
          break
    
        
    return sorted_new_page_rank



def main():
    
    usr_lt=page_rank();
         
   

if __name__ == '__main__':
  main()
