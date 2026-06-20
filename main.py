"""
TASK 3: DATA VISUALIZATION - Complete Modular Solution
Each section directly maps to specific task requirements
Books dataset from previous scraping tasks
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('books_custom.csv')
df['price_numeric'] = df['price'].str.replace('£', '').astype(float)
df['in_stock'] = df['availability'].str.contains('In stock')

print(f"🎨 TASK 3: Visualizing {len(df)} books")


# SECTION 1: Transform raw data into visual formats

print("\n📊 SECTION 1: RAW DATA → CHARTS & GRAPHS")
fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# 1a. Raw price data → Histogram
ax1.hist(df['price_numeric'], bins=25, alpha=0.7, color='skyblue', edgecolor='navy')
ax1.set_title('1. RAW → Histogram\nPrice Distribution', fontweight='bold', fontsize=12)
ax1.set_xlabel('Price (£)')
ax1.axvline(df['price_numeric'].mean(), color='red', linestyle='--', label='Mean')
ax1.legend()

# 1b. Raw ratings → Pie chart
rating_pct = df['rating'].value_counts()
ax2.pie(rating_pct.values, labels=rating_pct.index, autopct='%1.1f%%', startangle=90)
ax2.set_title('1. RAW → Pie Chart\nRating Distribution', fontweight='bold', fontsize=12)

# 1c. Raw stock → Bar chart
stock_counts = df['in_stock'].value_counts()
ax3.bar(['In Stock', 'Out of Stock'], stock_counts.values, color=['green', 'red'], alpha=0.8)
ax3.set_title('1. RAW → Bar Chart\nStock Status', fontweight='bold', fontsize=12)
ax3.set_ylabel('Count')

plt.tight_layout()
plt.savefig('section1_raw_to_visuals.png', dpi=300)
plt.show()

# SECTION 2: Use tools like Matplotlib, Seaborn

print("\n🛠️ SECTION 2: MULTIPLE VISUALIZATION TOOLS")
fig2, axes = plt.subplots(2, 2, figsize=(16, 12))

# 2a. Matplotlib line plot
rating_order = ['One', 'Two', 'Three', 'Four', 'Five']
price_means = [df[df['rating']==r]['price_numeric'].mean() for r in rating_order]
axes[0,0].plot(rating_order, price_means, marker='o', linewidth=3, markersize=10)
axes[0,0].set_title('2a. MATPLOTLIB: Price Trend by Rating', fontweight='bold')
axes[0,0].set_ylabel('Avg Price (£)')

# 2b. Seaborn boxplot
sns.boxplot(data=df, x='rating', y='price_numeric', ax=axes[0,1], order=rating_order)
axes[0,1].set_title('2b. SEABORN: Price by Rating', fontweight='bold')

# 2c. Seaborn heatmap
price_bins = pd.cut(df['price_numeric'], bins=5)
heatmap_data = pd.crosstab(price_bins, df['rating'])
sns.heatmap(heatmap_data, annot=True, fmt='d', ax=axes[1,0], cmap='Blues')
axes[1,0].set_title('2c. SEABORN: Heatmap', fontweight='bold')

# 2d. Matplotlib scatter
colors = {'True':'green', 'False':'red'}
axes[1,1].scatter(df['price_numeric'], df['rating'].map({'Five':5,'Four':4,'Three':3,'Two':2,'One':1}),
                 c=df['in_stock'].map(colors), alpha=0.6)
axes[1,1].set_title('2d. MATPLOTLIB: Price vs Rating Color=Stock', fontweight='bold')
axes[1,1].set_xlabel('Price (£)')

plt.tight_layout()
plt.savefig('section2_tools_demo.png', dpi=300)
plt.show()


# SECTION 3: Design visuals that enhance understanding

print("\n👁️ SECTION 3: ENHANCED UNDERSTANDING VISUALS")
fig3 = plt.figure(figsize=(20, 15))
gs = GridSpec(3, 3, figure=fig3, hspace=0.3, wspace=0.3)

# 3a. Annotated distribution with statistics
ax3a = fig3.add_subplot(gs[0,0])
n, bins, patches = ax3a.hist(df['price_numeric'], bins=30, alpha=0.7)
ax3a.axvline(df['price_numeric'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: £{df["price_numeric"].mean():.1f}')
ax3a.axvline(df['price_numeric'].median(), color='orange', linestyle='--', linewidth=2, label=f'Median: £{df["price_numeric"].median():.1f}')
ax3a.text(0.02, 0.98, f'Skew: {df["price_numeric"].skew():.2f}\nOutliers: {len(df[df["price_numeric"]>df["price_numeric"].quantile(0.95)]):,}', 
          transform=ax3a.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat'))
ax3a.set_title('3a. ENHANCED HISTOGRAM\nStatistics + Annotations', fontweight='bold')
ax3a.legend()

# 3b. Clear business bar chart
ax3b = fig3.add_subplot(gs[0,1])
segment_counts = pd.cut(df['price_numeric'], bins=[0,25,40,55,100]).value_counts()
bars = ax3b.bar(segment_counts.index, segment_counts.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
ax3b.set_title('3b. BUSINESS SEGMENT ANALYSIS', fontweight='bold')
ax3b.set_ylabel('Book Count')
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax3b.text(bar.get_x() + bar.get_width()/2., height + 10, f'{int(height)}', 
              ha='center', va='bottom', fontweight='bold')

# 3c. Insight-focused bubble chart
ax3c = fig3.add_subplot(gs[0,2])
bubble_sizes = df['price_numeric'] * 10
scatter = ax3c.scatter(df['price_numeric'], 
                      pd.to_numeric(df['rating'].map({'Five':5,'Four':4,'Three':3,'Two':2,'One':1}), errors='coerce'),
                      s=bubble_sizes, alpha=0.6, c=df['in_stock'].astype(int), cmap='RdYlGn')
ax3c.set_title('3c. INSIGHT BUBBLES\nSize=Price, Color=Stock', fontweight='bold')
ax3c.set_xlabel('Price (£)')
plt.colorbar(scatter, ax=ax3c, label='In Stock')

plt.savefig('section3_enhanced_visuals.png', dpi=300)
plt.show()


# SECTION 4: Craft compelling data stories

print("\n📖 SECTION 4: DATA STORYTELLING")
fig4, axes = plt.subplots(2, 2, figsize=(18, 14))

# 4a. Story: "Price vs Quality Tradeoff"
axes[0,0].scatter(df[df['in_stock']]['price_numeric'], 
                 pd.to_numeric(df[df['in_stock']]['rating'].map({'Five':5,'Four':4,'Three':3,'Two':2,'One':1}), errors='coerce'),
                 c='green', alpha=0.7, label='In Stock', s=50)
axes[0,0].scatter(df[~df['in_stock']]['price_numeric'], 
                 pd.to_numeric(df[~df['in_stock']]['rating'].map({'Five':5,'Four':4,'Three':3,'Two':2,'One':1}), errors='coerce'),
                 c='red', alpha=0.7, label='Out of Stock', s=50)
axes[0,0].set_title('STORY 1: Price-Quality Sweet Spot\nGreen zone = Best opportunities', fontweight='bold', fontsize=12)
axes[0,0].set_xlabel('Price (£)')
axes[0,0].set_ylabel('Rating (1-5)')
axes[0,0].legend()
axes[0,0].axvspan(30, 55, alpha=0.2, color='green', label='Optimal Zone')

# 4b. Story: "Rating Dominance"
rating_stats = df.groupby('rating')['price_numeric'].agg(['count', 'mean', 'std']).round(1)
x_pos = np.arange(len(rating_stats))
axes[0,1].bar(x_pos - 0.2, rating_stats['count']/10, 0.4, label='Volume (x10)', alpha=0.8)
axes[0,1].bar(x_pos + 0.2, rating_stats['mean'], 0.4, label='Avg Price', alpha=0.8)
axes[0,1].set_title('STORY 2: 5-Star Market Dominance\nVolume + Revenue Leader', fontweight='bold', fontsize=12)
axes[0,1].set_xticks(x_pos)
axes[0,1].set_xticklabels(rating_stats.index)
axes[0,1].legend()

plt.tight_layout()
plt.savefig('section4_data_stories.png', dpi=300)
plt.show()


# SECTION 5: Build portfolio with impactful visualsprint("\n💼 SECTION 5: PORTFOLIO-READY MASTERPIECE")
fig5 = plt.figure(figsize=(22, 16))

# Master dashboard combining all insights
gs5 = GridSpec(3, 4, figure=fig5, hspace=0.4, wspace=0.3)

# 5a. Executive KPI cards
ax5a = fig5.add_subplot(gs5[0,:2])
ax5a.axis('off')
kpis = [
    f"TOTAL BOOKS: {len(df):,}",
    f"AVG PRICE: £{df['price_numeric'].mean():.0f}",
    f"TOP RATING: {df['rating'].mode()[0]}",
    f"STOCK RATE: {df['in_stock'].mean():.0%}",
    f"PRICE SKEW: {df['price_numeric'].skew():.1f}"
]
for i, kpi in enumerate(kpis):
    ax5a.text(0.1, 0.9 - 0.18*i, kpi, fontsize=16, fontweight='bold',
              bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
ax5a.set_title('PORTFOLIO EXECUTIVE SUMMARY', fontsize=20, fontweight='bold', pad=20)

# 5b. Master correlation matrix
ax5b = fig5.add_subplot(gs5[1,0])
correlation_data = pd.crosstab(pd.cut(df['price_numeric'], bins=5), df['rating'], normalize='index')
sns.heatmap(correlation_data, annot=True, fmt='.1%', cmap='RdYlGn', ax=ax5b)
ax5b.set_title('PRICE-RATING MATRIX', fontweight='bold')

plt.suptitle('💎 DATA SCIENCE PORTFOLIO: COMPLETE BOOKSTORE ANALYTICS\n'
             'Web Scraping → EDA → Advanced Visualizations', fontsize=24, fontweight='bold')
plt.savefig('portfolio_masterpiece.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ TASK 3 COMPLETE - 5 SECTIONS ✓")
print("📁 Portfolio files saved:")
print("   section1_raw_to_visuals.png")
print("   section2_tools_demo.png") 
print("   section3_enhanced_visuals.png")
print("   section4_data_stories.png")
print("   portfolio_masterpiece.png")

