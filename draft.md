# md基本语法

|格式|标记|备注|对应tag|
|:-|:-|:-|:-|
|正文|无||`<p></p>`|
|标题|井号+空格|1~6级|`<h1></h1>`|
|斜体|两侧单下划线||`<i></i>`|
|粗体|两侧双星号无空格||`<b></b>`|
|引用|> + 空格||`<blockquote></blockquote>`|
|有序列表|数字+点+空格||`<ol></ol>`|
|无序列表|短横+空格||`<ul></ul>`|
|列表项|||`<li></li>`|
|行内代码|两侧单斜撇号允许空格||`<code></code>`|
|代码块|两头三撇号||`<pre><code></code><pre>`|
|链接|方括号+圆括号||`<a href=""></a>`|
|图片|叹号+方括号+圆括号||`<img alt="" src="" />`|
|水平分割线|---||`<hr color=#CCCCCC size=1 />`|
|换行|一个空行||`<br />`|
|复选框|短横+空格+有空格的方括号|方括号有x/X时为已勾上|`<input type="checkbox" name="checkbox1" value="" checked="checked">`|
|单选框|短横+空格+有空格的尖括号|尖括号有x/X时为已勾上, `name`必须一样|`<input type="radio" name="1" value="" checked="">`|
|填空框|两侧双方括号, 允许空格||`<input type="text" value="">`|





<input type="radio" name="哈" value="A">1111
<input type="radio" name="哈" value="A">22222
<input type="radio" name="哈" value="A">

radio: elem[0]: name elem[1]: value(also text) elem[2]: "checked" or ""

`-name<checked>value(text)`

`<input type="radio" name="name" value="value" checked = "">value`

checkbox: elem[0]: name elem[1]: value(also text) elem[2] = "checked" or ""

`-name[checked]value(text)`

`<input type="checkbox" name="name" value="value" checked = "">value`

<input type="checkbox" name="checkbox1" value="" checked="">

text: elem[0]: name elem[1]: value

`(name)[[value]]`

<input type="text" name="box1" value="Empty box">

<!-- 考虑为选框和文本框添加额外的格式来获取`name` -->

<!-- `ol` 和 `ul` 中的每项要用 `li` 包裹 -->



# 5号之前实现

解析, 生成html

注意模块化, 以备后续扩展


# notes

Markdown takes a similar DOM tree like HTML, we have to maintain a tree structure.
