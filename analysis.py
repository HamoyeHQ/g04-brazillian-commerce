import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
st.set_option('deprecation.showPyplotGlobalUse', False)


@st.cache
def load_order_data(allow_output_mutation=True):
	  data = pd.read_csv('data/olist_orders_dataset.csv')
	  return data

@st.cache
def load_customer_data(allow_output_mutation=True):
	  data = pd.read_csv('data/olist_customers_dataset.csv')
	  return data

@st.cache
def load_review_data():
	  data = pd.read_csv('data/olist_order_reviews_dataset.csv')
	  return data
@st.cache
def load_payment_data():
	  data = pd.read_csv('data/olist_order_payments_dataset.csv')
	  return data
@st.cache
def load_order_item_data():
	  data = pd.read_csv('data/olist_order_items_dataset.csv')
	  return data
@st.cache
def load_product_data():
	  data = pd.read_csv('data/olist_products_dataset.csv')
	  return data
@st.cache
def load_seller_data():
	  data = pd.read_csv('data/olist_sellers_dataset.csv')
	  return data
@st.cache
def load_geo_data():
	  data = pd.read_csv('data/olist_geolocation_dataset.csv')
	  return data
@st.cache
def load_translation_data():
	  data = pd.read_csv('data/product_category_name_translation.csv')
	  return data

#Load Data
order = load_order_data()
customer = load_customer_data()
review = load_review_data()
payment = load_payment_data()
order_item = load_order_item_data()
product = load_product_data()
seller = load_seller_data()
geo = load_geo_data()
translation = load_translation_data()

#Convert Timestamp Data
order_date=['order_purchase_timestamp', 'order_approved_at',
            'order_delivered_carrier_date', 'order_delivered_customer_date',
            'order_estimated_delivery_date']
for items in order_date:
    order[items] = pd.to_datetime(order[items])

# creating master dataframe 
df1 = payment.merge(order_item, on='order_id')
df2 = df1.merge(product, on='product_id')
df3 = df2.merge(seller, on='seller_id')
df4 = df3.merge(review, on='order_id')
df5 = df4.merge(order, on='order_id')
df6 = df5.merge(translation, on='product_category_name')
df = df6.merge(customer, on='customer_id')



#Customized plotting functions for visualizations
def format_spines(ax, right_border=True):
    
    ax.spines['bottom'].set_color('#666666')
    ax.spines['left'].set_color('#666666')
    ax.spines['top'].set_visible(False)
    if right_border:
        ax.spines['right'].set_color('#FFFFFF')
    else:
        ax.spines['right'].set_color('#FFFFFF')
    ax.patch.set_facecolor('#FFFFFF')

def count_plot(feature, df, colors='Greens_d', hue=False, ax=None, title=''):
    
    # Preparing variables
    ncount = len(df)
    if hue != False:
        ax = sns.countplot(x=feature, data=df, palette=colors, hue=hue, ax=ax)
    else:
        ax = sns.countplot(x=feature, data=df, palette=colors, ax=ax)
        
    format_spines(ax)
    
    # Setting percentage
    for p in ax.patches:
        x=p.get_bbox().get_points()[:,0]
        y=p.get_bbox().get_points()[1,1]

        ax.annotate(y, (x.mean(), y), 
                ha='center', va='bottom') # set the alignment of the text
    
    # Final configuration
    if not hue:
        ax.set_title(df[feature].describe().name + ' Analysis', size=13, pad=15)
    else:
        ax.set_title(df[feature].describe().name + ' Analysis by ' + hue, size=13, pad=15)  
    if title != '':
        ax.set_title(title)       
    plt.tight_layout()
    
    
