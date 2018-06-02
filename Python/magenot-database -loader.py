
# coding: utf-8

# In[19]:


import pandas as pd
import MySQLdb as my

master = pd.read_csv("master.csv")

''' variables'''
##################
sku_ids   = [ 361 ]  # add skud id 
magento_id= [ '2102'] # add magento id of the configarable product
################


'''Database connection'''
db = my.connect(host="127.0.0.1",user="root",passwd="root",db="dilsebol2")
cursor = db.cursor()
cursor.execute("SELECT relation_id FROM `printing_method_sku` ORDER BY `relation_id` DESC LIMIT 1 ");
(relation_id ,)=cursor.fetchone()
db.close()

production_time=[1,9,10,24,25,49,50,99,100,499,500,999,1000,2999,3000]

for r in range(len(sku_ids)):

    sku_ref = master[master['SKU Code'] == sku_ids[r]]


# #     ####################  Production time table  ###############
    print()


    a= b= sku_ref['1 to 9'].item()
    c= d= sku_ref['10 to 24'].item()
    e= f= sku_ref['25 to 49'].item()
    g= h= sku_ref['50 – 99'].item()
    i= j= sku_ref['100 – 499'].item()
    k= l= sku_ref['500 to 999'].item()
    m= n= sku_ref['1000 – 2999'].item()
    o  =  sku_ref['> 3000'].item()

    values =[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o]

    def isNaN(num):
        return num != num

    print("INSERT INTO `productiontime` (`pid`, `qty`, `time`) VALUES")
    for i in range(len(values)):
        if not isNaN(values[i]):
            if(i < len(values)-1):
                print("('"+magento_id[r]+"',"+str(production_time[i])+","+str(int(values[i]))+"),")    
            else:
                rr = values[i].split('>')[1]
                print("('"+magento_id[r]+"',"+str(production_time[i])+","+str(int(rr))+");")    


    ################    Varient table    ###############     
    print()
    size = sku_ref['Option2'].item()

    print("INSERT INTO `varient` (`skuid`, `varientname`, `options`) VALUES")
    if not isNaN(size):
        print("('"+magento_id[r]+"','size','"+str(size)+"');")    
    else:
        print("('"+magento_id[r]+"','size','Qty');")

#     ################# Printing method table ################
    print() 
    areas = sku_ref['Design area'].item()
    printing_methods=sku_ref['Applicable Imprinting method ID'].item()
    printing_methods =printing_methods.split(',')

    areas = areas.split(',')

    print("INSERT INTO `printing_method_sku` (`relation_id`, `sku_id`, `ref_id`, `side`) VALUES")
    for j in range(len(printing_methods)):
        for i in range(len(areas)):
            relation_id = relation_id+1
            if( i == len(areas)-1 and j == len(printing_methods)-1 ):
                print( "("+str(relation_id)+",'"+str(magento_id[r])+"',"+str(printing_methods[j].strip())+",'"+areas[i].strip()+"');" )
            else:
                 print( "("+str(relation_id)+",'"+str(magento_id[r])+"',"+str(printing_methods[j].strip())+",'"+areas[i].strip()+"')," )
            

