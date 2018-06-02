
# coding: utf-8

# In[92]:



import pandas as pd
import datetime , os

# data_xls = pd.read_excel('master.xls', 'Revised SKU list', index_col=None)
# data_xls.to_csv('master.csv', encoding='utf-8')

master = pd.read_csv("master.csv")
col ={}

s_product = pd.DataFrame()
######################

sku_ids = [326,329,330,365,366,367, 368,369,376,377,378]


#######################

for sku_id in sku_ids:

    sku_ref = master[master['SKU Code'] == sku_id]

#     '''Required once if folder name not in format
#     ######
#     for i in range(len(orginal_folder)):
#         os.rename('media/'+orginal_folder[i], 'media/'+orginal_folder[i].split(' ')[0]) 
#     '''

    if(str(sku_ref['Option1'].item()) != 'nan'):
        colors = sku_ref['Option1'].item().split(',')
    else:
        colors = ['Multicolor']

    # print(colors)

    orginal_folder = [name for name in os.listdir ("media") if '0'+str(sku_id) in name]

    print(orginal_folder)

    images = os.listdir('media/'+orginal_folder[0])


    # image name lower case
    for i in range(len(images)):
        os.rename('media/'+orginal_folder[0]+'/'+images[i], 'media/'+orginal_folder[0]+'/'+images[i].lower()) 

    sides = [ 'Front', 'Back','Left', 'Right', 'Left-chest', 'Right-chest', 'Right-sleeve' , 'Left-sleeve']

    color_images = []

    print(len(colors))
    if len(colors) > 1:
        for color in colors:    
            test=[]
            for side in sides:
                for image in images:
                    if (color.strip().lower() in image) and (side.strip().lower() in image):
                            test.append(image)
            color_images.append(test)
            print(color_images)
    else:
        test=[]
        color_images.append(images)
        print(color_images[0][0])

    def isNaN(num):
        return num != num


    price_list = []
    price_list2 = []
    price_qty = []
    qty_list = [1,10,25,50,100,500,1000,3000]
    custom_list =['Variant quantity','Imprinting details', 'Design code', 'Design cost']

    # colors = sku_ref['Option1'].item().split(',')
    sku = sku_ref['SKU Code'].item()
    now = datetime.datetime.now()

    price_list.append(sku_ref['1 to 9 nos'].item())
    price_list.append(sku_ref['10 to 24 nos'].item())
    price_list.append(sku_ref['25 to 49 nos'].item())
    price_list.append(sku_ref['50 - 99 nos'].item())
    price_list.append(sku_ref['100 - 499 nos'].item())
    price_list.append(sku_ref['500 to 999 nos'].item())
    price_list.append(sku_ref['1000 - 2999 nos'].item())
    price_list.append(sku_ref['> 3000 nos'].item())

    i = 0
    for price in price_list:
        if not isNaN(price):
            price_list2.append(price)
            price_qty.append(qty_list[i])
        i= i+1

    prd_price = price_list2[0]
    first_image = orginal_folder[0]+'/'+color_images[0][0]
    count = 0

    for color in colors:        
        col['sku'] =  col['url_key'] = str(sku)+'-'+color.strip()
        col['_attribute_set'] = 'Newdilsebol'
        col['_type'] = 'simple'
        col['_root_category'] = 'View All'
        col['_product_websites'] = 'base'
        col['created_at'] = col['updated_at']  = now.strftime("%Y-%m-%d %H:%M:%S")
        col['description'] = sku_ref["Spec level Description"].item()
        col['em_deal'] =0
        col['em_hot']=0
        col['em_label_bestseller'] =0
        col['em_label_new'] =0
        col['em_label_saleoff'] =0
        col['has_options'] =1
        col['image'] = first_image
        col['image_label'] ='Front'           
        col['msrp_display_actual_price_type'] = 'Use config'
        col['msrp_enabled'] ='Use config'
        col['name'] =  str(sku_ref["Type"].item())+" "+str(sku_ref['Specs1'].item())+" "+color.strip()
        col['newdilsebolcolor'] = color.strip()
        if(str(sku_ref['Specs1'].item()) != 'nan'):
            col['newdilsebolspec'] = sku_ref['Specs1'].item().strip()
        col['options_container'] = 'Product Info Column'
        col['price'] = prd_price
        col['required_options'] = 0
        col['short_description'] = sku_ref["Type Level Description"].item()
        col['small_image'] = first_image               
        col['small_image_label'] = 'Front'
        col['status'] = '1'          
        col['tax_class_id'] = '6'
        col['thumbnail'] = first_image  
        col['thumbnail_label'] = 'Front' 
        col['visibility'] = '1'
        col['weight'] = int(sku_ref["Avg weight in gms / pc"].item())/1000
        col['qty'] = 5000
        col['min_qty'] = 0
        col['use_config_min_qty'] = 1
        col['is_qty_decimal'] = 0
        col['backorders'] = 0
        col['use_config_backorders'] = 1
        col['min_sale_qty'] =  sku_ref["MOQ"].item()
        col['use_config_min_sale_qty'] = 0
        col['max_sale_qty'] = 0
        col['use_config_max_sale_qty'] = 1
        col['is_in_stock'] = 1
        col['notify_stock_qty'] = 1
        col['use_config_notify_stock_qty'] = 1
        col['manage_stock'] = 1
        col['use_config_manage_stock'] = 1
        col['stock_status_changed_auto'] = 0
        col['use_config_qty_increments'] = 1
        col['qty_increments'] = 0
        col['use_config_enable_qty_inc'] = 1
        col['enable_qty_increments'] = 0
        col['is_decimal_divided'] = 0


        max_list =[len(color_images[count]),len(custom_list),len(price_list2) ]
        for i in range(max(max_list)):
            if len(custom_list) > i:
                col['_custom_option_type'] ='field' 
                col['_custom_option_title'] =custom_list[i] 
                col['_custom_option_is_required'] = '0' 
                col['_custom_option_price'] = 0 
                col['_custom_option_max_characters'] = 0  
                col['_custom_option_sort_order'] = 0 

            if len(color_images[count]) > i:

                col['_media_image'] = orginal_folder[0]+'/'+color_images[count][i]
                col['_media_lable'] = sides[i]
                col['_media_position'] = i+1
                col['_media_is_disabled'] = 0
                col['_media_attribute_id'] = 88

            if len(price_qty) > i:
                col['_tier_price_website'] = 'all'    
                col['_tier_price_customer_group'] = 'all'
                col['_tier_price_qty'] = price_qty[i]
                col['_tier_price_price'] = price_list2[i]

            s_product = s_product.append(col, ignore_index=True)
            col ={}
        count =count+1

    try:
        os.remove(str(sku_id)+".csv")
    except OSError:
        pass

    s_product.to_csv(str(sku_id)+'.csv',index=False)
    print('finished')