def bar_plot(x, y, df, colors='Blues_d', hue=False, ax=None, value=False, title=''):
    
    # Preparing variables
    try:
        ncount = sum(df[y])
    except:
        ncount = sum(df[x])
    #fig, ax = plt.subplots()
    if hue != False:
        ax = sns.barplot(x=x, y=y, data=df, palette=colors, hue=hue, ax=ax, ci=None)
    else:
        ax = sns.barplot(x=x, y=y, data=df, palette=colors, ax=ax, ci=None)

    plt.xticks(fontsize=25, fontweight='bold')
    plt.yticks(fontsize=25, fontweight='bold')

    # Setting borders
    format_spines(ax)

    # Setting percentage
    for p in ax.patches:
        xp=p.get_bbox().get_points()[:,0]
        yp=p.get_bbox().get_points()[1,1]
        if value:
            ax.annotate('{:.2f}k'.format(yp/1000), (xp.mean(), yp), 
                    ha='center', va='bottom') # set the alignment of the text
        else:
            ax.annotate('{:.1f}%'.format(100.*yp/ncount), (xp.mean(), yp), 
                    ha='center', va='bottom') # set the alignment of the text
    if not hue:
        ax.set_title(df[x].describe().name + ' Analysis', size=12, pad=15)
    else:
        ax.set_title(df[x].describe().name + ' Analysis by ' + hue, size=12, pad=15)
    if title != '':
        ax.set_title(title)  
    plt.tight_layout()
    
    
def categorical_plot(cols_cat, axs, df):
    
    idx_row = 0
    for col in cols_cat:
        # Returning column index
        idx_col = cols_cat.index(col)

        # Verifying brake line in figure (second row)
        if idx_col >= 3:
            idx_col -= 3
            idx_row = 1

        # Plot params
        names = df[col].value_counts().index
        heights = df[col].value_counts().values

        # Bar chart
        axs[idx_row, idx_col].bar(names, heights, color='navy')
        if (idx_row, idx_col) == (0, 2):
            y_pos = np.arange(len(names))
            axs[idx_row, idx_col].tick_params(axis='x', labelrotation=30)
        if (idx_row, idx_col) == (1, 1):
            y_pos = np.arange(len(names))
            axs[idx_row, idx_col].tick_params(axis='x', labelrotation=90)

        total = df[col].value_counts().sum()
        axs[idx_row, idx_col].patch.set_facecolor('#FFFFFF')
        format_spines(axs[idx_row, idx_col], right_border=False)
        for p in axs[idx_row, idx_col].patches:
            w, h = p.get_width(), p.get_height()
            x, y = p.get_xy()
            axs[idx_row, idx_col].annotate('{:.1%}'.format(h/1000), (p.get_x()+.29*w,
                                            p.get_y()+h+20), color='k')

        # Plot configuration
        axs[idx_row, idx_col].set_title(col, size=12)
        axs[idx_row, idx_col].set_ylim(0, heights.max()+120)

