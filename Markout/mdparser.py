# coding=utf-8
from enum import Enum
import re


# TODO dict may be better?
class formats(Enum):
    null = 0
    para = 1
    h1 = 2
    h2 = 3
    h3 = 4
    h4 = 5
    h5 = 6
    h6 = 7
    italic = 8
    bold = 9
    quote = 10
    ol = 11
    ul = 12
    li = 13
    codeLine = 14
    codeBlock = 15
    href = 16
    img = 17
    hr = 18
    br = 19
    radio = 20
    checkBox = 21
    text = 22


# href, img, boxes have text inside, their tags will be added while dfsing
html_tag_head = [
    "",
    "<p>",
    "<h1 ",
    "<h2 ",
    "<h3 ",
    "<h4 ",
    "<h5 ",
    "<h6 ",
    "<i>",
    "<b>",
    "<blockquote>",
    "<ol>",
    "<ul>",
    "<li>",
    "<code>",
    "<pre><code>",
    "",
    "",
    "<hr color=#CCCCCC size=1 />",
    "<br />",
    "",
    "",
    "",
]

html_tag_end = [
    "",
    "</p>",
    "</h1>",
    "</h2>",
    "</h3>",
    "</h4>",
    "</h5>",
    "</h6>",
    "</i>",
    "</b>",
    "</blockquote>",
    "</ol>",
    "</ul>",
    "</li>",
    "</code>",
    "</code></pre>",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

html_head = """<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>Markdown</title>
        <style type="text/css">
        .markdown-body .octicon {
  display: inline-block;
  fill: currentColor;
  vertical-align: text-bottom;
}

.markdown-body .anchor {
  float: left;
  line-height: 1;
  margin-left: -20px;
  padding-right: 4px;
}

.markdown-body .anchor:focus {
  outline: none;
}

.markdown-body h1 .octicon-link,
.markdown-body h2 .octicon-link,
.markdown-body h3 .octicon-link,
.markdown-body h4 .octicon-link,
.markdown-body h5 .octicon-link,
.markdown-body h6 .octicon-link {
  color: #1b1f23;
  vertical-align: middle;
  visibility: hidden;
}

.markdown-body h1:hover .anchor,
.markdown-body h2:hover .anchor,
.markdown-body h3:hover .anchor,
.markdown-body h4:hover .anchor,
.markdown-body h5:hover .anchor,
.markdown-body h6:hover .anchor {
  text-decoration: none;
}

.markdown-body h1:hover .anchor .octicon-link,
.markdown-body h2:hover .anchor .octicon-link,
.markdown-body h3:hover .anchor .octicon-link,
.markdown-body h4:hover .anchor .octicon-link,
.markdown-body h5:hover .anchor .octicon-link,
.markdown-body h6:hover .anchor .octicon-link {
  visibility: visible;
}

.markdown-body h1:hover .anchor .octicon-link:before,
.markdown-body h2:hover .anchor .octicon-link:before,
.markdown-body h3:hover .anchor .octicon-link:before,
.markdown-body h4:hover .anchor .octicon-link:before,
.markdown-body h5:hover .anchor .octicon-link:before,
.markdown-body h6:hover .anchor .octicon-link:before {
  width: 16px;
  height: 16px;
  content: ' ';
  display: inline-block;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' version='1.1' width='16' height='16' aria-hidden='true'%3E%3Cpath fill-rule='evenodd' d='M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z'%3E%3C/path%3E%3C/svg%3E");
}.markdown-body {
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  line-height: 1.5;
  color: #24292e;
  font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji;
  font-size: 16px;
  line-height: 1.5;
  word-wrap: break-word;
}

.markdown-body details {
  display: block;
}

.markdown-body summary {
  display: list-item;
}

.markdown-body a {
  background-color: initial;
}

.markdown-body a:active,
.markdown-body a:hover {
  outline-width: 0;
}

.markdown-body strong {
  font-weight: inherit;
  font-weight: bolder;
}

.markdown-body h1 {
  font-size: 2em;
  margin: .67em 0;
}

.markdown-body img {
  border-style: none;
}

.markdown-body code,
.markdown-body kbd,
.markdown-body pre {
  font-family: monospace,monospace;
  font-size: 1em;
}

.markdown-body hr {
  box-sizing: initial;
  height: 0;
  overflow: visible;
}

.markdown-body input {
  font: inherit;
  margin: 0;
}

.markdown-body input {
  overflow: visible;
}

.markdown-body [type=checkbox] {
  box-sizing: border-box;
  padding: 0;
}

.markdown-body * {
  box-sizing: border-box;
}

.markdown-body input {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

.markdown-body a {
  color: #0366d6;
  text-decoration: none;
}

.markdown-body a:hover {
  text-decoration: underline;
}

.markdown-body strong {
  font-weight: 600;
}

.markdown-body hr {
  height: 0;
  margin: 15px 0;
  overflow: hidden;
  background: transparent;
  border: 0;
  border-bottom: 1px solid #dfe2e5;
}

.markdown-body hr:after,
.markdown-body hr:before {
  display: table;
  content: "";
}

.markdown-body hr:after {
  clear: both;
}

.markdown-body table {
  border-spacing: 0;
  border-collapse: collapse;
}

.markdown-body td,
.markdown-body th {
  padding: 0;
}

.markdown-body details summary {
  cursor: pointer;
}

.markdown-body kbd {
  display: inline-block;
  padding: 3px 5px;
  font: 11px SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
  line-height: 10px;
  color: #444d56;
  vertical-align: middle;
  background-color: #fafbfc;
  border: 1px solid #d1d5da;
  border-radius: 3px;
  box-shadow: inset 0 -1px 0 #d1d5da;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 0;
  margin-bottom: 0;
}

.markdown-body h1 {
  font-size: 32px;
}

.markdown-body h1,
.markdown-body h2 {
  font-weight: 600;
}

.markdown-body h2 {
  font-size: 24px;
}

.markdown-body h3 {
  font-size: 20px;
}

.markdown-body h3,
.markdown-body h4 {
  font-weight: 600;
}

.markdown-body h4 {
  font-size: 16px;
}

.markdown-body h5 {
  font-size: 14px;
}

.markdown-body h5,
.markdown-body h6 {
  font-weight: 600;
}

.markdown-body h6 {
  font-size: 12px;
}

.markdown-body p {
  margin-top: 0;
  margin-bottom: 10px;
}

.markdown-body blockquote {
  margin: 0;
}

.markdown-body ol,
.markdown-body ul {
  padding-left: 0;
  margin-top: 0;
  margin-bottom: 0;
}

.markdown-body ol ol,
.markdown-body ul ol {
  list-style-type: lower-roman;
}

.markdown-body ol ol ol,
.markdown-body ol ul ol,
.markdown-body ul ol ol,
.markdown-body ul ul ol {
  list-style-type: lower-alpha;
}

.markdown-body dd {
  margin-left: 0;
}

.markdown-body code,
.markdown-body pre {
  font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
  font-size: 12px;
}

.markdown-body pre {
  margin-top: 0;
  margin-bottom: 0;
}

.markdown-body input::-webkit-inner-spin-button,
.markdown-body input::-webkit-outer-spin-button {
  margin: 0;
  -webkit-appearance: none;
  appearance: none;
}

.markdown-body :checked+.radio-label {
  position: relative;
  z-index: 1;
  border-color: #0366d6;
}

.markdown-body .border {
  border: 1px solid #e1e4e8!important;
}

.markdown-body .border-0 {
  border: 0!important;
}

.markdown-body .border-bottom {
  border-bottom: 1px solid #e1e4e8!important;
}

.markdown-body .rounded-1 {
  border-radius: 3px!important;
}

.markdown-body .bg-white {
  background-color: #fff!important;
}

.markdown-body .bg-gray-light {
  background-color: #fafbfc!important;
}

.markdown-body .text-gray-light {
  color: #6a737d!important;
}

.markdown-body .mb-0 {
  margin-bottom: 0!important;
}

.markdown-body .my-2 {
  margin-top: 8px!important;
  margin-bottom: 8px!important;
}

.markdown-body .pl-0 {
  padding-left: 0!important;
}

.markdown-body .py-0 {
  padding-top: 0!important;
  padding-bottom: 0!important;
}

.markdown-body .pl-1 {
  padding-left: 4px!important;
}

.markdown-body .pl-2 {
  padding-left: 8px!important;
}

.markdown-body .py-2 {
  padding-top: 8px!important;
  padding-bottom: 8px!important;
}

.markdown-body .pl-3,
.markdown-body .px-3 {
  padding-left: 16px!important;
}

.markdown-body .px-3 {
  padding-right: 16px!important;
}

.markdown-body .pl-4 {
  padding-left: 24px!important;
}

.markdown-body .pl-5 {
  padding-left: 32px!important;
}

.markdown-body .pl-6 {
  padding-left: 40px!important;
}

.markdown-body .f6 {
  font-size: 12px!important;
}

.markdown-body .lh-condensed {
  line-height: 1.25!important;
}

.markdown-body .text-bold {
  font-weight: 600!important;
}

.markdown-body .pl-c {
  color: #6a737d;
}

.markdown-body .pl-c1,
.markdown-body .pl-s .pl-v {
  color: #005cc5;
}

.markdown-body .pl-e,
.markdown-body .pl-en {
  color: #6f42c1;
}

.markdown-body .pl-s .pl-s1,
.markdown-body .pl-smi {
  color: #24292e;
}

.markdown-body .pl-ent {
  color: #22863a;
}

.markdown-body .pl-k {
  color: #d73a49;
}

.markdown-body .pl-pds,
.markdown-body .pl-s,
.markdown-body .pl-s .pl-pse .pl-s1,
.markdown-body .pl-sr,
.markdown-body .pl-sr .pl-cce,
.markdown-body .pl-sr .pl-sra,
.markdown-body .pl-sr .pl-sre {
  color: #032f62;
}

.markdown-body .pl-smw,
.markdown-body .pl-v {
  color: #e36209;
}

.markdown-body .pl-bu {
  color: #b31d28;
}

.markdown-body .pl-ii {
  color: #fafbfc;
  background-color: #b31d28;
}

.markdown-body .pl-c2 {
  color: #fafbfc;
  background-color: #d73a49;
}

.markdown-body .pl-c2:before {
  content: "^M";
}

.markdown-body .pl-sr .pl-cce {
  font-weight: 700;
  color: #22863a;
}

.markdown-body .pl-ml {
  color: #735c0f;
}

.markdown-body .pl-mh,
.markdown-body .pl-mh .pl-en,
.markdown-body .pl-ms {
  font-weight: 700;
  color: #005cc5;
}

.markdown-body .pl-mi {
  font-style: italic;
  color: #24292e;
}

.markdown-body .pl-mb {
  font-weight: 700;
  color: #24292e;
}

.markdown-body .pl-md {
  color: #b31d28;
  background-color: #ffeef0;
}

.markdown-body .pl-mi1 {
  color: #22863a;
  background-color: #f0fff4;
}

.markdown-body .pl-mc {
  color: #e36209;
  background-color: #ffebda;
}

.markdown-body .pl-mi2 {
  color: #f6f8fa;
  background-color: #005cc5;
}

.markdown-body .pl-mdr {
  font-weight: 700;
  color: #6f42c1;
}

.markdown-body .pl-ba {
  color: #586069;
}

.markdown-body .pl-sg {
  color: #959da5;
}

.markdown-body .pl-corl {
  text-decoration: underline;
  color: #032f62;
}

.markdown-body .mb-0 {
  margin-bottom: 0!important;
}

.markdown-body .my-2 {
  margin-bottom: 8px!important;
}

.markdown-body .my-2 {
  margin-top: 8px!important;
}

.markdown-body .pl-0 {
  padding-left: 0!important;
}

.markdown-body .py-0 {
  padding-top: 0!important;
  padding-bottom: 0!important;
}

.markdown-body .pl-1 {
  padding-left: 4px!important;
}

.markdown-body .pl-2 {
  padding-left: 8px!important;
}

.markdown-body .py-2 {
  padding-top: 8px!important;
  padding-bottom: 8px!important;
}

.markdown-body .pl-3 {
  padding-left: 16px!important;
}

.markdown-body .pl-4 {
  padding-left: 24px!important;
}

.markdown-body .pl-5 {
  padding-left: 32px!important;
}

.markdown-body .pl-6 {
  padding-left: 40px!important;
}

.markdown-body .pl-7 {
  padding-left: 48px!important;
}

.markdown-body .pl-8 {
  padding-left: 64px!important;
}

.markdown-body .pl-9 {
  padding-left: 80px!important;
}

.markdown-body .pl-10 {
  padding-left: 96px!important;
}

.markdown-body .pl-11 {
  padding-left: 112px!important;
}

.markdown-body .pl-12 {
  padding-left: 128px!important;
}

.markdown-body hr {
  border-bottom-color: #eee;
}

.markdown-body kbd {
  display: inline-block;
  padding: 3px 5px;
  font: 11px SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
  line-height: 10px;
  color: #444d56;
  vertical-align: middle;
  background-color: #fafbfc;
  border: 1px solid #d1d5da;
  border-radius: 3px;
  box-shadow: inset 0 -1px 0 #d1d5da;
}

.markdown-body:after,
.markdown-body:before {
  display: table;
  content: "";
}

.markdown-body:after {
  clear: both;
}

.markdown-body>:first-child {
  margin-top: 0!important;
}

.markdown-body>:last-child {
  margin-bottom: 0!important;
}

.markdown-body a:not([href]) {
  color: inherit;
  text-decoration: none;
}

.markdown-body blockquote,
.markdown-body details,
.markdown-body dl,
.markdown-body ol,
.markdown-body p,
.markdown-body pre,
.markdown-body table,
.markdown-body ul {
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-body hr {
  height: .25em;
  padding: 0;
  margin: 24px 0;
  background-color: #e1e4e8;
  border: 0;
}

.markdown-body blockquote {
  padding: 0 1em;
  color: #6a737d;
  border-left: .25em solid #dfe2e5;
}

.markdown-body blockquote>:first-child {
  margin-top: 0;
}

.markdown-body blockquote>:last-child {
  margin-bottom: 0;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-body h1 {
  font-size: 2em;
}

.markdown-body h1,
.markdown-body h2 {
  padding-bottom: .3em;
  border-bottom: 1px solid #eaecef;
}

.markdown-body h2 {
  font-size: 1.5em;
}

.markdown-body h3 {
  font-size: 1.25em;
}

.markdown-body h4 {
  font-size: 1em;
}

.markdown-body h5 {
  font-size: .875em;
}

.markdown-body h6 {
  font-size: .85em;
  color: #6a737d;
}

.markdown-body ol,
.markdown-body ul {
  padding-left: 2em;
}

.markdown-body ol ol,
.markdown-body ol ul,
.markdown-body ul ol,
.markdown-body ul ul {
  margin-top: 0;
  margin-bottom: 0;
}

.markdown-body li {
  word-wrap: break-all;
}

.markdown-body li>p {
  margin-top: 16px;
}

.markdown-body li+li {
  margin-top: .25em;
}

.markdown-body dl {
  padding: 0;
}

.markdown-body dl dt {
  padding: 0;
  margin-top: 16px;
  font-size: 1em;
  font-style: italic;
  font-weight: 600;
}

.markdown-body dl dd {
  padding: 0 16px;
  margin-bottom: 16px;
}

.markdown-body table {
  display: block;
  width: 100%;
  overflow: auto;
}

.markdown-body table th {
  font-weight: 600;
}

.markdown-body table td,
.markdown-body table th {
  padding: 6px 13px;
  border: 1px solid #dfe2e5;
}

.markdown-body table tr {
  background-color: #fff;
  border-top: 1px solid #c6cbd1;
}

.markdown-body table tr:nth-child(2n) {
  background-color: #f6f8fa;
}

.markdown-body img {
  max-width: 100%;
  box-sizing: initial;
  background-color: #fff;
}

.markdown-body img[align=right] {
  padding-left: 20px;
}

.markdown-body img[align=left] {
  padding-right: 20px;
}

.markdown-body code {
  padding: .2em .4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27,31,35,.05);
  border-radius: 3px;
}

.markdown-body pre {
  word-wrap: normal;
}

.markdown-body pre>code {
  padding: 0;
  margin: 0;
  font-size: 100%;
  word-break: normal;
  white-space: pre;
  background: transparent;
  border: 0;
}

.markdown-body .highlight {
  margin-bottom: 16px;
}

.markdown-body .highlight pre {
  margin-bottom: 0;
  word-break: normal;
}

.markdown-body .highlight pre,
.markdown-body pre {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 3px;
}

.markdown-body pre code {
  display: inline;
  max-width: auto;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  word-wrap: normal;
  background-color: initial;
  border: 0;
}

.markdown-body .commit-tease-sha {
  display: inline-block;
  font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
  font-size: 90%;
  color: #444d56;
}

.markdown-body .full-commit .btn-outline:not(:disabled):hover {
  color: #005cc5;
  border-color: #005cc5;
}

.markdown-body .blob-wrapper {
  overflow-x: auto;
  overflow-y: hidden;
}

.markdown-body .blob-wrapper-embedded {
  max-height: 240px;
  overflow-y: auto;
}

.markdown-body .blob-num {
  width: 1%;
  min-width: 50px;
  padding-right: 10px;
  padding-left: 10px;
  font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
  font-size: 12px;
  line-height: 20px;
  color: rgba(27,31,35,.3);
  text-align: right;
  white-space: nowrap;
  vertical-align: top;
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.markdown-body .blob-num:hover {
  color: rgba(27,31,35,.6);
}

.markdown-body .blob-num:before {
  content: attr(data-line-number);
}

.markdown-body .blob-code {
  position: relative;
  padding-right: 10px;
  padding-left: 10px;
  line-height: 20px;
  vertical-align: top;
}

.markdown-body .blob-code-inner {
  overflow: visible;
  font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
  font-size: 12px;
  color: #24292e;
  word-wrap: normal;
  white-space: pre;
}

.markdown-body .pl-token.active,
.markdown-body .pl-token:hover {
  cursor: pointer;
  background: #ffea7f;
}

.markdown-body .tab-size[data-tab-size="1"] {
  -moz-tab-size: 1;
  tab-size: 1;
}

.markdown-body .tab-size[data-tab-size="2"] {
  -moz-tab-size: 2;
  tab-size: 2;
}

.markdown-body .tab-size[data-tab-size="3"] {
  -moz-tab-size: 3;
  tab-size: 3;
}

.markdown-body .tab-size[data-tab-size="4"] {
  -moz-tab-size: 4;
  tab-size: 4;
}

.markdown-body .tab-size[data-tab-size="5"] {
  -moz-tab-size: 5;
  tab-size: 5;
}

.markdown-body .tab-size[data-tab-size="6"] {
  -moz-tab-size: 6;
  tab-size: 6;
}

.markdown-body .tab-size[data-tab-size="7"] {
  -moz-tab-size: 7;
  tab-size: 7;
}

.markdown-body .tab-size[data-tab-size="8"] {
  -moz-tab-size: 8;
  tab-size: 8;
}

.markdown-body .tab-size[data-tab-size="9"] {
  -moz-tab-size: 9;
  tab-size: 9;
}

.markdown-body .tab-size[data-tab-size="10"] {
  -moz-tab-size: 10;
  tab-size: 10;
}

.markdown-body .tab-size[data-tab-size="11"] {
  -moz-tab-size: 11;
  tab-size: 11;
}

.markdown-body .tab-size[data-tab-size="12"] {
  -moz-tab-size: 12;
  tab-size: 12;
}

.markdown-body .task-list-item {
  list-style-type: none;
}

.markdown-body .task-list-item+.task-list-item {
  margin-top: 3px;
}

.markdown-body .task-list-item input {
  margin: 0 .2em .25em -1.6em;
  vertical-align: middle;
}
    </style>
</head>

<body>
    <article class="markdown-body">"""

html_end = """    </article>
</body>

</html>
"""


class parser():
    # these two strings below will be modified by the constructor
    __TOC = ""
    __CONTENT = ""

    # basic nodes
    class Cnode():
        '''
        Structure for TOC
        '''
        def __init__(self, hd: str):
            self.heading = hd
            self.children = []
            self.tag = ""

    class Node():
        '''
        Structure for contents
        '''
        def __init__(self, type: formats):
            self.type = type
            self.children = []
            self.element = ["", "", ""]

    def start(self, src: str) -> tuple:
        '''
        Process the spaces and tabs of one line
        @src str, the source string
        @return tuple, (num, substr)
            num    int, number of spaces/tabs
            substr str, src without the beginning spaces
        '''
        if len(src) == 0:
            return (0, "")
        cntspace = 0
        cnttab = 0
        for i in range(len(src)):
            if src[i] == ' ':
                cntspace += 1
            if src[i] == '\t':
                cnttab += 1
            else:
                return (cnttab + cntspace // 4, src[i:])

    def getType(self, src: str) -> tuple:
        '''
        Judge the type of one line by the head of it
        types: h1 ~ h5, codeblock, ul, ol, quote, para
        @src str the source string
        @return turple, (type, content)
            type    formats, type of this line
            content str, src without format tag
        '''
        i = 0
        while src[i] == '#':
            i += 1
        if i > 0 and src[i] == ' ':
            # value of h1 is 2
            return (formats(i - 1 + 2), src[i + 1:])

        i = 0
        if src[i:i + 3] == "```":
            return (formats.codeBlock, src[i + 3])
        if src[i:i + 2] == "- ":
            return (formats.ul, src[i + 2:])
        if src[i:i + 2] == "> ":
            return (formats.quote, src[i + 2:])
        digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if src[i] in digits and src[i + 1:i + 3] == ". ":
            return (formats.ol, src[i + 3:])
        return (formats.para, src)

    def isHeading(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if v is h1 ~ h6
        '''
        return (v.type.value >= formats.h1.value
                and v.type.value <= formats.h6.value)

    def isImg(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is img
        '''
        return v.type == formats.img

    def isHref(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is href
        '''
        return v.type == formats.href

    def isRadio(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is radio
        '''
        return v.type == formats.radio

    def isCheckBox(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is checkbox
        '''
        return v.type == formats.checkBox

    def isText(self, v: Node) -> bool:
        '''
        @v Node
        @return bool, True if node is text
        '''
        return v.type == formats.text

    def findNode(self, depth: int):
        '''
        With depth of the tree, find the node
        @depth int, depth of target node
        @return Node
        '''
        ptr = self.root
        while len(ptr.children) != 0 and depth != 0:
            ptr = ptr.children[-1]
            if ptr.type == formats.li:
                depth -= 1
        return ptr

    def insert_cnode(self, v: Cnode, x: int, hd: str, tag: int):
        '''
        Insert TOC node
        @cnode Cnode, node to be father
        @x int, depth
        @hd str, content of heading
        @tag formats,  tag = formats(0)
        '''
        n = len(v.children)
        if x == 1:
            v.children.append(self.Cnode(hd))
            v.children[-1].tag = "tag" + str(tag)
            return
        if n == 0 or len(v.children[-1].heading) == 0:
            v.children.append(self.Cnode(""))
        self.insert_cnode(v.children[-1], x - 1, hd, tag)
        return

    # REWRITE, pure char
    # TODO how to make it with pure re?
    def insert_node(self, v: Node, src: str):
        inbold = False
        incode = False
        initalic = False
        v.children.append(self.Node(formats.null))
        n = len(src)
        i = 0
        while i < n:
            ch = src[i]
            # do something and change the flag
            # codeline
            if ch == '`':
                v.children.append(self.Node(
                    formats.null)) if incode else v.children.append(
                        self.Node(formats.codeLine))
                incode = not incode
                i += 1
                continue
            # bold
            if ch == '*' and (i < n - 1 and src[i + 1] == '*') and not incode:
                i += 1
                v.children.append(self.Node(
                    formats.null)) if inbold else v.children.append(
                        self.Node(formats.bold))
                inbold = not inbold
                i += 1
                continue
            # italic
            if ch == '_' and not incode and not inbold:
                v.children.append(self.Node(
                    formats.null)) if initalic else v.children.append(
                        self.Node(formats.italic))
                initalic = not initalic
                i += 1
                continue
            # img
            fimg = re.compile(r"!\[.+\]\(.+( \".+\")?\)")
            if fimg.match(src[i:]) and (i < n - 1 and src[i + 1] == '['
                              ) and not incode and not inbold and not initalic:
                v.children.append(self.Node(formats.img))
                # collect the keywords
                i += 2
                while i < n - 1 and src[i] != ']':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 2
                while i < n - 1 and src[i] != ' ' and src[i] != ')':
                    v.children[-1].element[1] += src[i]
                    i += 1
                if src[i] != ')':
                    i += 1
                    while i < n - 1 and src[i] != ')':
                        if src[i] != '\"':
                            v.children[-1].element[2] += src[i]
                        i += 1
                v.children.append(self.Node(formats.null))
                i += 1
                continue
            # href
            fhref = re.compile(r"\[.+\]\(.+( \".+\")?\)")
            if fhref.match(src[i:]) and not incode and not inbold and not initalic:
                if i == 0 or (i > 0 and src[i - 1] != '!'):
                    v.children.append(self.Node(formats.href))
                    # collect the keywords
                    i += 1
                    while i < n - 1 and src[i] != ']':
                        v.children[-1].element[0] += src[i]
                        i += 1
                    i += 2
                    while i < n - 1 and src[i] != ' ' and src[i] != ')':
                        v.children[-1].element[1] += src[i]
                        i += 1
                    if src[i] != ')':
                        i += 1
                        while i < n - 1 and src[i] != ')':
                            if src[i] != '\"':
                                v.children[-1].element[2] += src[i]
                            i += 1
                    v.children.append(self.Node(formats.null))
                    i += 1
                    continue
            # radio
            fradio = re.compile(r"-.+<[ xX]>.+")
            if fradio.match(
                    src[i:]) and not inbold and not incode and not initalic:
                v.children.append(self.Node(formats.radio))
                # collect the keywords
                i += 1
                while i < n - 1 and src[i] != '<':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 1
                if src[i] == 'x' or src[i] == 'X':
                    v.children[-1].element[2] += "checked"
                i += 2
                while i < n - 1:
                    v.children[-1].element[1] += src[i]
                    i += 1
                v.children.append(self.Node(formats.null))
                i += 1
                continue
            # checkbox
            fcheckbox = re.compile(r"-.+\[[ xX]\].+")
            if fcheckbox.match(
                    src[i:]) and not incode and not inbold and not initalic:
                v.children.append(self.Node(formats.checkBox))
                # collect the keywords
                i += 1
                while i < n - 1 and src[i] != '[':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 1
                if src[i] == 'x' or src[i] == 'X':
                    v.children[-1].element[2] += "checked"
                i += 2
                while i < n - 1:
                    v.children[-1].element[1] += src[i]
                    i += 1
                v.children.append(self.Node(formats.null))
                i += 1
                continue
            # textbox
            ftext = re.compile(r"\(.+\)\[\[.+\]\]")
            if ftext.match(
                    src[i:]) and not inbold and not incode and not initalic:
                v.children.append(self.Node(formats.text))
                # collect the keywords
                i += 1
                while i < n - 1 and src[i] != ')':
                    v.children[-1].element[0] += src[i]
                    i += 1
                i += 3
                while i < n - 1 and src[i] != ']':
                    v.children[-1].element[1] += src[i]
                    i += 1
                v.children.append(self.Node(formats.null))
                i += 2
                continue
            # if none above, push into the normal null node
            v.children[-1].element[0] += ch
            i += 1
        # if a line has 2 or more ending spaces, it makrs a break(<br />)
        if len(src) >= 2:
            if src[-1] == ' ' and src[-2] == ' ':
                v.children.append(self.Node(formats.br))

    # if a line has starting "---", it marks a horizontal line <hr />
    def is_hr(self, src: str) -> bool:
        cnt = 0
        flag = True
        for c in src:
            if c != ' ' and c != '\t' and c != '-':
                flag = False
                break
            if c == '-':
                cnt += 1
        if cnt >= 3:
            flag = True
        return flag

    # use a para to warp nodes
    def make_para(self, v: Node):
        if len(v.children) == 1 and v.children[-1].type == formats.para:
            return
        if v.type == formats.para:
            return
        if v.type == formats.null:
            v.type = formats.para
            return
        x = self.Node(formats.para)
        x.children = v.children
        v.children = [x]

    def dfs_node(self, v: Node):
        if len(v.element[0]) == 0 and len(
                v.children) == 0 and v.type == formats.para:
            return
        # add head
        self.__CONTENT += html_tag_head[v.type.value]
        flag = True
        # heading
        if self.isHeading(v):
            self.__CONTENT += "id=\"" + v.element[0] + "\">"
            flag = False
        # href
        if self.isHref(v):
            self.__CONTENT += "<a  href=\"" + v.element[
                1] + "\" title=\"" + v.element[2] + "\">" + v.element[
                    0] + "</a>"
            flag = False
        # img
        if self.isImg(v):
            self.__CONTENT += "<img alt=\"" + v.element[
                0] + "\" src=\"" + v.element[1] + "\" title=\"" + v.element[
                    2] + "\" />"
            flag = False
        # radio
        if self.isRadio(v):
            self.__CONTENT += "<input type=\"radio\" name=\"" + v.element[
                0] + "\" value=\"" + v.element[1] + "\" "
            if v.element[2] == "checked":
                self.__CONTENT += "checked=\"" + v.element[
                    2] + "\">" + v.element[1]
            else:
                self.__CONTENT += "\">" + v.element[1]
            flag = False
        # checkbox
        if self.isCheckBox(v):
            self.__CONTENT += "<input type=\"checkbox\" name=\"" + v.element[
                0] + "\" value=\"" + v.element[1] + "\" "
            if v.element[2] == "checked":
                self.__CONTENT += "checked=\"" + v.element[
                    2] + "\">" + v.element[1]
            else:
                self.__CONTENT += "\">" + v.element[1]
            flag = False
        # text
        if self.isText(v):
            self.__CONTENT += "<input type=\"text\" name=\"" + v.element[
                0] + "\" value=\"" + v.element[1] + "\">"
            flag = False
        # none of above
        if flag:
            self.__CONTENT += v.element[0]
            flag = False
        # dfs
        for child in v.children:
            self.dfs_node(child)
        # add end
        self.__CONTENT += html_tag_end[v.type.value]

    def dfs_cnode(self, v: Cnode, idx: str):
        self.__TOC += "<li>\n"
        self.__TOC += "<a href=\"#" + v.tag + "\">" + idx + " " + v.heading + "</a>\n"
        n = len(v.children)
        if n:
            self.__TOC += "<ul>\n"
            for i in range(n):
                self.dfs_cnode(v.children[i], idx + str(i + 1) + ".")
            self.__TOC += "</ul>\n"
        self.__TOC += "</li>\n"

    def getTable(self):
        '''
        @return str, table of contents of the markdown file
        in HTML format.
        '''
        return self.__TOC

    def getContent(self):
        '''
        @return str, full contents of the markdown file in HTML format
        '''
        return self.__CONTENT

    def getHTML(self):
        '''
        @return str, complete HTML file
        '''
        return html_head + self.getTable() + self.getContent() + html_end

    # def __init__(self, path: str):
    def __init__(self, raw: str):
        self.Croot = self.Cnode("")
        self.root = self.Node(formats.null)
        self.now = self.Node(formats.null)
        self.cntTag = 0
        self.line = ""
        self.newpara = False
        self.inblock = False
        self.preline = False
        # with open(path, "rt", encoding="utf_8") as fin:
        raw = "\n" + raw
        raw_lines = raw.splitlines()
        for line in raw_lines:
            self.line = line + "\n"
            # while True:
            #     self.line = fin.readline()
            #     if self.line == "":
            #         break

            # not in codeblock and need a hr
            if not self.inblock and self.is_hr(self.line):
                self.now = self.root
                self.now.children.append(self.Node(formats.hr))
                self.newpara = False
                continue

            # handle the leading space/tab
            ps = self.start(self.line)

            # if a line is not in codeblock
            # and is blank
            # it marks the start of a paragraph
            if not self.inblock and ps[1] == "\n":
                # back to the root
                self.now = self.root
                self.newpara = True
                continue

            # get type of this line
            tp = self.getType(ps[1])

            # if is codeblock
            if tp[0] == formats.codeBlock:
                self.now.children.append(
                    self.Node(formats.null
                              )) if self.inblock else self.now.children.append(
                                  self.Node(formats.codeBlock))
                self.inblock = not self.inblock
                continue

            # if in codeblock, insert the content
            if self.inblock:
                self.now.children[-1].element[0] += self.line
                continue

            # if normal paragraph
            if tp[0] == formats.para:
                if self.now == self.root:
                    self.now = self.findNode(ps[0])
                    self.now.children.append(self.Node(formats.para))
                    self.now = self.now.children[-1]

                flag = False
                if self.newpara and len(self.now.children) != 0:
                    ptr = 0
                    for child in self.now.children:
                        if child.type == formats.null:
                            ptr = child
                    if ptr != 0:
                        self.make_para(ptr)
                    flag = True
                if flag:
                    self.now.children.append(self.Node(formats.para))
                    self.now = self.now.children[-1]

                self.now.children.append(self.Node(formats.null))
                self.insert_node(self.now.children[-1], tp[1])
                self.newpara = False
                continue

            self.now = self.findNode(ps[0])

            # if is heading
            if tp[0].value >= formats.h1.value and tp[
                    0].value <= formats.h6.value:
                self.now.children.append(self.Node(tp[0]))
                self.cntTag += 1
                self.now.children[-1].element[0] = "tag" + str(self.cntTag)
                self.insert_node(self.now.children[-1], tp[1])
                self.insert_cnode(self.Croot,
                                  tp[0].value - formats.h1.value + 1, tp[1],
                                  self.cntTag)

            # if is ul
            if tp[0] == formats.ul:
                if len(self.now.children
                       ) == 0 or self.now.children[-1].type != formats.ul:
                    self.now.children.append(self.Node(formats.ul))
                self.now = self.now.children[-1]
                flag = False
                if self.newpara and len(self.now.children) != 0:
                    ptr = None
                    for child in self.now.children:
                        if child.type == formats.li:
                            ptr = child
                    if ptr is not None:
                        self.make_para(ptr)
                    flag = True
                self.now.children.append(self.Node(formats.li))
                self.now = self.now.children[-1]
                if flag:
                    self.now.children.append(self.Node(formats.para))
                    self.now = self.now.children[-1]
                self.insert_node(self.now, tp[1])

            # if ol
            if tp[0] == formats.ol:
                if len(self.now.children
                       ) == 0 or self.now.children[-1].type != formats.ol:
                    self.now.children.append(self.Node(formats.ol))
                self.now = self.now.children[-1]
                flag = False
                if self.newpara and len(self.now.children) != 0:
                    ptr = None
                    for child in self.now.children:
                        if child.type == formats.li:
                            ptr = child
                    if ptr is not None:
                        self.make_para(ptr)
                    flag = True
                self.now.children.append(self.Node(formats.li))
                self.now = self.now.children[-1]
                if flag:
                    self.now.children.append(self.Node(formats.para))
                    self.now = self.now.children[-1]
                self.insert_node(self.now, tp[1])

            if tp[0] == formats.quote:
                if len(self.now.children
                       ) == 0 or self.now.children[-1].type != formats.quote:
                    self.now.children.append(self.Node(formats.quote))
                self.now = self.now.children[-1]
                if self.newpara or len(self.now.children) == 0:
                    self.now.children.append(self.Node(formats.para))
                self.insert_node(self.now.children[-1], tp[1])
            # done a para
            self.newpara = False
        # construct the __CONTENT
        self.dfs_node(self.root)
        # construct the __TOC
        self.__TOC += "<ul>"
        for i in range(len(self.Croot.children)):
            self.dfs_cnode(self.Croot.children[i], str(i + 1) + ".")
        self.__TOC += "</ul>"
