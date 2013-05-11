import sys
import simplejson
import difflib
import re
import collections
import math
import numpy
import operator


def vector_retrieval():
    
    filename = sys.argv[1]
 
    tweets_text = [] # We will store the text of every tweet in this list
    small_collection= []
    count=0
    idf_dictionary=collections.defaultdict(float)
    d=collections.defaultdict(float)
    dic=collections.defaultdict(float)
    text_id_dictionary={}
    dictionary_list=[]
    sum_square_query=0
    
    # Loop over all lines
    f = file(filename, "r")
    lines = f.readlines()
    for line in lines:
        try:
                tweet = simplejson.loads(line)
                         
                # Fetch text from tweet
                text = tweet["text"].lower()
                screen_name=tweet['user']['screen_name']
                tweet_id   = tweet['id']
                user_id = tweet['user']['id']
                text_id_dictionary[tweet_id]=(screen_name,text)             
                list2=[]
                list2=re.findall(r"[\w']+",text)
                set_list=set(list2);
                for word in set_list:
                    if idf_dictionary.has_key(word):     
                       idf_dictionary[word]+=1;
                    else:
                       idf_dictionary[word]=1;
                
                # We will create a term frequency dictionary here

                for wrd in list2:
                    if  wrd not in d:
                        d[wrd]=1
                    else:
                        d[wrd]+=1

                # Now we will convert it to log form

                for ky in d:
                    value = d[ky]
                    d[ky]=1+float(math.log(value,2))
                
                dictionary_list.append((tweet_id,d,user_id));
                d={}   # We will have to reuse the dictionary so we need to empty it first
                count+=1
                tweets_text.append( text )
                
 
        except ValueError:
               pass

      
     
    
    for key in idf_dictionary:
        val = count/float(idf_dictionary[key])
        idf_dictionary[key]=math.log(val,2)
   
    

    for single_list in dictionary_list:
        for key in single_list[1]:
            idf_value = idf_dictionary[key]    # We are getting the idf value for that term
            single_list[1][key] = float(single_list[1][key]) * float(idf_value)
            
    


    query_term=raw_input('\nInput Query\n')
    input_query=query_term.split()
    
    
    # We will create a trem frequency dictionary here

    for wrd in input_query:
      if  wrd not in dic:
          dic[wrd]=1
      else:
          dic[wrd]+=1

    # Now we will convert it to log form

    for ky in dic:
        value = dic[ky]
        dic[ky]=1+float(math.log(value,2))

    for kk in dic:
        if kk in idf_dictionary:
          
           idf_value = idf_dictionary[kk]    # We are getting the idf value for that term
        else:
            idf_value =0
        dic[kk] = dic[kk] * idf_value
        sum_square_query += dic[kk] * dic[kk]

    
    sum_square_query=math.sqrt(sum_square_query);    

    

    
    sum_val =0
    denominator=0
    score_doc_list=[]
    score_doc=0
    tweet_list=[]
    counter=0
    for singl_list in dictionary_list:
        denominator=0
        sum_val=0
        for key_dic in singl_list[1]:
            denominator+=singl_list[1][key_dic] * singl_list[1][key_dic]
        for kl in dic:
            if kl in singl_list[1]:
               
               sum_val+=dic[kl]*singl_list[1][kl]
            else:
               sum_val+=0

        mult_denominator=sum_square_query * math.sqrt(denominator)   
        if(mult_denominator!=0):      
          score_doc=sum_val/(sum_square_query * math.sqrt(denominator))
        
        
        if score_doc!=0:
           score_doc_list.append((singl_list[0],score_doc,singl_list[2]));
           
           counter+=1


    

    score_doc_list.sort(key=lambda x: x[1])

    score_doc_list.reverse()

   
    tweet_list=[]
    for element in score_doc_list:
        tweet_list.append((element[0],element[1],element[2],text_id_dictionary[element[0]][0],text_id_dictionary[element[0]][1]))

    if len(tweet_list)==0:
       print 'Sorry No Match'
 
       
    
    return tweet_list

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
          new_page_rank[kl]+=0.15
          new_page_rank[kl] = float(new_page_rank[kl] * 0.9) + float((0.1)/float(len(new_page_rank)))
      
      flg=1
      
      for key in new_page_rank:
          compare_value = abs((new_page_rank[key] - old_page_rank[key]))
          if compare_value > 0.0000001:
             flg=0
             break
             
      old_page_rank = new_page_rank
      number_of_iterations+=1
      
      if(flg):
        flag=0
    
    sorted_new_page_rank = sorted(new_page_rank.items(), key=operator.itemgetter(1),reverse=True)
    
        
    return sorted_new_page_rank

def integrated_rank(twts_input,usr_input):
    
    integrated_tuple=[]
    flag = 0
    counter = 0
    
    for element in twts_input:
        list_tweets=[]
        flag=0
        face_value=0
        for elem in usr_input:
            if element[2]==elem[0]:
               list_tweets.append(element[4])
               name_value=element[3]
               face_value = float(float(0.6 * element[1]) * float(0.4 *elem[1]))
               flag=1
        if(flag==1):
              integrated_tuple.append((element[2],face_value,list_tweets,name_value))
              counter+=1
   
        if counter == 50:
           break

    
    integrated_tuple.sort(key=lambda x: x[1])
    integrated_tuple.reverse()
  
    if len(twts_input)!=0:
     print 'We will display the query results integrated with page rank of users\n'

    for iter_element in integrated_tuple:
        print('name:%s\t tweets:%s'%(iter_element[3],iter_element[2]))
        print '\n'

    return

def main():
    
    print 'Welcome to Integrated Page Rank System..!!!\n'
    
    twt_lt=vector_retrieval();
    usr_lt=page_rank();
    
    integrated_rank(twt_lt,usr_lt)  
   

if __name__ == '__main__':
  main()