#cleaning up and re-engineering some columns
df['order_purchase_year'] = df.order_purchase_timestamp.apply(lambda x: x.year)
df['order_purchase_month'] = df.order_purchase_timestamp.apply(lambda x: x.month)
df['order_purchase_dayofweek'] = df.order_purchase_timestamp.apply(lambda x: x.dayofweek)
df['order_purchase_hour'] = df.order_purchase_timestamp.apply(lambda x: x.hour)
df['order_purchase_day'] = df['order_purchase_dayofweek'].map({0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'})
df['order_purchase_mon'] = df.order_purchase_timestamp.apply(lambda x: x.month).map({1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'})
df['order_count']=1
df['year_month'] = df['order_purchase_timestamp'].dt.strftime('%Y-%m')

df['ship_duration']=(df['order_delivered_customer_date']-df['order_purchase_timestamp'])/24
df['ship_duration']=df['ship_duration'].astype('timedelta64[h]')

df['tocarrier_duration']=(df['order_delivered_carrier_date']-df['order_purchase_timestamp'])/24
df['tocarrier_duration']=df['tocarrier_duration'].astype('timedelta64[h]')

df['lastmile_duration']=(df['order_delivered_customer_date']-df['order_delivered_carrier_date'])/24
df['lastmile_duration']=df['lastmile_duration'].astype('timedelta64[h]')

df['expected_vs_shipdate']=(df['order_estimated_delivery_date']-df['order_delivered_customer_date'])/24
df['expected_vs_shipdate']=df['expected_vs_shipdate'].astype('timedelta64[h]')

df['expected_duration']=(df['order_estimated_delivery_date']-df['order_purchase_timestamp'])/24
df['expected_duration']=df['expected_duration'].astype('timedelta64[h]')

def main():
	"""
	Main App
	"""

	st.title('Time Series Analysis')

	st.write('''

		*Context: We observed that new user growth has gradually slowed over the last year. In the past few months, 
		customer churn is up to 10% from last year. No obvious change in product or major bug.*

		*Question: why are retailers churning?*

		*Analysis Direction: We will discover the reasons for retailer churn by analyzing three dimensions*:

		1. Customers Analysis: New User, Retention (repeated purchases) - Any trends YoY? Anythings standout by Geo? \n
		2. Order Analysis: Order volume (take into account seasonality) & value \n
		3. Review Analysis: Any significant degrade in CSAT(Customer Satisfaction \n

		''')
	st.subheader('Orders Volume and Sales Analysis')
	st.write("Observations: Order purchase was on a rise throughout 2017, and suddenly came to a plateau in 2018 and has been on a downward trend. Both order's volume and order's value have reduced in 2018.")
	st.write("This reduction on order volume and sales happened very sudden at the start of 2018, across all geos.")

	df_sales = df.groupby(['order_purchase_year', 'order_purchase_month','year_month'], as_index=False).sum().loc[:, ['order_purchase_year', 'order_purchase_month','year_month', 'payment_value','order_count']]

	# fig, ax = plt.subplots(figsize=(20, 4.5))
	ax = px.line(df_sales, x='year_month', y='payment_value', width=1000, height=500,
		title='Brazilian E-Commerce Monthly Sales from 2016 to 2018')
	st.plotly_chart(ax)
	
	ax = px.bar(df_sales, x='year_month', y='payment_value', width=1000, height=500,
		title='Brazilian E-Commerce Monthly Sales from 2016 to 2018')
	st.plotly_chart(ax)

	ax = px.line(df_sales, x='year_month', y='order_count', width=1000, height=500,
		title='Brazilian E-Commerce Monthly Order Volume from 2016 to 2018')
	st.plotly_chart(ax)
	st.write('The trend shows a general increase in volume and sales of products.')

	# Grouping by customer state
	df_cus_count = df.groupby(['order_purchase_year', 'order_purchase_month','year_month'], as_index=False).nunique().loc[:, ['order_purchase_year', 'order_purchase_month','year_month', 'customer_unique_id','seller_id']]
	cus_count = st.button('See customer\'s count per year and month')
	if cus_count:
		st.dataframe(df_cus_count.head(10))

		ax = px.bar(df_cus_count, x='year_month', y='customer_unique_id', title='Brazilian E-Commerce Number of Customers from 2016 to 2018')
		st.plotly_chart(ax)

	df_cus_state = df.groupby(['customer_state','order_purchase_year'], as_index=False).sum().loc[:, ['customer_state','order_purchase_year', 'payment_value']].sort_values(by='payment_value', ascending=False)
	cus_state = st.button('See Customer State')
	if cus_state:
		st.dataframe(df_cus_state.head(10))
		st.write('**Based on the above table, the biggest five states: SP, RJ, MG, RS, and PR Their sale patterns are similar, on the decline. SP dominates the overall sale figure, so let\'s isolate it out.**')

	df_cus_state = df.groupby(['customer_state','year_month'], as_index=False).sum().loc[:, ['customer_state','year_month', 'payment_value']].sort_values(by='payment_value', ascending=False)

	top5 = ['SP', 'RJ','MG','RS','PR']
	df_top5_state = df_cus_state.loc[df_cus_state['customer_state'].isin(top5)]

	for state in top5:
		data=df_top5_state[df_top5_state['customer_state']==state]
		ax = px.line(data, x='year_month', y='payment_value', color='customer_state', width=900, title='Sales from the top 5 states from 2016 to 2018')

		# st.plotly_chart(ax)

	top4_noSP = ['RJ','MG','RS','PR']
	df_top4_noSP = df_cus_state.loc[df_cus_state['customer_state'].isin(top4_noSP)]

	for state in top4_noSP:
		data=df_top5_state[df_top5_state['customer_state']==state]
		ax = px.line(data, x='year_month', y='payment_value', color='customer_state', width=900, title='Sales from the top 5 states from 2016 to 2018')

		# st.plotly_chart(ax)

	st.write('''
			All other top 4 states suffer from the same decline as SP. Since the sale decline happened in 2018 across all states, there could be only two reasons:\n
				1. Competitors launch something in Brazil, attracting customers/sales to their sites. The top 3 states are all trending down in the past 3 to 4 months.\n
				2. There are some serious bugs/business strategy changes \n
			Since the case assumed no major bugs, the first hypothesis is the most reasonable one. This hypothesis is further confirmed here "The company Amazon made its first big move into merchandise in October 2017, when it began offering the use of its Brazilian website to third-party merchants to sell electronics
		''')

	st.subheader('**Sellers**')

	x = px.line(df_cus_count, x='year_month', y='seller_id', width=1100, height=500, title='Brazilian E-Commerce Number of Sellers from 2016 to 2018')
	ax = px.bar(df_cus_count, x='year_month', y='seller_id', width=1100,  height=500, title='Brazilian E-Commerce Number of Sellers from 2016 to 2018')
	st.plotly_chart(ax)

	st.subheader('**Churn Analysis**')

	#Create a dataframe to count how many times a customer shop 
	df_order = df.groupby(['order_id','year_month','order_purchase_year','customer_unique_id'], as_index=False).sum().loc[:, ['order_id','customer_unique_id','year_month','order_purchase_year', 'payment_value']].sort_values(by='year_month', ascending=True)
	df_order['shop_times']=df_order.groupby(['customer_unique_id']).cumcount() + 1 #cumcount() starts at 0, add 1 so that it starts at 1

	df_order_2016 = df_order[df_order['order_purchase_year']==2016]
	df_order_2017 = df_order[df_order['order_purchase_year']==2017]
	df_order_2018 = df_order[df_order['order_purchase_year']==2018]

	df_count_cust = df_order.groupby(['customer_unique_id']).count().reset_index()
	df_count_cust["order_count"] = df_count_cust["order_id"]
	df_count_cust = df_count_cust.drop(["order_id", "year_month", "payment_value", "shop_times","order_purchase_year"], axis=1)
	df_count_cust = df_count_cust.groupby(["order_count"]).count().reset_index().rename(columns={"customer_unique_id": "num_customer"})
	df_count_cust["percentage_customer"] = 100.0 * df_count_cust["num_customer"] / df_count_cust["num_customer"].sum()
	st.dataframe(df_count_cust.head(10))
	st.text('`96% of customers only buy with Olist once :amazed:, which is a big problem.`')

	st.write('The Year **2016**')
	df_count_cust= df_order_2016.groupby(['customer_unique_id']).count().reset_index()
	df_count_cust["order_count"] = df_count_cust["order_id"]
	df_count_cust = df_count_cust.drop(["order_id", "year_month", "payment_value", "shop_times"], axis=1)
	df_count_cust = df_count_cust.groupby(["order_count"]).count().reset_index().rename(columns={"customer_unique_id": "num_customer"})
	df_count_cust["percentage_customer"] = 100.0 * df_count_cust["num_customer"] / df_count_cust["num_customer"].sum()
	st.dataframe(df_count_cust)

	st.write('The Year **2017**')
	df_count_cust= df_order_2017.groupby(['customer_unique_id']).count().reset_index()
	df_count_cust["order_count"] = df_count_cust["order_id"]
	df_count_cust = df_count_cust.drop(["order_id", "year_month", "payment_value", "shop_times"], axis=1)
	df_count_cust = df_count_cust.groupby(["order_count"]).count().reset_index().rename(columns={"customer_unique_id": "num_customer"})
	df_count_cust["percentage_customer"] = 100.0 * df_count_cust["num_customer"] / df_count_cust["num_customer"].sum()
	st.dataframe(df_count_cust)

	st.write('The Year **2018**')
	df_count_cust= df_order_2018.groupby(['customer_unique_id']).count().reset_index()
	df_count_cust["order_count"] = df_count_cust["order_id"]
	df_count_cust = df_count_cust.drop(["order_id", "year_month", "payment_value", "shop_times", 'order_purchase_year'], axis=1)
	df_count_cust = df_count_cust.groupby(["order_count"]).count().reset_index().rename(columns={"customer_unique_id": "num_customer"})
	df_count_cust["percentage_customer"] = 100.0 * df_count_cust["num_customer"] / df_count_cust["num_customer"].sum()
	st.dataframe(df_count_cust)
	st.write('### The Olist stores has new customers every year, but they seem not to continue patronizing them.')

	st.subheader('**RootCause Analysis**')
if __name__ == '__main__':
	main()