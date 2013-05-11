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


    counter =0
    print '\n'
    if len(tweet_list)==0:
       print 'Sorry No Match'
    else:
        for range_value in range(0,len(tweet_list)):
            print('user:%s\ttweet:%s\ttweet_id:%s\tscore:%s'%(tweet_list[range_value][3],tweet_list[range_value][4],tweet_list[range_value][0],tweet_list[range_value][1]))
            print '\n'
            counter+=1
            if counter==50:
               break
           
    return tweet_list


def main():
    
    twt_lt=vector_retrieval();
       
   

if __name__ == '__main__':
  main()
