# mdparser模块

## 使用

`import mdparser as md`

新建解析器实例并传入文档字符串

`parser = md.parser(raw_string)`

获取文档目录的HTML文本

`table_of_content = parser.getTable()`

获取文档正文的HTML文本

`content = parser.getContent()`

获取带有CSS格式的全部HTML文本

`html = parser.getHTML()`