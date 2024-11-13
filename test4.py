import os

def generate_html_summary(directory):
    # 获取目录下的所有文件
    files = os.listdir(directory)
    
    # 创建 HTML 表格头
    html_content = '''
    <html>
    <head>
        <title>File Summary</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .pass {
                background-color: #c6f6c6; /* 绿色背景 */
            }
            .fail {
                background-color: #f8d7da; /* 红色背景 */
            }
            a {
                color: #007bff; /* 蓝色链接 */
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>File Summary Report</h1>
        <table>
            <tr>
                <th>File Name</th>
                <th>Result</th>
                <th>FBC</th>
            </tr>
    '''
    
    # 遍历文件夹中的文件
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            # 检查文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 设置 Result 列的 pass/fail 状态
            result = 'pass' if not content else 'fail'
            result_class = 'pass' if not content else 'fail'
            
            # 如果是 fail，添加超链接，指向同名的 .html 文件
            if result == 'fail':
                linked_file = f"{os.path.splitext(file)[0]}.html"
                link_html = f'<a href="{linked_file}">{result}</a>'
            else:
                link_html = result
            
            # 检查是否存在同名子目录以及其中是否包含 .svg 文件
            base_name = os.path.splitext(file)[0]
            subdirectory_path = os.path.join(directory, base_name)+'_'
            fbc_result = 'pass'
            fbc_html = 'pass'
            
            # 如果存在同名子目录
            if os.path.isdir(subdirectory_path):
                svg_files = [f for f in os.listdir(subdirectory_path) if f.endswith('.svg')]
                
                # 如果找到 .svg 文件
                if svg_files:
                    fbc_result = 'fail'
                    # 创建一个新的HTML页面用于显示所有的SVG图片
                    svg_html_content = '''
                    <html>
                    <head><title>SVG Files</title></head>
                    <body>
                        <h1>SVG Images for {}</h1>
                    '''.format(base_name)
                    
                    for svg_file in svg_files:
                        svg_path = os.path.join(base_name, svg_file)
                        svg_html_content += f'<div><img src="{svg_path}" alt="{svg_file}"></div>\n'
                    
                    svg_html_content += '''
                    </body>
                    </html>
                    '''
                    
                    # 将新页面保存为 HTML 文件
                    svg_html_file = os.path.join(directory, f"{base_name}_svg.html")
                    with open(svg_html_file, 'w', encoding='utf-8') as f:
                        f.write(svg_html_content)
                    
                    # 设置 FBC 列的超链接
                    fbc_html = f'<a href="{base_name}_svg.html">{fbc_result}</a>'
            
            # 添加文件名和结果到 HTML 中
            html_content += f'''
            <tr>
                <td>{file}</td>
                <td class="{result_class}">{link_html}</td>
                <td class="{fbc_result}">{fbc_html}</td>
            </tr>
            '''
    
    # 关闭 HTML 标签
    html_content += '''
        </table>
    </body>
    </html>
    '''
    
    # 写入生成的HTML文件
    output_file = os.path.join(directory, 'summary_report.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Summary report generated: {output_file}")

# 调用函数生成HTML总结报告
generate_html_summary('./test_data/')

