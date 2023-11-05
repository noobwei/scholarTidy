import pandas as pd
search_term = input("keyword: ")
file_path = f'{search_term}.csv'
df = pd.read_csv(file_path)

# 按照 Cites 列进行降序排序
df = df.sort_values(by='Cites', ascending=False)

author_citations = {}

for index, row in df.iterrows():
    authors = row['Authors'].split(', ')  # 假设作者名字以逗号和空格分隔
    for author in authors:
        if author in author_citations:
            author_citations[author] += row['Cites']
        else:
            author_citations[author] = row['Cites']

# 将作者按照被引量排序
sorted_authors = sorted(author_citations.items(), key=lambda x: x[1], reverse=True)

# 创建一个字典来存储每位作者的论文数量和前三篇被引用最多的论文
author_info = {}

for index, row in df.iterrows():
    authors = row['Authors'].split(', ')  # 假设作者名字以逗号和空格分隔
    for author in authors:
        if author not in author_info:
            author_info[author] = {'ArticleCount': 1, 'TopCitedPapers': []}
        else:
            author_info[author]['ArticleCount'] += 1

        author_info[author]['TopCitedPapers'].append({'Title': row['Title'], 'Cites': row['Cites']})

# 将作者按照被引量排序
sorted_authors = sorted(author_citations.items(), key=lambda x: x[1], reverse=True)

# 创建并写入到新的文本文件
output_file = f'{search_term}_author'  # 新文本文件的路径和名称

with open(output_file, 'w', encoding='utf-8') as file:
    for author, citations in sorted_authors:
        line = f"Author: {author}\n"
        line += f"Total Citations: {citations}\n"
        line += f"Total Articles: {author_info[author]['ArticleCount']}\n"

        top_cited_papers = sorted(author_info[author]['TopCitedPapers'], key=lambda x: x['Cites'], reverse=True)[:3]
        line += "Top 3 Cited Papers:\n"
        for paper in top_cited_papers:
            line += f"- Title: {paper['Title']}, Citations: {paper['Cites']}\n"

        file.write(line + "\n")

print(f"Results saved to {output_file}")

